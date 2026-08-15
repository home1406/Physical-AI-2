from flask import Flask, Response
from picamera2 import Picamera2
import cv2, threading, time

app = Flask(__name__)

class CameraStream:
    def __init__(self):
        self.cam = Picamera2()
        self.cam.configure(self.cam.create_video_configuration(
            main={"size": (640,480)}))
        self.cam.start()
        self.frame = None
        self.lock  = threading.Lock()
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while True:
            raw   = self.cam.capture_array()
            frame = cv2.cvtColor(raw, cv2.COLOR_RGB2BGR)
            ts    = time.strftime("%H:%M:%S")
            cv2.putText(frame, ts, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
            _, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
            with self.lock:
                self.frame = jpeg.tobytes()

    def get_frame(self):
        with self.lock:
            return self.frame


stream = CameraStream()

def generate():
    while True:
        frame = stream.get_frame()
        if frame:
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        time.sleep(1/20)

@app.route("/video")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/")
def index():
    return """<html><body style="background:#111">
    <h2 style="color:#4af;text-align:center">📷 라즈베리파이 카메라</h2>
    <div style="text-align:center">
    <img src="/video" style="max-width:640px">
    </div></body></html>"""


if __name__ == "__main__":
    print("브라우저에서: http://라즈베리파이IP:5000/")
    app.run(host="0.0.0.0", port=5000, threaded=True)
