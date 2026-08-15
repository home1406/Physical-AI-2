import math
 
def expected_pwm(target_percent, max_value=255):
    """목표 값(0~100%)을 PWM 듀티사이클(0~255)로 변환"""
    return round(target_percent / 100 * max_value)
 
def verify_output(name, pin, target_percent, tolerance=5):
    """설정한 PWM 값이 실제로 핀에 적용됐는지 재검증"""
    target_duty = expected_pwm(target_percent)
    actual_duty = pi.get_PWM_dutycycle(pin)
    error = abs(actual_duty - target_duty)
    ok = error <= tolerance
    print(f"{name}: 목표 {target_duty} 실제 {actual_duty} "
          f"오차 {error} -> {'통과' if ok else '실패'}")
    return ok
 
# PWM 설정 후에는 항상 실제 적용값을 재검증한 뒤 다음 동작으로 넘어가는 것이 안전하다
set_led("red", expected_pwm(80))
verify_output("red LED", LED_PINS["red"], target_percent=80)
