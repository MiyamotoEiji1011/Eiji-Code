from flask import Flask, render_template, Response, request, jsonify
import cv2
import serial
import time
import os
from pydub import AudioSegment
from pydub.playback import play

app = Flask(__name__)

ser1 = serial.Serial('COM15', 9600)
ser2 = serial.Serial('COM16', 9600)
time.sleep(2)

SOUNDS_FOLDER = 'audio'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_button', methods=['POST'])
def send_button():
    global current_value
    data = request.get_json()
    value = data.get('value')

    try:
        current_value = int(value)
        ser1.write(f"{current_value}\n".encode())
        print(f"Sent to Arduino 1: {current_value}")
        response = ser1.readline().decode().strip()
        print(f"Response from Arduino 1: {response}")
        return jsonify({'status': 'success'})
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid value'})

@app.route('/adjust_offset', methods=['POST'])
def adjust_offset():
    data = request.get_json()
    adjustment = data.get('adjustment')
    
    try:
        adjustment = int(adjustment)
        ser2.write(f"{adjustment}\n".encode())
        print(f"Sent to Arduino 2: {adjustment}")
        response = ser2.readline().decode().strip()
        print(f"Response from Arduino 2: {response}")
        return jsonify({'status': 'success', 'offset': adjustment})
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid adjustment'})

@app.route('/send_special_button', methods=['POST'])
def send_special_button():
    data = request.get_json()
    value = data.get('value')

    try:
        ser2.write(f"{value}\n".encode())
        print(f"Sent special command to Arduino 2: {value}")
        response = ser2.readline().decode().strip()
        print(f"Response from Arduino 2: {response}")
        return jsonify({'status': 'success'})
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid special command'})

@app.route('/play_sound', methods=['POST'])
def play_sound():
    data = request.get_json()
    sound_id = data.get('sound_id')
    
    try:
        file_path = os.path.join(SOUNDS_FOLDER, f"sound{sound_id}.wav")
        
        if not os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': 'File not found'})
        
        sound = AudioSegment.from_file(file_path)
        play(sound)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
