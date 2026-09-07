# ros2-px4-devkit

ROS 2 Humble + PX4 / ArduPilot SITL 기반 드론 개발 환경을 빠르게 세팅하고 디버깅하기 위한 스크립트·설정·치트시트 모음입니다.

매번 새 장비에 개발 환경을 다시 깔면서 반복했던 작업들을 정리한 저장소입니다.

## 구성

| 디렉터리 | 내용 |
|---|---|
| `setup/` | 원커맨드 설치 스크립트 (ROS 2, PX4 SITL, ArduPilot SITL, MAVROS) |
| `config/` | DDS 미들웨어 프로파일 (CycloneDDS / FastDDS) |
| `tools/` | 진단용 파이썬 유틸리티 |
| `docs/` | 치트시트 및 트러블슈팅 노트 |
| `templates/` | ROS 2 패키지 스캐폴드 |

## 요구 환경

- Ubuntu 22.04
- ROS 2 Humble
- Python 3.10+

## 시작하기

```bash
git clone https://github.com/98kje/ros2-px4-devkit.git
cd ros2-px4-devkit
./setup/install_ros2_humble.sh
```

## 라이선스

MIT
