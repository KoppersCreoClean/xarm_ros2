#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2021, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

import os
import yaml
from ament_index_python import get_package_share_directory
from launch.launch_description_sources import load_python_launch_file_as_module
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def load_file(package_name, *file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, *file_path)

    try:
        with open(absolute_file_path, 'r') as file:
            return file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None

def load_yaml(package_name, *file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, *file_path)

    try:
        with open(absolute_file_path, 'r') as file:
            return yaml.safe_load(file)
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None


def get_xarm_robot_description_parameters(
    xacro_urdf_file=PathJoinSubstitution([FindPackageShare('xarm_description'), 'urdf', 'xarm_device.urdf.xacro']),
    xacro_srdf_file=PathJoinSubstitution([FindPackageShare('xarm_moveit_config'), 'srdf', 'xarm7.srdf.xacro']),
    urdf_arguments={},
    srdf_arguments={},
    arguments={}):
    urdf_arguments['ros2_control_plugin'] = urdf_arguments.get('ros2_control_plugin', 'xarm_control/XArmHW')
    moveit_config_package_name = 'xarm_moveit_config'
    xarm_type = arguments['xarm_type']
    # robot_description
    mod = load_python_launch_file_as_module(os.path.join(get_package_share_directory('xarm_description'), 'launch', 'lib', 'xarm_description_lib.py'))
    get_xacro_file_content = getattr(mod, 'get_xacro_file_content')
    return {
        'robot_description': get_xacro_file_content(
            xacro_file=xacro_urdf_file, 
            arguments=urdf_arguments
        ),
        'robot_description_semantic': get_xacro_file_content(
            xacro_file=xacro_srdf_file,
            arguments=srdf_arguments
        ),
        'robot_description_kinematics': load_yaml(
            moveit_config_package_name, 'config', xarm_type, 'kinematics.yaml'),
        # 'robot_description_planning': load_yaml(
        #     moveit_config_package_name, 'config', xarm_type, 'joint_limits.yaml')
    }