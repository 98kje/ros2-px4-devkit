from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    period = LaunchConfiguration("period")

    return LaunchDescription([
        DeclareLaunchArgument("period", default_value="1.0"),
        Node(
            package="ros2_python_pkg",
            executable="example_node",
            name="example_node",
            output="screen",
            parameters=[{"period": period}],
        ),
    ])
