#!/bin/bash
source /opt/ros/noetic/setup.bash

cd /ros_proj
catkin_make

source devel/setup.bash
echo "Build done!"
