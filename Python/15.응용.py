from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
 
def generate_launch_description():
    threshold_arg = DeclareLaunchArgument(
        "temp_threshold", default_value="28.0",
        description="팬이 켜지는 온도 임계값(°C)"
    )
 
    publisher_node = Node(
        package="pai_sensors",
        executable="dht22_publisher",
        name="dht22_publisher",
        output="screen",
    )
 
    subscriber_node = Node(
        package="pai_sensors",
        executable="fan_controller",
        name="fan_controller",
        output="screen",
        parameters=[{"threshold": LaunchConfiguration("temp_threshold")}],
    )
 
    return LaunchDescription([
        threshold_arg,
        publisher_node,
        subscriber_node,
    ])
 
# 실행: ros2 launch pai_sensors sensor_fan.launch.py temp_threshold:=30.0
