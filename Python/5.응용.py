import time, numpy as np
from tflite_runtime.interpreter import Interpreter
 
def benchmark(model_path, n_runs=50):
    interp = Interpreter(model_path=model_path)
    interp.allocate_tensors()
    input_detail = interp.get_input_details()[0]
    shape = input_detail["shape"]
    dtype = input_detail["dtype"]
 
    if dtype == np.uint8:
        dummy = np.random.randint(0, 255, shape, dtype=np.uint8)
    else:
        dummy = np.random.rand(*shape).astype(np.float32)
 
    interp.set_tensor(input_detail["index"], dummy)
    interp.invoke()  # 워밍업 (첫 실행은 느림)
 
    start = time.perf_counter()
    for _ in range(n_runs):
        interp.set_tensor(input_detail["index"], dummy)
        interp.invoke()
    elapsed = time.perf_counter() - start
    return (elapsed / n_runs) * 1000  # ms/회
 
fp32_ms = benchmark("model_fp32.tflite")
int8_ms = benchmark("model_int8.tflite")
 
print(f"FP32: {fp32_ms:.2f} ms/추론 ({1000/fp32_ms:.1f} FPS)")
print(f"INT8: {int8_ms:.2f} ms/추론 ({1000/int8_ms:.1f} FPS)")
print(f"속도 향상: {fp32_ms/int8_ms:.2f}배")
