#!/usr/bin/env python3
"""
Created on May 25 2023 

@author: suminkxng
"""

import rospy
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import *
from rospkg import RosPack
from pedsim_msgs.msg import AgentStates
from std_msgs.msg import Int64
import time

# xml file containing a gazebo model to represent agent, currently is represented by a cubic but can be changed
global xml_file

actor_id_mapping = {}
spawned_models = []


def actor_poses_callback(actors):
    global actor_id_mapping, spawned_models  # Include spawned_models here
    for actor in actors.agent_states:
        actor_id_simulator = actor.id
        actor_id_gazebo = str(actor_id_simulator)
        actor_id_mapping[actor_id_simulator] = actor_id_gazebo

        # If the model does not exist, spawn it
        if actor_id_gazebo not in spawned_models:
            actor_pose = actor.pose
            rospy.loginfo("Spawning model: actor_id = %s", actor_id_gazebo)

            model_pose = Pose(Point(x=actor_pose.position.x,
                                    y=actor_pose.position.y,
                                    z=actor_pose.position.z),
                              Quaternion(actor_pose.orientation.x,
                                         actor_pose.orientation.y,
                                         actor_pose.orientation.z,
                                         actor_pose.orientation.w))

            spawn_model(actor_id_gazebo, xml_string, "", model_pose, "world")
            spawned_models.append(actor_id_gazebo)


def agent_sink_callback(data):  # Add for delete model
    rospy.loginfo("Received sink event for actor_id = %s", str(data.data))
    global actor_id_mapping, spawned_models
    actor_id_simulator = data.data
    actor_id_gazebo = actor_id_mapping.get(actor_id_simulator, None)

    if actor_id_gazebo is not None and actor_id_gazebo in spawned_models:
        try:
            delete_response = delete_model(actor_id_gazebo)
            if delete_response.success:
                rospy.loginfo("Model %s successfully deleted.",
                              actor_id_gazebo)
                spawned_models.remove(actor_id_gazebo)
            else:
                rospy.loginfo(
                    "Actor ID %s not found in actor_id_dict.", str(data.data))
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s" % e)
    else:
        rospy.loginfo(
            "Actor ID %s not found in actor_id_mapping.", str(data.data))


if __name__ == '__main__':

    rospy.init_node("spawn_pedsim_agents")

    rospack1 = RosPack()
    pkg_path = rospack1.get_path('pedsim_gazebo_plugin')
    default_actor_model_file = pkg_path + "/models/person_walking/model.sdf"

    actor_model_file = rospy.get_param(
        '~actor_model_file', default_actor_model_file)
    file_xml = open(actor_model_file)
    xml_string = file_xml.read()

    print("Waiting for gazebo services...")

    while not rospy.is_shutdown():
        rospy.wait_for_service("gazebo/spawn_sdf_model")
        rospy.wait_for_service("gazebo/delete_model")
        spawn_model = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
        delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)

        print("service: spawn_sdf_model and delete_model are available ....")
        rospy.Subscriber("/pedsim_simulator/simulated_agents",
                         AgentStates, actor_poses_callback)
        rospy.Subscriber("/agent_sink_event", Int64, agent_sink_callback)
        time.sleep(1)
