#!/usr/bin/env python3
"""여러 토픽의 발행 주기를 한 화면에 표로 출력한다.

`ros2 topic hz` 는 한 번에 하나씩만 볼 수 있어서, 노드 여러 개의
주기를 동시에 비교하려면 터미널을 그만큼 띄워야 한다. 이 스크립트는
지정한 토픽들을 한꺼번에 구독해 주기를 한 표로 보여준다.

사용법:
    python3 tools/ros2_topic_hz_table.py /mavros/state /mavros/imu/data
"""
import argparse
import sys
import time
from collections import deque

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rosidl_runtime_py.utilities import get_message

WINDOW = 50  # 주기 계산에 사용할 최근 샘플 수


class HzTable(Node):
    def __init__(self, topics: list[str], period: float) -> None:
        super().__init__("ros2_topic_hz_table")
        self._stamps: dict[str, deque[float]] = {t: deque(maxlen=WINDOW) for t in topics}
        self._pending = list(topics)
        self._subs: dict[str, object] = {}
        self.create_timer(period, self._render)
        self.create_timer(1.0, self._try_subscribe)

    def _try_subscribe(self) -> None:
        """아직 타입을 못 알아낸 토픽을 주기적으로 재시도한다."""
        available = dict(self.get_topic_names_and_types())
        still_pending = []
        for topic in self._pending:
            types = available.get(topic)
            if not types:
                still_pending.append(topic)
                continue
            msg_type = get_message(types[0])
            qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
            self._subs[topic] = self.create_subscription(
                msg_type, topic, lambda _msg, t=topic: self._on_msg(t), qos
            )
        self._pending = still_pending

    def _on_msg(self, topic: str) -> None:
        self._stamps[topic].append(time.monotonic())

    @staticmethod
    def _hz(stamps: deque[float]) -> float | None:
        if len(stamps) < 2:
            return None
        span = stamps[-1] - stamps[0]
        return (len(stamps) - 1) / span if span > 0 else None

    def _render(self) -> None:
        width = max(len(t) for t in self._stamps)
        lines = [f"{'TOPIC'.ljust(width)}  {'HZ':>8}  STATUS"]
        lines.append("-" * (width + 20))
        now = time.monotonic()
        for topic, stamps in self._stamps.items():
            hz = self._hz(stamps)
            if topic in self._pending:
                status, shown = "미발견", "-"
            elif hz is None:
                status, shown = "대기중", "-"
            elif now - stamps[-1] > 2.0:
                status, shown = "끊김", f"{hz:.1f}"
            else:
                status, shown = "정상", f"{hz:.1f}"
            lines.append(f"{topic.ljust(width)}  {shown:>8}  {status}")
        print("\033[2J\033[H" + "\n".join(lines), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topics", nargs="+", help="감시할 토픽 이름들")
    parser.add_argument("--period", type=float, default=1.0, help="화면 갱신 주기(초)")
    args = parser.parse_args()

    rclpy.init()
    node = HzTable(args.topics, args.period)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
