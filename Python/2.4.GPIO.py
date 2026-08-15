import RPi.GPIO as GPIO
import time

# 반드시 BCM 체계 먼저 선언
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # 채널 재사용 경고 억제

# 핀 모드 설정
LED_PIN    = 17
BUTTON_PIN = 27
GPIO.setup(LED_PIN,    GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# LED 제어
GPIO.output(LED_PIN, GPIO.HIGH)  # 켜기
time.sleep(1)
GPIO.output(LED_PIN, GPIO.LOW)   # 끄기

# 버튼 읽기
state = GPIO.input(BUTTON_PIN)   # 0 또는 1
print(f'버튼 상태: {state}')

# 인터럽트 방식 (CPU 효율적)
def on_button(channel):
    print(f'버튼 눌림! GPIO{channel}')

GPIO.add_event_detect(
    BUTTON_PIN,
    GPIO.RISING,       # LOW→HIGH 변화 감지
    callback=on_button,
    bouncetime=200     # 200ms 내 중복 이벤트 무시
)

try:
    while True: time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()  # 반드시! 핀 상태 초기화
