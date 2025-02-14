import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yanyew/Multi-Drone-SLAM-and-Merge-Map/install/crazyflie_ros2_multiranger_simple_mapper'
