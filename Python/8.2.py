import RPi.GPIO as GPIO, time

IN1, IN2, IN3, IN4 = 17, 18, 27, 22
PINS = [IN1, IN2, IN3, IN4]

GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS, GPIO.OUT)
GPIO.output(PINS, GPIO.LOW)

HALF_STEP = [
    [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0],
    [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1],
]

STEPS_PER_REV = 2048

class StepperMotor:
    def __init__(self, delay_ms=2.0):
        self.delay    = delay_ms / 1000
        self.position = 0

    def step(self, direction=1):
        self.position = (self.position + direction) % len(HALF_STEP)
        for i, pin in enumerate(PINS):
            GPIO.output(pin, HALF_STEP[self.position][i])
        time.sleep(self.delay)

    def rotate_degrees(self, degrees):
        steps     = int(abs(degrees) / 360 * STEPS_PER_REV)
        direction = 1 if degrees > 0 else -1
        for _ in range(steps):
            self.step(direction)
        print(f"{degrees:.1f}° 회전 완료 ({steps} 스텝)")

    def stop(self):
        GPIO.output(PINS, GPIO.LOW)


motor = StepperMotor(delay_ms=2.0)
try:
    motor.rotate_degrees(360)
    time.sleep(0.5)
    motor.rotate_degrees(-180)
    motor.stop()
except KeyboardInterrupt:
    motor.stop()
    GPIO.cleanup()
