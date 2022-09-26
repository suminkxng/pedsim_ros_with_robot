#! /usr/bin/env python3

import time
import rospy
import tf2_ros
import sys
from actionlib import SimpleActionClient
from pedsim_msgs.msg import TrackedPersons
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from moveit_msgs.msg import DisplayTrajectory
from moveit_commander import RobotCommander, PlanningSceneInterface, MoveGroupCommander, roscpp_initialize


def getTF(target_frame, source_frame):

    while True:
        try:
            trans = tfBuffer.lookup_transform(target_frame, source_frame, rospy.Time())
            return trans
        except:
            rospy.sleep(1)
            continue


if __name__ == "__main__":
    roscpp_initialize(sys.argv)
    rospy.init_node("move_base_example", anonymous=True, disable_signals=True)

    # tf listner
    tfBuffer = tf2_ros.Buffer()
    tfListner = tf2_ros.TransformListener(tfBuffer)

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
    pub_display_trajectory = rospy.Publisher("/move_group/display_planned_path", DisplayTrajectory, queue_size=20)
    planning_frame = group.get_planning_frame()

    # targetX, targetY = 6, 12
    target_X = rospy.get_param("~target_X", 6)
    target_Y = rospy.get_param("~target_Y", 12)
    theta = 0
    base_goal_quat = quaternion_from_euler(0, 0, theta)

    # group.go(group.get_named_target_values("up"), wait=False)
    print("Moving to ", target_X, target_Y)
    base_goal = MoveBaseGoal()
    base_goal.target_pose.header.frame_id = "odom"
    base_goal.target_pose.header.stamp = rospy.Time.now()
    base_goal.target_pose.pose.position.x = target_X
    base_goal.target_pose.pose.position.y = target_Y
    base_goal.target_pose.pose.position.z = 0
    base_goal.target_pose.pose.orientation.x = base_goal_quat[0]
    base_goal.target_pose.pose.orientation.y = base_goal_quat[1]
    base_goal.target_pose.pose.orientation.z = base_goal_quat[2]
    base_goal.target_pose.pose.orientation.w = base_goal_quat[3]

    robot_log, human_log = [], []
    start = rospy.Time.now()
    client.send_goal(base_goal)

    while not client.wait_for_result(timeout=rospy.Duration(0.5)):
        loc = getTF("map", "base_link")

        robot_log.append(str(loc.transform.translation.x) + "\t" + str(loc.transform.translation.y) + "\n")

        try:
            ploc = rospy.wait_for_message("/pedsim_visualizer/tracked_persons", TrackedPersons, 0.1)
        except:
            print(end="")

        try:

            human_log.append(str(ploc.tracks[0].pose.pose.position.x) + "\t" + str(ploc.tracks[0].pose.pose.position.y) + "\n")
        except:
            print(end="")
    end = rospy.Time.now()
    cost = (end - start).to_sec()
    lctime = time.localtime(time.time())
    sim_name = "{0}{1}{2}-{3}{4}{5}".format(lctime[0], lctime[1], lctime[2], lctime[3], lctime[4], lctime[5])
    robot_file = open("../catkin_ws/" + sim_name + "_robot.txt", "w")
    human_file = open("../catkin_ws/" + sim_name + "_human.txt", "w")

    for line in robot_log:
        robot_file.write(line)
    robot_file.write("Robot cost: " + str(cost))
    for line in human_log:
        human_file.write(line)
    human_file.write("Robot cost: " + str(cost))
    rospy.loginfo("Took " + str(cost) + "sec.")
    robot_file.close()
    human_file.close()
    exit()