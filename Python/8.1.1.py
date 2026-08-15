import pigpio, time


class Servo:
    MIN_PULSE = 500    # 0°  (μs)
    MAX_PULSE = 2500   # 180° (μs)

    def __init__(self, gpio_pin, pi=None):
        self.pin  = gpio_pin
        self.pi   = pi or pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpio 데몬 미실행. sudo pigpiod 확인!")
        self._angle = 90
        self.angle  = 90

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, deg):
        deg   = max(0, min(180, deg))
        pulse = self.MIN_PULSE + (self.MAX_PULSE - self.MIN_PULSE) * deg / 180
        self.pi.set_servo_pulsewidth(self.pin, int(pulse))
        self._angle = deg

    def smooth_move(self, target, duration=1.0, steps=100):
        start     = self._angle
        step_delay = duration / steps
        for i in range(steps + 1):
            self.angle = start + (target - start) * i / steps
            time.sleep(step_delay)

    def stop(self):
        self.pi.set_servo_pulsewidth(self.pin, 0)

    def cleanup(self):
        self.stop()
        self.pi.stop()


# 사용 예시
pi    = pigpio.pi()
servo = Servo(gpio_pin=18, pi=pi)

try:
    servo.angle = 0
    time.sleep(1)
    servo.angle = 90
    time.sleep(1)
    servo.angle = 180
    time.sleep(1)
    servo.smooth_move(target=0, duration=2.0)
finally:
    servo.cleanup()
