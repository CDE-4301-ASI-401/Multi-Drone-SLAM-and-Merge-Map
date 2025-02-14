import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yanyew/Multi-Drone-SLAM-and-Merge-Map/install/ros_gz_crazyflie_control'
