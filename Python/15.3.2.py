from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import RPi.GPIO as GPIO, rclpy

FAN_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)


class TempController(Node):
    def __init__(self):
        super().__init__("temp_controller")
        self.declare_parameter("high_temp", 28.0)
        self.declare_parameter("low_temp",  25.0)
        self.high   = self.get_parameter("high_temp").value
        self.low    = self.get_parameter("low_temp").value
        self.fan_on = False
        self.sub    = self.create_subscription(
            Float32MultiArray, "/sensor/temperature_humidity",
            self.callback, 10)

    def callback(self, msg):
        temp, hum = msg.data[0], msg.data[1]
        if temp > self.high and not self.fan_on:
            GPIO.output(FAN_PIN, GPIO.HIGH)
            self.fan_on = True
            self.get_logger().warn(f"팬 ON ({temp:.1f}°C)")
        elif temp < self.low and self.fan_on:
            GPIO.output(FAN_PIN, GPIO.LOW)
            self.fan_on = False
            self.get_logger().info(f"팬 OFF ({temp:.1f}°C)")
