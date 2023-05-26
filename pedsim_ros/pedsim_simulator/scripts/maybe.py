#! /usr/bin/env python3

import rospy
import sys
from actionlib import SimpleActionClient
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from moveit_msgs.msg import DisplayTrajectory
from moveit_commander import RobotCommander, PlanningSceneInterface, MoveGroupCommander, roscpp_initialize


if __name__ == "__main__":
    roscpp_initialize(sys.argv)
    rospy.init_node("move_base_example", anonymous=True, disable_signals=True)
    client = SimpleActionClient("move_base", MoveBaseAction)
    client.wait_for_server()

    # move_group configuration
    robot = RobotCommander()
    scene = PlanningSceneInterface()

    group_name = "ur3_manipulator"
    group = MoveGroupCommander(group_name)
    # Must be specified for regular manipulation speed
    group.set_max_velocity_scaling_factor(1.0)
    group.set_max_acceleration_scaling_factor(1.0)
    pub_display_trajectory = rospy.Publisher(
        "/move_group/display_planned_path", DisplayTrajectory, queue_size=20)
    planning_frame = group.get_planning_frame()

    # targetX, targetY = 17, 0
    targetX, targetY = 17, -1
    theta = 0
    base_goal_quat = quaternion_from_euler(0, 0, theta)

    group.go(group.get_named_target_values("default"), wait=False)
    print("Moving to ", targetX, targetY)
    base_goal = MoveBaseGoal()
    base_goal.target_pose.header.frame_id = "odom"
    base_goal.target_pose.header.stamp = rospy.Time.now()
    base_goal.target_pose.pose.position.x = targetX
    base_goal.target_pose.pose.position.y = targetY
    base_goal.target_pose.pose.position.z = 0
    base_goal.target_pose.pose.orientation.x = base_goal_quat[0]
    base_goal.target_pose.pose.orientation.y = base_goal_quat[1]
    base_goal.target_pose.pose.orientation.z = base_goal_quat[2]
    base_goal.target_pose.pose.orientation.w = base_goal_quat[3]

    client.send_goal(base_goal)
    # group.go(group.get_named_target_values("default"), wait=False)
