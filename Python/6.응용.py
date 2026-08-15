import cv2, numpy as np
from picamera2 import Picamera2
from tflite_runtime.interpreter import Interpreter
 
LABELS = ["정상", "불량"]  # 학습 시 사용한 클래스 순서와 동일해야 함
 
interp = Interpreter(model_path="custom_model.tflite")
interp.allocate_tensors()
in_detail = interp.get_input_details()[0]
out_detail = interp.get_output_details()[0]
_, H, W, _ = in_detail["shape"]
 
cam = Picamera2()
cam.configure(cam.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}))
cam.start()
 
while True:
    frame = cam.capture_array()
    resized = cv2.resize(frame, (W, H))
    input_data = np.expand_dims(resized, axis=0).astype(np.float32) / 255.0
 
    interp.set_tensor(in_detail["index"], input_data)
    interp.invoke()
    probs = interp.get_tensor(out_detail["index"])[0]
 
    class_id = int(np.argmax(probs))
    confidence = float(probs[class_id])
    label = f"{LABELS[class_id]} ({confidence*100:.1f}%)"
    color = (0, 255, 0) if confidence > 0.7 else (0, 165, 255)
 
    bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.putText(bgr, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.9, color, 2)
    cv2.imshow("Custom Classifier", bgr)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
 
cam.stop()
cv2.destroyAllWindows()
