import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    controller_yaml = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'controller.yaml')
    bt_navigator_yaml = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'bt_navigator.yaml')
    planner_yaml = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'planner_server.yaml')
    recovery_yaml = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'recovery.yaml')
    filters_yaml = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'filter.yaml')
    # RVIZ configuration file
    rviz_file = "pathplanning.rviz"
    rviz_config_dir = os.path.join(get_package_share_directory("path_planner_server"), "rviz", rviz_file)


    
    return LaunchDescription([     
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            remappings=[('/cmd_vel', '/diffbot_base_controller/cmd_vel_unstamped')],
            parameters=[controller_yaml]),

        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            remappings=[('/cmd_vel', '/diffbot_base_controller/cmd_vel_unstamped')],
            parameters=[planner_yaml]),
            
        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            parameters=[recovery_yaml],
            output='screen'),

        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[bt_navigator_yaml]),

        Node(
            package='nav2_map_server',
            executable='map_server',
            name='filter_mask_server',
            output='screen',
            emulate_tty=True,
            parameters=[filters_yaml]),

        Node(
            package='nav2_map_server',
            executable='costmap_filter_info_server',
            name='costmap_filter_info_server',
            output='screen',
            emulate_tty=True,
            parameters=[filters_yaml]),

        Node(
            package="rviz2",
            executable="rviz2",
            output="screen",
            parameters=[{"use_sim_time": True}],
            arguments=["-d", rviz_config_dir]),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_pathplanner',
            output='screen',
            parameters=[{'autostart': True},
                        {'node_names': ['planner_server',
                                        'controller_server',
                                        'behavior_server',
                                        'bt_navigator', 'filter_mask_server','costmap_filter_info_server']}])
    ])