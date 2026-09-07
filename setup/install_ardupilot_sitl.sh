#!/usr/bin/env bash
# ArduPilot SITL 환경 설치
set -euo pipefail

AP_DIR="${AP_DIR:-$HOME/ardupilot}"
AP_BRANCH="${AP_BRANCH:-Copter-4.5}"

if [[ ! -d "$AP_DIR" ]]; then
  echo "[1/4] ardupilot 클론 ($AP_BRANCH)"
  git clone --recursive --branch "$AP_BRANCH" \
    https://github.com/ArduPilot/ardupilot.git "$AP_DIR"
else
  echo "[1/4] 기존 $AP_DIR 사용"
fi

echo "[2/4] 사전 요구 패키지 설치"
bash "$AP_DIR/Tools/environment_install/install-prereqs-ubuntu.sh" -y

echo "[3/4] 환경변수 반영"
# shellcheck disable=SC1090
source ~/.profile

echo "[4/4] SITL 최초 빌드"
(cd "$AP_DIR" && ./waf configure --board sitl && ./waf copter)

cat <<'MSG'
완료.

SITL 실행:
  cd ~/ardupilot/ArduCopter && sim_vehicle.py -v ArduCopter --console --map

MAVProxy 에서 추가 출력 열기:
  output add 127.0.0.1:14550
MSG
