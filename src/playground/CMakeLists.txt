cmake_minimum_required(VERSION 3.0.2)
project(playground)

find_package(catkin REQUIRED COMPONENTS
  rospy
  roscpp
  std_msgs
  sensor_msgs
  nav_msgs
  geometry_msgs
  gazebo_ros
  gazebo_plugins
  xacro
  cv_bridge
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

# Install Python scripts
catkin_install_python(PROGRAMS
  src/sensor_reader.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# Install launch files
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

# Install world files
install(DIRECTORY worlds/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/worlds
)

# Install URDF files
install(DIRECTORY urdf/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/urdf
)