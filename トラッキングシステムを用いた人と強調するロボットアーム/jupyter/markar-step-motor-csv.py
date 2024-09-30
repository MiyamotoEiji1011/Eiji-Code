import cv2
from cv2 import aruco
import numpy as np
import serial
import time
import csv
from datetime import datetime

def get_mark_coordinate(cap, dict_aruco, parameters, num_id):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

    if ids is not None and num_id in ids:
        index = np.where(ids == num_id)[0][0]
        cornerUL = corners[index][0][0]
        cornerUR = corners[index][0][1]
        cornerBR = corners[index][0][2]
        cornerBL = corners[index][0][3]

        center = [(cornerUL[0] + cornerBR[0]) / 2, (cornerUL[1] + cornerBR[1]) / 2]

        # Draw coordinates on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f'ID: {num_id}', (int(center[0]), int(center[1])), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f'Coord: ({center[0]:.2f}, {center[1]:.2f})', (10, 30), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.imshow('Camera Window', frame)

        return center

    # If ID is not found, display the original frame
    cv2.imshow('Camera Window', frame)

    return None

def send_command_and_wait(ser, cap, command, expected_response):
    cap.grab()
    while True:
        if command != "none":
            ser.write((command + '\n').encode())

        response = ser.readline().decode().strip()
        if response == expected_response:
            print("Arduino Response:", response)
            break

def record_to_csv(csv_file, count, captured_coord):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([count, 350, 180, captured_coord[0], captured_coord[1]])

cameraID = 0
cap = cv2.VideoCapture(cameraID)
dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

markID = 5

# Arduinoとのシリアル通信設定
arduino_port = 'COM4'  # Arduinoのポートに合わせて変更
arduino_baudrate = 115200
ser = serial.Serial(arduino_port, arduino_baudrate, timeout=1)

# CSVファイルの初期化
csv_file = 'marker_positions.csv'

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Count', 'Target_X', 'Target_Y', 'Marker_X', 'Marker_Y'])

send_command_and_wait(ser, cap, 'serial_connecting', 'serial_connected')

for i in range(200):
    try:
        send_command_and_wait(ser, cap, 'motor_offset', 'processing_now')
        send_command_and_wait(ser, cap, 'none', 'processing_completed')

        send_command_and_wait(ser, cap, 'motorA_start', 'processing_now')

        # Rest of the code
        while True:
            date = get_mark_coordinate(cap, dict_aruco, parameters, markID)
            if date and date[1] < 180 + 10:
                send_command_and_wait(ser, cap, 'motorA_stop', 'stop_motorA')
                send_command_and_wait(ser, cap, 'none', 'processing_completed')
                break

        send_command_and_wait(ser, cap, 'motorB_start', 'processing_now')

        # Rest of the code
        while True:
            date = get_mark_coordinate(cap, dict_aruco, parameters, markID)
            if date and date[0] < 350 + 10:
                send_command_and_wait(ser, cap, 'motorB_stop', 'stop_motorB')
                send_command_and_wait(ser, cap, 'none', 'processing_completed')
                break

    except Exception as e:
        print("Error:", str(e))

    print(' ----- get_mark_coordinate ----- ')
    date = get_mark_coordinate(cap, dict_aruco, parameters, markID)
    record_to_csv(csv_file, i, date)

send_command_and_wait(ser, cap, 'process_end', 'end_return')
print('------process end------')

ser.close()
cap.release()

cv2.destroyAllWindows()
