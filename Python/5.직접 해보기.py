import time, cv2
from ultralytics import YOLO
 
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)
 
def measure(imgsz, n_frames=30):
    fps_list, count_list = [], []
    for _ in range(n_frames):
        ret, frame = cap.read()
        if not ret:
            break
        t0 = time.perf_counter()
        results = model(frame, imgsz=imgsz, verbose=False)
        elapsed = time.perf_counter() - t0
        fps_list.append(1 / elapsed if elapsed > 0 else 0)
        count_list.append(len(results[0].boxes))
    return sum(fps_list) / len(fps_list), sum(count_list) / len(count_list)
 
print(f"{'해상도':>8}{'평균FPS':>10}{'평균탐지수':>12}")
for size in [320, 480, 640]:
    fps, count = measure(size)
    print(f"{size:8d}{fps:10.1f}{count:12.1f}")
 
cap.release()
