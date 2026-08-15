import threading, time
from picamera2 import Picamera2
import cv2

class ThreadedCamera:
    def __init__(self, width=640, height=480):
        self.cam = Picamera2()
        self.cam.configure(self.cam.create_video_configuration(
            main={"size": (width, height), "format": "RGB888"}))
        self.cam.start()
        self.frame   = None
        self.lock    = threading.Lock()
        self.running = True
        threading.Thread(target=self._update, daemon=True).start()
        time.sleep(0.5)

    def _update(self):
        while self.running:
            frame = self.cam.capture_array()
            with self.lock:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.running = False
        self.cam.stop()


# FPS 비교 테스트
AI_TIME = 0.05  # AI 처리 50ms 시뮬레이션

# 순차 방식
cam_seq = Picamera2()
cam_seq.configure(cam_seq.create_video_configuration(main={"size":(640,480),"format":"RGB888"}))
cam_seq.start()
cnt = 0; t0 = time.perf_counter()
while time.perf_counter() - t0 < 5:
    cam_seq.capture_array()
    time.sleep(AI_TIME)
    cnt += 1
print(f"순차 방식 FPS: {cnt/5:.1f}")
cam_seq.stop()

# 멀티스레드 방식
cam_mt = ThreadedCamera()
cnt = 0; t0 = time.perf_counter()
while time.perf_counter() - t0 < 5:
    cam_mt.read()
    time.sleep(AI_TIME)
    cnt += 1
print(f"멀티스레드 FPS: {cnt/5:.1f}  (약 2~3배 향상)")
cam_mt.stop()
