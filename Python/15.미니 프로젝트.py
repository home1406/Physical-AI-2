import rclpy
from rclpy.node import Node
from std_msgs.msg import String
 
class HealthCheckNode(Node):
    def __init__(self):
        super().__init__("health_check")
        self.expected_topics = ["/sensor/dht22", "/cmd/fan"]
        self.last_seen = {t: None for t in self.expected_topics}
        for topic in self.expected_topics:
            self.create_subscription(
                String, topic, self._make_callback(topic), 10)
        self.timer = self.create_timer(5.0, self.check_health)
 
    def _make_callback(self, topic):
        def callback(msg):
            self.last_seen[topic] = self.get_clock().now()
        return callback
 
    def check_health(self):
        now = self.get_clock().now()
        for topic, last in self.last_seen.items():
            if last is None:
                self.get_logger().warn(f"{topic}: 아직 메시지 없음")
            else:
                elapsed = (now - last).nanoseconds / 1e9
                if elapsed > 10:
                    self.get_logger().warn(f"{topic}: {elapsed:.1f}초간 무응답")
 
def main():
    rclpy.init()
    node = HealthCheckNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()
