import cv2, numpy as np, RPi.GPIO as GPIO, time
 
IR_LED_PIN = 23
NIGHT_THRESHOLD = 60  # 0~255 기준, 이보다 어두우면 야간으로 판단
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_LED_PIN, GPIO.OUT)
GPIO.output(IR_LED_PIN, GPIO.LOW)
 
def is_night(frame_bgr) -> bool:
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    return float(np.mean(gray)) < NIGHT_THRESHOLD
 
def update_night_mode(frame_bgr, current_state: bool) -> bool:
    """밝기를 판단해 IR LED를 제어하고 현재 야간 여부를 반환"""
    night = is_night(frame_bgr)
    if night != current_state:
        GPIO.output(IR_LED_PIN, GPIO.HIGH if night else GPIO.LOW)
        print("야간 모드 전환" if night else "주간 모드 전환")
    return night
 
cap = cv2.VideoCapture(0)
night_state = False
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        night_state = update_night_mode(frame, night_state)
        label = "야간" if night_state else "주간"
        cv2.putText(frame, label, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Night Mode", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
