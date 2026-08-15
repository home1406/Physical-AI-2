import time
 
def trapezoidal_delays(total_steps, min_delay=0.002, max_delay=0.008, accel_ratio=0.25):
    """사다리꼴 속도 프로파일의 각 스텝별 지연시간 리스트를 생성"""
    accel_steps = max(1, int(total_steps * accel_ratio))
    cruise_steps = total_steps - 2 * accel_steps
    if cruise_steps < 0:
        accel_steps = total_steps // 2
        cruise_steps = total_steps - 2 * accel_steps
 
    delays = []
    for i in range(accel_steps):
        t = i / max(accel_steps - 1, 1)
        delays.append(max_delay - (max_delay - min_delay) * t)
    delays += [min_delay] * cruise_steps
    for i in range(total_steps - accel_steps - cruise_steps):
        t = i / max(accel_steps - 1, 1)
        delays.append(min_delay + (max_delay - min_delay) * t)
    return delays
 
def move_stepper_smooth(step_fn, total_steps, direction=1):
    for delay in trapezoidal_delays(total_steps):
        step_fn(direction)
        time.sleep(delay)
 
# 사용 예 (8.2절의 step() 함수 재사용)
# move_stepper_smooth(stepper.step, total_steps=512, direction=1)  # 약 90도 회전
