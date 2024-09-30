import cv2
from cv2 import aruco
import numpy as np
import serial
import time
import mediapipe as mp
import keyboard       

def get_index_finger_tip_coordinates(cap):
    while True:
        ret, frame = cap.read()
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]  # Assuming only one hand is detected
            index_finger_tip = hand_landmarks.landmark[8]
            height, width, _ = frame.shape

            # 座標変換: 中心を原点とする座標系に変換
            x_pixel = int(index_finger_tip.x * width - width / 2)
            y_pixel = int(index_finger_tip.y * height - height / 2)

            return x_pixel, y_pixel



def send_command_and_wait(ser, cap, command, expected_response):
    cap.grab()
    while True:
        if command != "none":
            ser.write((command + '\n').encode())
     
        response = ser.readline().decode().strip()
        if response == expected_response:
            print("Arduino Response:", response)
            break

def get_mark_coordinate(cap, dict_aruco, parameters, num_id):
    while True:
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
            
            # Get the image center coordinates
            height, width, _ = frame.shape
            image_center = (width // 2, height // 2)

            # Convert coordinates to center-based coordinate system
            center_based_coords = (int(center[0]) - image_center[0], int(center[1]) - image_center[1])

            return center_based_coords



hands = mp.solutions.hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5)

cameraID = 0
cap = cv2.VideoCapture(cameraID)
dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

markID = 5

# Arduinoとのシリアル通信設定
arduino_port = 'COM4'  # Arduinoのポートに合わせて変更
arduino_baudrate = 115200
ser = serial.Serial(arduino_port, arduino_baudrate, timeout=1)

timeout_seconds = 5  # 30秒のタイムアウトを設定

try:
    send_command_and_wait(ser, cap, 'serial_connecting', 'serial_connected')
    send_command_and_wait(ser, cap, 'motor_offset', 'processing_now')
    send_command_and_wait(ser, cap, 'none', 'processing_completed')
    time.sleep(2)
    ###key press
    #print("Press SPACE to start the process.")
    # keyboard.wait("space")  # スペースキーが押されるまで待機

    coordinates = get_index_finger_tip_coordinates(cap)
    x_pixel, y_pixel = coordinates

    if coordinates:

        if 160 < x_pixel < -130 and 160 < y_pixel < 130:
            # マーカー位置の取得
            marker_position = get_mark_coordinate(cap, dict_aruco, parameters, markID)
            if marker_position:
                print(f"Index Finger Tip: ({x_pixel}, {y_pixel})")
                print(f"ArUco Marker Position: {marker_position}")
        print(f"Index Finger Tip: ({x_pixel}, {y_pixel})")

    
    send_command_and_wait(ser, cap, 'motorB_start', 'processing_now')

    # Rest of the code
    start_time = time.time()
    while True:
        date = get_mark_coordinate(cap, dict_aruco, parameters, markID)
        if date[0] <= x_pixel + 30:
            send_command_and_wait(ser, cap, 'motorB_stop', 'stop_motorB')
            send_command_and_wait(ser, cap, 'none', 'processing_completed')
            break

        if time.time() - start_time > timeout_seconds:
            print("Timeout reached. Exiting the loop.")
            break


    send_command_and_wait(ser, cap, 'motorA_start', 'processing_now')

    # Rest of the code
    start_time = time.time()
    while True:
        date = get_mark_coordinate(cap, dict_aruco, parameters, markID)
        if date[1] <= y_pixel + 190:
            send_command_and_wait(ser, cap, 'motorA_stop', 'stop_motorA')
            send_command_and_wait(ser, cap, 'none', 'processing_completed')
            break
        if time.time() - start_time > timeout_seconds:
            print("Timeout reached. Exiting the loop.")
            break

    send_command_and_wait(ser, cap, 'servo_start', 'processing_now')
    send_command_and_wait(ser, cap, 'none', 'processing_completed')

except Exception as e:
    print("Error:", str(e))


time.sleep(1)

print(' ----- get_mark_coordinate ----- ')
print(get_mark_coordinate(cap, dict_aruco, parameters, markID))

send_command_and_wait(ser, cap, 'process_end', 'end_return')
print('------process end------')

ser.close()
cap.release()

cv2.destroyAllWindows()
