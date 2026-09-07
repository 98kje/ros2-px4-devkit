# MAVROS 치트시트

## 연결

```bash
# PX4 SITL
ros2 launch mavros px4.launch fcu_url:=udp://:14540@127.0.0.1:14557

# ArduPilot SITL
ros2 launch mavros apm.launch fcu_url:=udp://:14550@127.0.0.1:14555

# 실기체 (시리얼)
ros2 launch mavros px4.launch fcu_url:=/dev/ttyACM0:921600
```

연결 확인:

```bash
ros2 topic echo /mavros/state --once
# connected: true 여야 함
```

## 핵심 토픽

| 토픽 | 타입 | 용도 |
|---|---|---|
| `/mavros/state` | `mavros_msgs/State` | 연결·아밍·모드 |
| `/mavros/local_position/pose` | `geometry_msgs/PoseStamped` | 로컬 위치 |
| `/mavros/global_position/global` | `sensor_msgs/NavSatFix` | GPS |
| `/mavros/imu/data` | `sensor_msgs/Imu` | IMU |
| `/mavros/battery` | `sensor_msgs/BatteryState` | 배터리 |
| `/mavros/setpoint_position/local` | `geometry_msgs/PoseStamped` | 위치 지령 |
| `/mavros/setpoint_velocity/cmd_vel` | `geometry_msgs/TwistStamped` | 속도 지령 |

## 아밍·모드 전환

```bash
ros2 service call /mavros/cmd/arming mavros_msgs/srv/CommandBool "{value: true}"

ros2 service call /mavros/set_mode mavros_msgs/srv/SetMode \
  "{base_mode: 0, custom_mode: 'OFFBOARD'}"

ros2 service call /mavros/cmd/takeoff mavros_msgs/srv/CommandTOL \
  "{altitude: 10.0}"
```

## OFFBOARD 진입 조건

PX4 는 **setpoint 를 2Hz 이상으로 이미 보내고 있어야** OFFBOARD 를 받아줍니다.
모드 전환 요청 전에 setpoint 를 최소 100회 정도 미리 흘려보내는 것이 정석입니다.

```
setpoint 발행 시작 → (약 1초 대기) → set_mode OFFBOARD → arming
```

순서를 바꾸면 `OFFBOARD` 진입이 거부되거나 즉시 페일세이프로 빠집니다.

## 자주 겪는 문제

| 증상 | 원인 |
|---|---|
| `connected: false` | fcu_url 포트 불일치, 방화벽 |
| 기동 시 GeographicLib 오류 | 데이터셋 미설치 (`setup/install_mavros.sh` 참조) |
| OFFBOARD 거부 | setpoint 스트림 미선행 |
| 위치 토픽 안 나옴 | EKF 미수렴 — GPS/비전 입력 확인 |
