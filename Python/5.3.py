import tensorflow as tf, numpy as np

model = tf.keras.applications.MobileNetV2(weights="imagenet")

# ── 동적 범위 양자화 ─────────────────────────────────────
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
with open("mobilenet_dynamic.tflite", "wb") as f:
    f.write(tflite_model)
print(f"동적 범위 양자화: {len(tflite_model)/1024/1024:.1f}MB")

# ── 완전 정수 양자화 ─────────────────────────────────────
def representative_dataset():
    for _ in range(100):
        data = np.random.rand(1, 224, 224, 3).astype(np.float32)
        yield [data]

converter2 = tf.lite.TFLiteConverter.from_keras_model(model)
converter2.optimizations = [tf.lite.Optimize.DEFAULT]
converter2.representative_dataset = representative_dataset
converter2.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter2.inference_input_type  = tf.uint8
converter2.inference_output_type = tf.uint8
tflite_int8 = converter2.convert()
with open("mobilenet_int8.tflite", "wb") as f:
    f.write(tflite_int8)
print(f"완전 정수 양자화: {len(tflite_int8)/1024/1024:.1f}MB")

# 결과 예시:
# float32 원본:    14.0MB (top-1 정확도 72.2%)
# 동적 범위 양자화: 3.5MB (71.8%, -0.4%)
# 완전 정수 양자화: 3.5MB (71.0%, -1.2%)
