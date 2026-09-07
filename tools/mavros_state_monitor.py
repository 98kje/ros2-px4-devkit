#!/usr/bin/env python3
"""MAVROS 연결·아밍·비행모드 상태를 한 줄로 계속 출력한다.

SITL 이나 실기체를 붙였을 때 "왜 OFFBOARD 로 안 들어가지"를 확인하려면
연결 여부, 아밍 상태, 현재 모드, 배터리를 동시에 봐야 한다.

사용법:
    python3 tools/mavros_state_monitor.py
    python3 tools/mavros_state_monitor.py --ns /uav1
"""
import argparse
import sys

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

from mavros_msgs.msg import State
from sensor_msgs.msg import BatteryState

# MAVROS 상태 토픽은 TRANSIENT_LOCAL + BEST_EFFORT 로 발행된다.
SENSOR_QOS = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
)


class StateMonitor(Node):
    def __init__(self, ns: str) -> None:
        super().__init__("mavros_state_monitor")
        self._state: State | None = None
        self._battery: BatteryState | None = None

        self.create_subscription(State, f"{ns}/state", self._on_state, SENSOR_QOS)
        self.create_subscription(
            BatteryState, f"{ns}/battery", self._on_battery, SENSOR_QOS
        )
        self.create_timer(0.5, self._render)

    def _on_state(self, msg: State) -> None:
        self._state = msg

    def _on_battery(self, msg: BatteryState) -> None:
        self._battery = msg

    def _render(self) -> None:
        if self._state is None:
            print("\r상태 토픽 대기중...", end="", flush=True)
            return

        conn = "연결" if self._state.connected else "끊김"
        armed = "ARMED" if self._state.armed else "DISARMED"
        mode = self._state.mode or "-"

        if self._battery is not None and self._battery.percentage >= 0:
            batt = f"{self._battery.percentage * 100:5.1f}%"
        else:
            batt = "  -  "

        print(
            f"\r{conn:>4} | {armed:<8} | mode={mode:<12} | batt={batt}",
            end="",
            flush=True,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ns", default="/mavros", help="MAVROS 네임스페이스")
    args = parser.parse_args()

    rclpy.init()
    node = StateMonitor(args.ns.rstrip("/"))
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print()
    finally:
        node.destroy_node()
        rclpy.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
