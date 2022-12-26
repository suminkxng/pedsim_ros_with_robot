#! /usr/bin/env python3

import rospy
import dynamic_reconfigure.client


if __name__ == "__main__":
    rospy.init_node("pedsim_toggle_pause")

    client = dynamic_reconfigure.client.Client("pedsim_simulator")
    state = False
    while not rospy.is_shutdown():
        input()
        state = not state
        params = {"paused": state}
        if state:
            rospy.loginfo("Pausing PedSim...")
        else:
            rospy.loginfo("Unpausing PedSim...")
        client.update_configuration(params)
