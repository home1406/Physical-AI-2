ALLOWED_FUNCTIONS = {
    "set_led": {"pin": (17, 27), "state": (0, 1)},
    "set_servo_angle": {"pin": (17, 27), "angle": (0, 180)},
}
 
def safe_call(func_name: str, args: dict, real_func):
    """화이트리스트에 등록된 함수와 파라미터 범위만 실행 허용"""
    if func_name not in ALLOWED_FUNCTIONS:
        raise PermissionError(f"허용되지 않은 함수 호출: {func_name}")
 
    spec = ALLOWED_FUNCTIONS[func_name]
    for key, (lo, hi) in spec.items():
        if key not in args:
            raise ValueError(f"필수 파라미터 누락: {key}")
        value = args[key]
        if not (lo <= value <= hi):
            raise ValueError(
                f"{key}={value}는 허용 범위 [{lo},{hi}]를 벗어남")
 
    print(f"[검증 통과] {func_name}({args}) 실행")
    return real_func(**args)
 
def set_led(pin, state):
    print(f"GPIO{pin} LED {'ON' if state else 'OFF'}")
 
# LLM이 반환한 함수 호출을 그대로 실행하지 않고 반드시 safe_call을 거친다
llm_call = {"function": "set_led", "arguments": {"pin": 17, "state": 1}}
safe_call(llm_call["function"], llm_call["arguments"], set_led)
 
# 범위를 벗어난 위험한 호출은 차단된다
try:
    dangerous = {"function": "set_servo_angle", "arguments": {"pin": 17, "angle": 999}}
    safe_call(dangerous["function"], dangerous["arguments"], set_led)
except ValueError as e:
    print("차단됨:", e)
