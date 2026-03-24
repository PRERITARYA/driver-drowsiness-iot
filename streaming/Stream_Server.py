from flask import Flask, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # your laptop webcam

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        # Resize to match Pi's expected resolution
        frame = cv2.resize(frame, (320, 240))
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)