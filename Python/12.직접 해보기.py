import time
 
def drive_motor_safe(direction, target_speed, get_moving_fn,
                      max_time=1.5, step=15, delay=0.03):
    """모터를 서서히 가속하며 예상보다 늦게 움직이면 과부하로 판단"""
    start = time.time()
    motor_ramp(direction, target_speed, step=step, delay=delay)
    while time.time() - start < max_time:
        if get_moving_fn():
            print(f"정상적으로 회전 시작 ({time.time()-start:.2f}초)")
            return "ok"
        time.sleep(0.05)
    motor_stop_smooth()
    set_led_color(255, 0, 0)
    print("과부하(스톨) 감지! 모터 정지, 경고등 점등")
    return "overload"
 
# 사용 예 (인코더나 광센서로 회전 여부를 판단하는 get_moving_fn 재사용)
# result = drive_motor_safe("forward", 150, is_wheel_spinning)
# if result == "overload": notify("모터 과부하 감지됨")
