import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
 
class DynamicThresholdNode(Node):
    def __init__(self):
        super().__init__("dynamic_threshold")
        self.declare_parameter("threshold", 28.0)
        self.threshold = self.get_parameter("threshold").value
        self.add_on_set_parameters_callback(self.on_param_change)
        self.get_logger().info(f"초기 임계값: {self.threshold}")
 
    def on_param_change(self, params):
        for p in params:
            if p.name == "threshold":
                if p.value < 0:
                    return SetParametersResult(
                        successful=False, reason="threshold는 0 이상이어야 함")
                self.threshold = p.value
                self.get_logger().info(f"임계값이 {self.threshold}로 변경됨")
        return SetParametersResult(successful=True)
 
def main():
    rclpy.init()
    node = DynamicThresholdNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()
 
# 터미널에서: ros2 param set /dynamic_threshold threshold 32.0
