import time, json, numpy as np
from tflite_runtime.interpreter import Interpreter
 
MODELS = ["mobilenet_fp32.tflite", "mobilenet_int8.tflite", "yolov8n_int8.tflite"]
 
def profile_model(path, n_runs=30):
    interp = Interpreter(model_path=path)
    interp.allocate_tensors()
    detail = interp.get_input_details()[0]
    shape, dtype = detail["shape"], detail["dtype"]
    dummy = (np.random.randint(0, 255, shape, dtype=np.uint8)
             if dtype == np.uint8 else np.random.rand(*shape).astype(np.float32))
    interp.set_tensor(detail["index"], dummy)
    interp.invoke()  # 워밍업
    times = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        interp.set_tensor(detail["index"], dummy)
        interp.invoke()
        times.append((time.perf_counter() - t0) * 1000)
    return {
        "mean_ms": float(np.mean(times)),
        "std_ms": float(np.std(times)),
        "fps": 1000 / float(np.mean(times)),
    }
 
report = {}
for model_path in MODELS:
    try:
        report[model_path] = profile_model(model_path)
        print(f"{model_path}: {report[model_path]['fps']:.1f} FPS")
    except Exception as e:
        report[model_path] = {"error": str(e)}
 
with open("model_benchmark.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)
