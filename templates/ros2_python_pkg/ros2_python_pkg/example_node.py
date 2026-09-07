#!/usr/bin/env python3
"""최소 구성 퍼블리셔 노드."""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ExampleNode(Node):
    def __init__(self) -> None:
        super().__init__("example_node")
        self.declare_parameter("period", 1.0)
        period = self.get_parameter("period").value

        self._pub = self.create_publisher(String, "chatter", 10)
        self._count = 0
        self.create_timer(period, self._tick)
        self.get_logger().info(f"example_node 시작 (period={period}s)")

    def _tick(self) -> None:
        msg = String()
        msg.data = f"hello {self._count}"
        self._pub.publish(msg)
        self._count += 1


def main() -> None:
    rclpy.init()
    node = ExampleNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
