# 설치
# pip install tflite-runtime

# MobileNetV2 모델 다운로드
# wget -q https://storage.googleapis.com/download.tensorflow.org/models/\
        #  tflite/mobilenet_v2_1.0_224_quant.tflite
# wget -q https://raw.githubusercontent.com/tensorflow/tensorflow/master/\
        #  tensorflow/lite/examples/label_image/labels.txt
import tflite_runtime.interpreter as tflite
import numpy as np, cv2, time

# ── 1단계: 모델 로드 ──────────────────────────────────────
interpreter = tflite.Interpreter(model_path="mobilenet_v2_1.0_224_quant.tflite")

# ── 2단계: 텐서 메모리 할당 ─────────────────────────────
interpreter.allocate_tensors()

input_details  = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]["shape"]   # [1, 224, 224, 3]
input_dtype = input_details[0]["dtype"]   # uint8
print(f"입력 형태: {input_shape}, 타입: {input_dtype}")

with open("labels.txt") as f:
    labels = [line.strip() for line in f]


def classify(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))

    # ── 3단계: 입력 전처리 ───────────────────────────────
    # uint8 모델: 0~255 그대로
    # float32 모델: (pixel - 127.5) / 127.5 필요
    input_data = np.expand_dims(img, axis=0).astype(np.uint8)
    interpreter.set_tensor(input_details[0]["index"], input_data)

    # ── 4단계: 추론 실행 ─────────────────────────────────
    t0 = time.perf_counter()
    interpreter.invoke()
    ms = (time.perf_counter() - t0) * 1000

    # ── 5단계: 출력 읽기 ─────────────────────────────────
    probs = interpreter.get_tensor(output_details[0]["index"])[0]
    top3  = np.argsort(probs)[::-1][:3]

    print(f"추론 시간: {ms:.1f}ms")
    for i in top3:
        print(f"  {labels[i]:<30}: {probs[i]/255*100:.1f}%")

classify("test_image.jpg")
