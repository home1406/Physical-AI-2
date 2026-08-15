import pigpio, time
 
pi = pigpio.pi()
SERVO_PINS = [17, 18, 27, 22]  # 다중 서보 제어 예시
 
def angle_to_pulsewidth(angle):
    """0~180도를 500~2500us 펄스폭으로 변환"""
    return int(500 + (angle / 180) * 2000)
 
def move_all_smooth(pi, pins, start_angles, target_angles, duration=1.0, steps=60):
    """여러 서보를 같은 시간(duration) 동안 동시에 목표 각도로 이동"""
    assert len(pins) == len(start_angles) == len(target_angles)
    delay = duration / steps
    for step in range(1, steps + 1):
        t = step / steps
        for pin, start, target in zip(pins, start_angles, target_angles):
            angle = start + (target - start) * t
            pi.set_servo_pulsewidth(pin, angle_to_pulsewidth(angle))
        time.sleep(delay)
 
# 사용 예: 초기 자세에서 물건을 집는 자세로 동시에 이동
home = [90, 90, 90, 30]
pick = [45, 120, 60, 90]
move_all_smooth(pi, SERVO_PINS, home, pick, duration=1.2)
time.sleep(0.5)
move_all_smooth(pi, SERVO_PINS, pick, home, duration=1.2)
 
for pin in SERVO_PINS:
    pi.set_servo_pulsewidth(pin, 0)  # 서보 떨림 방지를 위해 신호 끄기
pi.stop()
