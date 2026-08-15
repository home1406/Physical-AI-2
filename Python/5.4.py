# 성능 비교 (YOLOv8n, 640×640 입력):
# ──────────────────────────────────────────────────────
# 방식                  FPS      CPU 사용률   소비 전력
# ──────────────────────────────────────────────────────
# CPU 전용              ~8 FPS   95%          약 8W
# TFLite INT8 (CPU)    ~12 FPS  85%          약 7W
# Hailo-8L             ~80 FPS  15%          약 3W
# ──────────────────────────────────────────────────────
# Hailo-8L 설치
# sudo apt update
# sudo apt install hailo-all -y
# sudo reboot

# 확인
# hailortcli fw-control identify

# Python 바인딩
# pip install hailort
# Hailo로 YOLOv8n 실행
from picamera2 import Picamera2
from picamera2.devices.hailo import Hailo
import cv2

MODEL = "/usr/share/hailo-models/yolov8n.hef"

with Hailo(MODEL) as hailo:
    h, w, _ = hailo.get_input_shape()
    cam = Picamera2()
    cam.configure(cam.create_video_configuration(
        main={"size": (1280,960), "format": "RGB888"},
        lores={"size": (w, h), "format": "RGB888"}
    ))
    cam.start()

    while True:
        frame, lores = cam.capture_arrays(["main","lores"])
        results = hailo.run(lores)
        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        for det in results:
            if det["score"] < 0.5: continue
            bbox = det["bbox"]
            fh, fw = bgr.shape[:2]
            x1,y1 = int(bbox[0]*fw), int(bbox[1]*fh)
            x2,y2 = int(bbox[2]*fw), int(bbox[3]*fh)
            cv2.rectangle(bgr, (x1,y1), (x2,y2), (0,255,0), 2)

        cv2.imshow("Hailo YOLOv8", bgr)
        if cv2.waitKey(1) & 0xFF == ord("q"): break

    cam.stop()
