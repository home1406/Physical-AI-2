"""security_camera.py — 스마트 보안 카메라"""
import threading, time, logging
import cv2, RPi.GPIO as GPIO
from picamera2 import Picamera2
from ultralytics import YOLO
from flask import Flask, Response
import requests, json

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s")
log = logging.getLogger("SecurityCam")

TELEGRAM_TOKEN   = "YOUR_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
PIR_PIN          = 17
CONFIDENCE       = 0.55
ALERT_COOLDOWN   = 60


class PIRController:
    def __init__(self, pin, cooldown=5):
        self.pin      = pin
        self.cooldown = cooldown
        self._last    = 0
        self._cb      = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING,
            callback=self._on, bouncetime=3000)

    def _on(self, ch):
        now = time.time()
        if now - self._last < self.cooldown: return
        self._last = now
        if self._cb: self._cb()

    def on_motion(self, fn): self._cb = fn


class ObjectDetector:
    def __init__(self, model="yolov8n.pt", conf=0.55):
        self.model = YOLO(model)
        self.conf  = conf

    def detect_persons(self, frame_bgr):
        results = self.model(frame_bgr, imgsz=320, conf=self.conf, verbose=False)
        return [box for r in results for box in (r.boxes or []) if int(box.cls[0]) == 0]


class SecurityCamera:
    def __init__(self):
        self.cam = Picamera2()
        self.cam.configure(self.cam.create_video_configuration(
            main={"size":(640,480), "format":"RGB888"}))
        self.cam.start()
        time.sleep(0.5)

        self.pir      = PIRController(PIR_PIN)
        self.detector = ObjectDetector()

        self._frame      = None
        self._frame_lock = threading.Lock()
        self._detect_evt = threading.Event()
        self._last_alert = 0

        self.pir.on_motion(lambda: self._detect_evt.set())

        self.app = Flask(__name__)
        self.app.add_url_rule("/",      "index", self._index)
        self.app.add_url_rule("/video", "video", self._video)

    def _capture_loop(self):
        while True:
            frame = self.cam.capture_array()
            bgr   = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            ts    = time.strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(bgr, ts, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
            with self._frame_lock:
                self._frame = bgr

    def _detect_loop(self):
        while True:
            self._detect_evt.wait()
            self._detect_evt.clear()
            with self._frame_lock:
                if self._frame is None: continue
                frame = self._frame.copy()
            persons = self.detector.detect_persons(frame)
            if persons and time.time() - self._last_alert > ALERT_COOLDOWN:
                self._last_alert = time.time()
                log.info(f"사람 감지! {len(persons)}명")
                self._send_telegram(frame, len(persons))

    def _send_telegram(self, frame, count):
        _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                data={"chat_id": TELEGRAM_CHAT_ID,
                      "caption": f"🚨 사람 감지! {count}명\n{time.strftime('%H:%M:%S')}"},
                files={"photo": ("cam.jpg", buf.tobytes(), "image/jpeg")},
                timeout=10
            )
        except Exception as e:
            log.error(f"텔레그램 오류: {e}")

    def _generate(self):
        while True:
            with self._frame_lock:
                f = self._frame
            if f is not None:
                _, jpeg = cv2.imencode(".jpg", f, [cv2.IMWRITE_JPEG_QUALITY, 70])
                yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                       + jpeg.tobytes() + b"\r\n")
            time.sleep(1/20)

    def _video(self):
        return Response(self._generate(),
            mimetype="multipart/x-mixed-replace; boundary=frame")

    def _index(self):
        return """<html><body style="background:#0a0a1a">
        <h2 style="color:#4af;text-align:center">🔐 스마트 보안 카메라</h2>
        <div style="text-align:center">
        <img src="/video" style="max-width:640px">
        </div></body></html>"""

    def run(self, port=5000):
        for fn in [self._capture_loop, self._detect_loop]:
            threading.Thread(target=fn, daemon=True).start()
        log.info(f"보안 카메라 시작. http://라즈베리파이IP:{port}/")
        self.app.run(host="0.0.0.0", port=port, threaded=True)


if __name__ == "__main__":
    cam = SecurityCamera()
    try:
        cam.run()
    except KeyboardInterrupt:
        GPIO.cleanup()
