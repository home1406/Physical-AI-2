import pigpio, time, math

pi = pigpio.pi()

LED_PINS = {
    "red":   18,
    "green": 13,
    "blue":  12,
    "white": 19,   # 단색 LED, 패턴 효과용
}

MOTOR = {"in1": 23, "in2": 24, "ena": 25}

def set_led(name, brightness):
    """0~255 밝기로 LED 하나를 켠다 (PWM)"""
    pi.set_PWM_dutycycle(LED_PINS[name], max(0, min(255, brightness)))

def set_led_color(r, g, b):
    """RGB LED 색상을 동시에 설정 (0~255)"""
    set_led("red", r)
    set_led("green", g)
    set_led("blue", b)

def leds_off():
    for name in LED_PINS:
        set_led(name, 0)

def motor_stop():
    pi.write(MOTOR["in1"], 0)
    pi.write(MOTOR["in2"], 0)
    pi.set_PWM_dutycycle(MOTOR["ena"], 0)

def motor_drive(direction, speed):
    """direction: 'forward' 또는 'backward', speed: 0~255"""
    speed = max(0, min(255, speed))
    if direction == "forward":
        pi.write(MOTOR["in1"], 1); pi.write(MOTOR["in2"], 0)
    else:
        pi.write(MOTOR["in1"], 0); pi.write(MOTOR["in2"], 1)
    pi.set_PWM_dutycycle(MOTOR["ena"], speed)
