import os
from glob import glob

from setuptools import setup

package_name = "ros2_python_pkg"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        # launch/config 를 빼먹으면 설치 후 파일을 못 찾는다.
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="your name",
    maintainer_email="you@example.com",
    description="ament_python 패키지 스캐폴드",
    license="MIT",
    entry_points={
        "console_scripts": [
            "example_node = ros2_python_pkg.example_node:main",
        ],
    },
)
