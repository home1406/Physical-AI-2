"""dht22_publisher.py — DHT22를 ROS2 토픽으로 발행"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import board, adafruit_dht, time


class DHT22Publisher(Node):
    def __init__(self):
        super().__init__("dht22_publisher")
        self.declare_parameter("interval", 5.0)
        interval     = self.get_parameter("interval").value
        self.sensor  = adafruit_dht.DHT22(board.D4)
        self.pub     = self.create_publisher(
            Float32MultiArray, "/sensor/temperature_humidity", 10)
        self.timer   = self.create_timer(interval, self.publish_callback)
        self.get_logger().info(f"DHT22 Publisher 시작 (간격: {interval}초)")

    def publish_callback(self):
        try:
            temp = self.sensor.temperature
            hum  = self.sensor.humidity
            if temp and hum:
                msg      = Float32MultiArray()
                msg.data = [float(temp), float(hum)]
                self.pub.publish(msg)
                self.get_logger().info(f"발행: {temp:.1f}°C  {hum:.1f}%")
        except RuntimeError:
            self.get_logger().warn("DHT22 읽기 실패")


def main(args=None):
    rclpy.init(args=args)
    node = DHT22Publisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
