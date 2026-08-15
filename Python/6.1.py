# YOLOv8 설치
# pip install ultralytics

from ultralytics import YOLO
from picamera2 import Picamera2
import cv2, time, numpy as np

model = YOLO("yolov8n.pt")  # nano 모델

cam = Picamera2()
cam.configure(cam.create_video_configuration(
    main={"size": (640,480), "format": "RGB888"}))
cam.start()

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(80, 3), dtype=np.uint8)

fps = 0; cnt = 0; t_fps = time.perf_counter()

while True:
    frame = cam.capture_array()
    bgr   = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    results = model(bgr, imgsz=320, conf=0.5, verbose=False)

    for r in results:
        for box in (r.boxes or []):
            x1,y1,x2,y2 = map(int, box.xyxy[0])
            cls   = int(box.cls[0])
            conf  = float(box.conf[0])
            label = model.names[cls]
            color = COLORS[cls].tolist()
            cv2.rectangle(bgr, (x1,y1), (x2,y2), color, 2)
            cv2.putText(bgr, f"{label} {conf:.2f}",
                        (x1, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cnt += 1
    if time.perf_counter() - t_fps >= 1:
        fps = cnt; cnt = 0; t_fps = time.perf_counter()

    cv2.putText(bgr, f"FPS: {fps}  감지: {len(results[0].boxes)}개",
                (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
    cv2.imshow("YOLOv8n", bgr)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cam.stop()
cv2.destroyAllWindows()
