# L298N 연결:
# ENA → GPIO12 (PWM)  ENB → GPIO13 (PWM)
# IN1 → GPIO20        IN2 → GPIO21
# IN3 → GPIO19        IN4 → GPIO26
# VCC → 배터리 양극 (7.4V~12V)
# GND → 배터리 음극 + 라즈베리파이 GND
# 주의: 라즈베리파이 5V → L298N VCC 연결 금지!
import RPi.GPIO as GPIO, time

class DCMotor:
    def __init__(self, en, in1, in2, freq=1000):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([en, in1, in2], GPIO.OUT)
        self.in1 = in1
        self.in2 = in2
        self.pwm = GPIO.PWM(en, freq)
        self.pwm.start(0)

    def forward(self, speed=70):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(max(0, min(100, speed)))

    def backward(self, speed=70):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(max(0, min(100, speed)))

    def coast(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)


class MiniCar:
    def __init__(self):
        self.left  = DCMotor(12, 20, 21)
        self.right = DCMotor(13, 19, 26)

    def forward(self, speed=70):
        self.left.forward(speed)
        self.right.forward(speed)

    def backward(self, speed=70):
        self.left.backward(speed)
        self.right.backward(speed)

    def turn_left(self, speed=70, ratio=0.4):
        self.left.forward(int(speed * ratio))
        self.right.forward(speed)

    def turn_right(self, speed=70, ratio=0.4):
        self.left.forward(speed)
        self.right.forward(int(speed * ratio))

    def stop(self):
        self.left.coast()
        self.right.coast()

    def cleanup(self):
        self.stop()
        GPIO.cleanup()


# 동작 테스트
car = MiniCar()
try:
    car.forward(70);    time.sleep(2)
    car.turn_right(70); time.sleep(1)
    car.forward(70);    time.sleep(2)
    car.stop()
finally:
    car.cleanup()
