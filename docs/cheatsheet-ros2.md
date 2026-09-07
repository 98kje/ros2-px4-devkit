# ROS 2 CLI 치트시트

자주 쓰는데 매번 검색하게 되는 것들만 모았습니다.

## 노드·토픽 조사

```bash
ros2 node list                          # 실행 중 노드
ros2 node info /mavros                  # 특정 노드의 pub/sub/서비스 전체
ros2 topic list -t                      # 토픽 + 메시지 타입
ros2 topic echo /mavros/state --once    # 한 번만 받고 종료
ros2 topic hz /mavros/imu/data          # 발행 주기
ros2 topic bw /camera/image_raw         # 대역폭
ros2 topic info /mavros/state -v        # QoS 포함 상세 (불일치 진단용)
```

## QoS 불일치 진단

구독이 안 될 때 8할은 QoS 불일치입니다. `-v` 로 양쪽 프로파일을 비교하세요.

| 발행자 | 구독자 | 결과 |
|---|---|---|
| BEST_EFFORT | RELIABLE | ❌ 연결 안 됨 |
| RELIABLE | BEST_EFFORT | ✅ 연결됨 |
| VOLATILE | TRANSIENT_LOCAL | ❌ 연결 안 됨 |

## 파라미터

```bash
ros2 param list /mavros
ros2 param get /mavros system_id
ros2 param set /mavros system_id 2
ros2 param dump /mavros > mavros_params.yaml
ros2 param load /mavros mavros_params.yaml
```

## 서비스·액션

```bash
ros2 service list -t
ros2 service call /mavros/cmd/arming mavros_msgs/srv/CommandBool "{value: true}"
ros2 action list -t
```

## 기록·재생

```bash
ros2 bag record -a -o run1                    # 전체 토픽
ros2 bag record /mavros/state /tf -o run1     # 지정 토픽만
ros2 bag info run1
ros2 bag play run1 --rate 0.5 --loop
```

## 빌드

```bash
colcon build --symlink-install                       # 파이썬 수정 시 재빌드 불필요
colcon build --packages-select my_pkg                # 특정 패키지만
colcon build --packages-up-to my_pkg                 # 의존성 포함
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release
colcon test --packages-select my_pkg && colcon test-result --verbose
```

## 환경 점검

```bash
echo $ROS_DOMAIN_ID          # 같은 망의 다른 팀과 충돌 시 변경
echo $RMW_IMPLEMENTATION
ros2 doctor --report
```
