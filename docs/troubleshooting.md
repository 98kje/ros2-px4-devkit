# 트러블슈팅

실제로 시간을 많이 뺏겼던 것들만 기록합니다.

## 노드끼리 서로 안 보인다

증상: 같은 PC 안에서는 되는데 다른 PC 와는 `ros2 topic list` 결과가 다르다.

점검 순서:

1. **`ROS_DOMAIN_ID` 가 같은가** — 다르면 완전히 격리됩니다.
2. **NIC 가 여러 개인가** — 유선 + 무선 + 도커 브리지가 동시에 뜬 장비에서
   디스커버리가 엉뚱한 인터페이스로 나갑니다. `config/cyclonedds-lan.xml` 로 고정하세요.
3. **멀티캐스트가 차단됐나** — 아래로 확인합니다.

```bash
# 한쪽에서
ros2 multicast receive
# 다른 쪽에서
ros2 multicast send
```

받지 못하면 멀티캐스트가 막힌 것이므로 `config/fastdds-udp.xml` 의 유니캐스트 방식으로 전환합니다.

## 구독이 아예 안 붙는다

발행자는 살아 있는데 콜백이 한 번도 안 불립니다. 대부분 QoS 불일치입니다.

```bash
ros2 topic info /토픽이름 -v
```

발행자가 `BEST_EFFORT` 인데 구독자가 기본값(`RELIABLE`)이면 연결되지 않습니다.
센서·상태 토픽은 대체로 `BEST_EFFORT` 이므로 구독 시 명시해야 합니다.

## colcon build 후에도 예전 코드가 돈다

- `--symlink-install` 없이 빌드하면 파이썬 파일이 복사되므로 수정이 반영되지 않습니다.
- `install/` 에 삭제한 파일이 남아 있을 수 있습니다. 패키지 구조를 바꿨다면
  `build/ install/ log/` 를 지우고 다시 빌드하세요.

```bash
rm -rf build install log && colcon build --symlink-install
```

## mavros 가 기동하자마자 죽는다

GeographicLib 데이터셋 누락이 가장 흔합니다. `setup/install_mavros.sh` 가 이 단계를 포함합니다.

## OFFBOARD 로 전환되지 않는다

PX4 는 setpoint 스트림이 이미 흐르고 있어야 OFFBOARD 를 승인합니다.
`setpoint 발행 시작 → 약 1초 대기 → set_mode → arming` 순서를 지키세요.
자세한 내용은 `docs/cheatsheet-mavros.md` 를 참고하세요.

## SITL 이 뜨자마자 즉시 착륙한다

배터리 시뮬레이션 값이 페일세이프 임계 아래로 잡힌 경우가 많습니다.
SITL 파라미터에서 배터리 페일세이프를 낮추거나 비활성화하세요.
