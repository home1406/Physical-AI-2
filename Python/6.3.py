# 데이터셋 구조:
# dataset/
# ├── images/
# │   ├── train/  ← 학습용 이미지 (80%)
# │   └── val/    ← 검증용 이미지 (20%)
# └── labels/
#     ├── train/  ← YOLO 형식 레이블 (.txt)
#     └── val/

# dataset.yaml:
# path: /home/pi/dataset
# train: images/train
# val: images/val
# nc: 2
# names: ['good', 'bad']
from ultralytics import YOLO

# 사전학습 모델에서 전이학습 시작
model = YOLO("yolov8n.pt")

results = model.train(
    data="dataset.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
    device="cpu",
    patience=10,
    name="my_model",
    project="runs/train",
    workers=2,
    cache=True,
)

print(f"mAP50: {results.results_dict['metrics/mAP50(B)']:.3f}")
print(f"최적 모델: runs/train/my_model/weights/best.pt")

# 학습된 모델로 추론
my_model     = YOLO("runs/train/my_model/weights/best.pt")
test_results = my_model("test_image.jpg")
test_results[0].show()
