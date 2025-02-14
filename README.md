# Multi-Drone-SLAM-and-Merge-Map
This repository provides a multi-robot SLAM solution for Crazyflie drones, including real-time mapping and map fusion using ROS 2.


## Getting Started



### Clone the Repository

```bash
git clone https://github.com/CDE-4301-ASI-401/Multi-Drone-SLAM-and-Merge-Map.git
cd ~/Multi-Drone-SLAM-and-Merge-Map
```

### Build the Workspace

```bash
colcon build
```

> **Note:** Building some packages (especially Crazyswarm2) might display a lot of warnings and messages on stderr. As long as the build completes without any errors (i.e., no package fails to build), the workspace is good to go.

---

## Usage

### Source the Workspace

Before running any nodes, source your workspace:

```bash
source ~/Multi-Drone-SLAM-and-Merge-Map/install/setup.bash
```

### Launch Nodes

#### Terminal A: Launch Crazyswarm2 and SLAM Node

```bash
ros2 launch crazyflie_launch swarm_mapping.launch.py
```

#### Terminal B: Launch MergeMap Node to View the Merged Map

```bash
ros2 launch merge_map merge_map_launch.py
```

#### [Optional] Terminal C: Teleoperate Drones

To control each drone independently, use the teleop twist keyboard and remap the command topic. For example, to control the `cf09` drone:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cf09/cmd_vel
```

For `cf14`, run in a separate terminal:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cf14/cmd_vel
```

---

## Setting Up the Drones

### Configuration in `crazyflies.yaml`

Make sure your `crazyflies.yaml` file (typically located in `src/crazyswarm2/crazyflie/config/crazyflies.yaml`) is configured correctly and that each drone is enabled. For example:

```yaml
robots:
  cf09:
    enabled: true
    uri: radio://0/60/2M/E7E7E7E735
    initial_position: [0, 0.0, 0.0]
    type: cf21  # see robot_types
  cf14:
    enabled: true
    uri: radio://0/60/2M/E7E7E7E714
    initial_position: [1.23, -3.14, 0.0]
    type: cf21  # see robot_types
```

### Updating the Launch File if the Drone List Changes

If you modify the drone list in `crazyflies.yaml`, you'll also need to update the launch file accordingly. For example, in your launch file located at:

```
~/Multi-Drone-SLAM-and-Merge-Map/src/crazyflie_launch/launch/swarm_mapping.launch.py
```

ensure you update the parameters for the `vel_mux` and mapping nodes. For example:

#### Create a vel_mux node for cf09

```python
Node(
    package='crazyflie',
    executable='vel_mux.py',
    name='vel_mux_cf09',
    output='screen',
    parameters=[
        {'hover_height': 0.3},
        {'incoming_twist_topic': '/cf09/cmd_vel'},
        {'robot_prefix': 'cf09'}
    ]
),
```

#### Create a simple mapper node for cf09

```python
Node(
    package='crazyflie',
    executable='simple_mapper_multiranger.py',
    name='simple_mapper_cf09',
    output='screen',
    parameters=[
        {'robot_prefix': 'cf09'},
        {'use_sim_time': False},
        {'initial_position': crazyflies['robots']['cf09']['initial_position']}
    ]
),
```

#### Create the MergeMap node

```python
Node(
    package='merge_map',
    executable='merge_map',
    name='merge_map_node',
    output='screen',
    parameters=[{'use_sim_time': False}],
    remappings=[
        ("/map1", "/cf09/map"),
        ("/map2", "/cf14/map"),
    ],
),
```

---
