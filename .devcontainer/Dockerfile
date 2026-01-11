FROM osrf/ros:noetic-desktop-full

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-catkin-tools \
    python3-rosdep \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    && rm -rf /var/lib/apt/lists/*

# Setup workspace
WORKDIR /ros_proj

# Copy scripts
COPY .devcontainer/entrypoint.sh /entrypoint.sh
COPY .devcontainer/workspace.sh /workspace.sh
RUN chmod +x /entrypoint.sh /workspace.sh

# Auto-source when entering bash shell
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc && \
    echo "if [ -f /ros_proj/devel/setup.bash ]; then source /ros_proj/devel/setup.bash; fi" >> /root/.bashrc

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
