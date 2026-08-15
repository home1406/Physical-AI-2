import RPi.GPIO as GPIO
import time, statistics

TRIG, ECHO = 23, 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, GPIO.LOW)
time.sleep(0.5)  # 센서 안정화 대기


def measure_once(timeout=0.03):
    """단일 거리 측정. 실패 시 None 반환."""
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    t0 = time.perf_counter()
    while GPIO.input(ECHO) == GPIO.LOW:
        if time.perf_counter() - t0 > timeout:
            return None
    start = time.perf_counter()

    while GPIO.input(ECHO) == GPIO.HIGH:
        if time.perf_counter() - start > timeout:
            return None
    end = time.perf_counter()

    dist = (end - start) * 34300 / 2  # 음속 34300cm/s
    return round(dist, 1) if 2.0 <= dist <= 350.0 else None


def measure_stable(n=5):
    """n회 측정 후 중앙값 반환 (이상값 자동 제거)."""
    readings = [d for d in (measure_once() for _ in range(n)) if d is not None]
    if len(readings) < 2:
        return None
    return statistics.median(readings)


if __name__ == "__main__":
    print("HC-SR04 거리 측정 (Ctrl+C로 종료)")
    try:
        while True:
            dist = measure_stable()
            print(f"{dist:.1f}cm" if dist is not None else "측정 실패 — 범위 초과 또는 반사 없음")
            time.sleep(0.2)
    except KeyboardInterrupt:
        GPIO.cleanup()
