# ── 기본 캡처 코드 ─────────────────────────────────────────
from picamera2 import Picamera2
import cv2, time

cam = Picamera2()

# 640×480 RGB888 포맷 설정
config = cam.create_video_configuration(
    main={"format": "RGB888", "size": (640, 480)},
    controls={"FrameDurationLimits": (33333, 33333)}  # 30 FPS
)
cam.configure(config)
cam.start()
time.sleep(0.5)  # 카메라 워밍업

# 프레임 캡처
frame = cam.capture_array()  # numpy: (480, 640, 3) uint8
print(f"프레임 크기: {frame.shape}  dtype: {frame.dtype}")

# OpenCV는 BGR 사용 → RGB→BGR 변환
frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

# 이미지 저장
cv2.imwrite("capture.jpg", frame_bgr)
print("capture.jpg 저장 완료")

cam.stop()
cam.close()
