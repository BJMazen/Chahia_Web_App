from flask import Flask, render_template, send_from_directory, Response, jsonify, request
import cv2
import os
import numpy as np
from ultralytics import YOLO

app = Flask(__name__, static_folder='../frontend/build', template_folder='../frontend/build')

# Load the YOLOv8 model
model = YOLO('best.pt')  # Use your trained best.pt model here

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory(os.path.join(app.static_folder), path)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        video_path = 'uploaded_video.mp4'
        file.save(video_path)
        return jsonify({"message": "File uploaded successfully", "video_path": video_path}), 200

@app.route('/video_feed')
def video_feed():
    video_path = 'uploaded_video.mp4'
    if not os.path.exists(video_path):
        return jsonify({"message": "No video file found"}), 404

    def gen_frames():
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Predict the chicken caliber
            caliber = predict_caliber(frame)

            # Display the caliber prediction on the frame
            if caliber:
                cv2.putText(frame, f'Caliber: {caliber}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, 'No caliber detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        cap.release()
    
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def predict_caliber(frame):
    # Run inference on the frame using YOLOv8 model
    results = model(frame)  # Automatically resizes and preprocesses the image
    
    # Extract predictions (assuming the first prediction contains the caliber information)
    for result in results:
        if len(result.boxes) > 0:
            # Extract the class name or ID as the caliber prediction
            caliber_prediction = result.names[result.boxes[0].cls[0]]
            return caliber_prediction
    
    return None  # Return None if no predictions are found

if __name__ == '__main__':
    app.run(debug=True)
