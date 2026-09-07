#!/usr/bin/env bash
# PX4-Autopilot SITL 환경 설치
set -euo pipefail

PX4_DIR="${PX4_DIR:-$HOME/PX4-Autopilot}"
PX4_TAG="${PX4_TAG:-v1.14.3}"

if [[ ! -d "$PX4_DIR" ]]; then
  echo "[1/3] PX4-Autopilot 클론 ($PX4_TAG)"
  git clone --recursive --depth 1 --branch "$PX4_TAG" \
    https://github.com/PX4/PX4-Autopilot.git "$PX4_DIR"
else
  echo "[1/3] 기존 $PX4_DIR 사용"
fi

echo "[2/3] 의존성 설치"
bash "$PX4_DIR/Tools/setup/ubuntu.sh" --no-nuttx

echo "[3/3] SITL 빌드 (gazebo-classic iris)"
make -C "$PX4_DIR" px4_sitl_default

cat <<'MSG'
완료.

SITL 실행:
  make -C ~/PX4-Autopilot px4_sitl gazebo-classic_iris

MAVLink 기본 포트:
  14540 (offboard / MAVSDK), 14550 (GCS)
MSG
