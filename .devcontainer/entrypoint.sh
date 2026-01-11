#!/bin/bash
set -e

# Source ROS Noetic
source /opt/ros/noetic/setup.bash

# Source workspace nếu đã build
if [ -f /ros_proj/devel/setup.bash ]; then
    echo "[Entrypoint] Sourcing catkin workspace"
    source /ros_proj/devel/setup.bash
fi

# Source script tùy chọn của bạn
if [ -f /ros_proj/workspace.sh ]; then
    echo "[Entrypoint] Sourcing workspace.sh"
    source /ros_proj/workspace.sh
fi

exec "$@"
