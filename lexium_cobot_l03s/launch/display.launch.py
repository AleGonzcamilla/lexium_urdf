
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    pkg_share = get_package_share_directory("lexium_cobot_l03s")

    # ── Paths ────────────────────────────────────────────────────────────────
    default_urdf_xacro = os.path.join(
        pkg_share, "urdf", "lexium_cobot_l03s.urdf.xacro"
    )
    default_rviz_config = os.path.join(
        pkg_share, "rviz", "lexium_cobot_l03s.rviz"
    )

    # ── Declared arguments ───────────────────────────────────────────────────
    urdf_xacro_arg = DeclareLaunchArgument(
        name="urdf_xacro",
        default_value=default_urdf_xacro,
        description="Absolute path to the robot URDF/Xacro file",
    )

    rviz_config_arg = DeclareLaunchArgument(
        name="rviz_config",
        default_value=default_rviz_config,
        description="Absolute path to the RViz2 configuration file",
    )

    use_gui_arg = DeclareLaunchArgument(
        name="use_gui",
        default_value="true",
        description="Start joint_state_publisher_gui instead of joint_state_publisher",
    )

    # ── robot_description ────────────────────────────────────────────────────
    robot_description = ParameterValue(
        Command([
            "xacro",
            LaunchConfiguration("urdf_xacro")
        ]),
        value_type=str
    )

    # ── Nodes ────────────────────────────────────────────────────────────────
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": False,
            }
        ],
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen",
        # Condition: only start when use_gui == "true"
        # (LaunchConfiguration cannot drive a Condition directly without
        #  IfCondition, so we import it here.)
    )

    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", LaunchConfiguration("rviz_config")],
        parameters=[{"use_sim_time": False}],
    )

    return LaunchDescription(
        [
            urdf_xacro_arg,
            rviz_config_arg,
            use_gui_arg,
            robot_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz2_node,
        ]
    )
