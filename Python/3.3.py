import RPi.GPIO as GPIO
import time
from datetime import datetime

PIR_PIN = 17
COOLDOWN = 3.0  # 초 단위 중복 알림 방지

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

detection_count = 0
last_alert = 0.0


def motion_detected(channel):
    global detection_count, last_alert
    now = time.time()
    if now - last_alert < COOLDOWN:
        return
    detection_count += 1
    last_alert = now
    print(f"움직임 감지! (누적 {detection_count}회) - {datetime.now():%H:%M:%S}")


GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected, bouncetime=3000)

print("PIR 대기 중... 처음 30~60초는 센서 안정화 시간이 필요하다 (Ctrl+C로 종료)")
try:
    while True:
        time.sleep(1)  # 메인 루프는 슬립 -- 인터럽트가 실제 감지를 담당
except KeyboardInterrupt:
    print(f"총 감지 횟수: {detection_count}회")
    GPIO.cleanup()
