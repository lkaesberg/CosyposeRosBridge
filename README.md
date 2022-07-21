# Cosypose ROS Bridge

Provide compressed images to cosypose and publish the 6D pose

## Download
```
git clone https://github.com/lkaesberg/CosyposeRosBridge.git
cd cosypose_ros_bridge
```
## Build
```
colcon build --packages-select cosypose_ros_bridge
```

## Installation
```
. install/setup.bash
```

## Usage
```
ros2 run cosypose_ros_bridge cosypose_ros_bridge topic1 topic2 ...
```