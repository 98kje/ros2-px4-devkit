#!/usr/bin/env bash
# ROS 2 Humble (Ubuntu 22.04) 설치
set -euo pipefail

if [[ "$(lsb_release -cs)" != "jammy" ]]; then
  echo "이 스크립트는 Ubuntu 22.04(jammy) 전용입니다." >&2
  exit 1
fi

echo "[1/5] 로케일 설정"
sudo apt-get update -qq
sudo apt-get install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

echo "[2/5] 저장소 등록"
sudo apt-get install -y software-properties-common curl gnupg
sudo add-apt-repository -y universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list >/dev/null

echo "[3/5] ros-humble-desktop 설치"
sudo apt-get update -qq
sudo apt-get install -y ros-humble-desktop ros-dev-tools

echo "[4/5] rosdep 초기화"
sudo rosdep init 2>/dev/null || true
rosdep update

echo "[5/5] .bashrc 등록"
grep -qF "source /opt/ros/humble/setup.bash" ~/.bashrc \
  || echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

echo "완료. 새 셸을 열거나 'source /opt/ros/humble/setup.bash' 실행하세요."
