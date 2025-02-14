import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import yaml


def generate_launch_description():

    # load crazyflies
    crazyflies_yaml = os.path.join(
        get_package_share_directory('crazyflie'),
        'config',
        'crazyflies.yaml')

    with open(crazyflies_yaml, 'r') as ymlfile:
        crazyflies = yaml.safe_load(ymlfile)
    
    # server params
    server_yaml = os.path.join(
        get_package_share_directory('crazyflie'),
        'config',
        'server.yaml')
    with open(server_yaml, 'r') as ymlfile:
        server_yaml_contents = yaml.safe_load(ymlfile)
        
    # server_params = crazyflies
    server_params = [crazyflies] + [server_yaml_contents["/crazyflie_server"]["ros__parameters"]]

    # robot description
    urdf = os.path.join(
        get_package_share_directory('crazyflie'),
        'urdf',
        'crazyflie_description.urdf')
    with open(urdf, 'r') as f:
        robot_desc = f.read()
    server_params[1]['robot_description'] = robot_desc

    # crazyflie_name = '/cf231'
    # pkg_project_crazyswarm2 = get_package_share_directory('crazyflie')
    # crazyflie_real = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([os.path.join(pkg_project_crazyswarm2, 'launch'), '/launch.py']),
    #     launch_arguments={'crazyflies_yaml_file': crazyflies_yaml, 'backend': 'cflib', 'mocap': 'False', 'rviz': 'False'}.items()
    # )

    rviz_config_path = os.path.join(
        get_package_share_directory('crazyflie_ros2_multiranger_bringup'),
        'config',
        'real_mapping.rviz')

    return LaunchDescription([
        # crazyflie_real,
        Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_path],
            parameters=[{
                "use_sim_time": False
            }]
        ),
      # These nodes need https://github.com/IMRCLab/crazyswarm2
        Node(
            package='crazyflie',
            executable='crazyflie_server.py',
            name='crazyflie_server',
            output='screen',
            parameters=server_params,
            #remappings=[
            #    ('/cf09/odom', '/cfcombi/odom'),
            #    ('/cf09/scan', '/cfcombi/scan'),
            #    ('/cf14/odom', '/cfcombi/odom'),
            #    ('/cf14/scan', '/cfcombi/scan'),
            #    ('/cf6/odom', '/cfcombi/odom'),
            #    ('/cf6/scan', '/cfcombi/scan'),
            #]
        ),
        Node(
            package='crazyflie',
            executable='vel_mux.py',
            name='vel_mux',
            output='screen',
            parameters=[{'hover_height': 0.3},
                        {'incoming_twist_topic': '/cf09/cmd_vel'},
                        {'robot_prefix': 'cf09'}]
        ),
        Node(
            package='crazyflie',
            executable='vel_mux.py',
            name='vel_mux',
            output='screen',
            parameters=[{'hover_height': 0.4},
                        {'incoming_twist_topic': '/cf14/cmd_vel'},
                        {'robot_prefix': 'cf14'}]
        ),
        # Node(
        #     package='crazyflie',
        #     executable='vel_mux.py',
        #     name='vel_mux',
        #     output='screen',
        #     parameters=[{'hover_height': 0.5},
        #                 {'incoming_twist_topic': '/cmd_vel'},
        #                 {'robot_prefix': 'cf6'}]
        # ),

        Node(
            package='crazyflie',
            executable='simple_mapper_multiranger.py',
            name='simple_mapper_multiranger',
            output='screen',
            parameters=[
                {'robot_prefix': 'cf09'},
                {'use_sim_time': False},
                {'initial_position': crazyflies['robots']['cf09']['initial_position']}
            ]
        ),
        Node(
            package='crazyflie',
            executable='simple_mapper_multiranger.py',
            name='simple_mapper_multiranger',
            output='screen',
            parameters=[
                {'robot_prefix': 'cf14'},
                {'use_sim_time': False},
                {'initial_position': crazyflies['robots']['cf14']['initial_position']}
            ]
        ),
        # Node(
        #     package='crazyflie',
        #     executable='simple_mapper_multiranger.py',
        #     name='simple_mapper_multiranger',
        #     output='screen',
        #     parameters=[
        #         {'robot_prefix': 'cf6'}]
        # ),
      # these node need: https://github.com/abdulkadrtr/mapMergeForMultiRobotMapping-ROS2
        Node(
            package='merge_map',
            executable='merge_map',
            output='screen',
            parameters=[{'use_sim_time': False}],
            remappings=[
                ("/map1", "/cf09/map"),
                ("/map2", "/cf14/map"),
            ],
        ),
        # Node(
        #     package='merge_map',
        #     executable='merge_map',
        #     output='screen',
        #     remappings=[
        #         ("/map1", "/map12"),
        #         ("/map2", "/cf09/map"),
        #    ],
        # ),
    ])