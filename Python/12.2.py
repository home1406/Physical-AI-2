current_speed = 0

def motor_ramp(direction, target_speed, step=15, delay=0.03):
    """현재 속도에서 목표 속도까지 서서히 변화"""
    global current_speed
    target_speed = max(0, min(255, target_speed))
    if direction == "forward":
        pi.write(MOTOR["in1"], 1); pi.write(MOTOR["in2"], 0)
    else:
        pi.write(MOTOR["in1"], 0); pi.write(MOTOR["in2"], 1)
    while current_speed != target_speed:
        if current_speed < target_speed:
            current_speed = min(target_speed, current_speed + step)
        else:
            current_speed = max(target_speed, current_speed - step)
        pi.set_PWM_dutycycle(MOTOR["ena"], current_speed)
        time.sleep(delay)

def motor_stop_smooth():
    motor_ramp("forward", 0)
    pi.write(MOTOR["in1"], 0)
    pi.write(MOTOR["in2"], 0)
