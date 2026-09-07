#!/usr/bin/env bash
# MAVROS(ROS 2) 설치 및 GeographicLib 데이터셋 준비
set -euo pipefail

echo "[1/3] mavros 패키지 설치"
sudo apt-get update -qq
sudo apt-get install -y \
  ros-humble-mavros \
  ros-humble-mavros-extras \
  ros-humble-mavros-msgs

echo "[2/3] GeographicLib 데이터셋 설치"
# 이걸 빼먹으면 mavros 기동 시 지오이드 관련 오류로 죽습니다.
DATASET_URL="https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh"
curl -sSL "$DATASET_URL" -o /tmp/install_geographiclib_datasets.sh
sudo bash /tmp/install_geographiclib_datasets.sh
rm -f /tmp/install_geographiclib_datasets.sh

echo "[3/3] 설치 확인"
ros2 pkg list 2>/dev/null | grep -q '^mavros$' \
  && echo "mavros 등록 확인" \
  || echo "경고: ros2 환경을 source 한 뒤 다시 확인하세요."

cat <<'MSG'
완료.

PX4 SITL 연결:
  ros2 launch mavros px4.launch fcu_url:=udp://:14540@127.0.0.1:14557

ArduPilot SITL 연결:
  ros2 launch mavros apm.launch fcu_url:=udp://:14550@127.0.0.1:14555
MSG
