# pedsim_ros_with_robot

<p align="center">
 <img src="https://github.com/suminkxng/pedsim_ros_with_robot/assets/87006619/1b972851-a8e6-473e-8a5e-28c91a2f72c7">
</p>

This repository is an enhanced version of the [pedsim_ros](https://github.com/srl-freiburg/pedsim_ros) package, which includes several key additions. The primary addition is the ability to spawn a robot during the pedestrian simulation. This feature supports robots such as the Jackal Kinova and Husky UR3, among others. This integration allows users to simulate interactions between robots and pedestrians, which is essential for a variety of robotics research and applications. 

Please note that this package retains all of the original [pedsim_ros](https://github.com/srl-freiburg/pedsim_ros) package's features. The ability to spawn robots is implemented in a way that complements and extends the existing pedestrian simulation capabilities without compromising them. Feel free to explore this enriched pedestrian-robot interactive simulation!    


## Requirments
* Ubuntu 20.04 with ROS Noetic and Gazebo11
* [Husky UR3 package](https://github.com/QualiaT/husky_ur3_simulator)
* [Jackal Kinova package](https://github.com/Sungwwoo/jackal_kinova_simulator)    

## Sample Usage
* For visualization
```
$ roslaunch pedsim_simulator demo.launch # rviz
$ roslaunch pedsim_gazebo_plugin demo.launch # Gazebo
```
* For control
```
$ roslaunch husky_ur3_gripper_moveit_config Omni_control.launch
$ roslaunch husky_ur3_nav_without_map execution_without_map.launch
```    

## Acknowledgement
Part of this simulation is based on:
  * [pedsim_ros](https://github.com/srl-freiburg/pedsim_ros)
  * [ros_maps_to_pedsim](https://github.com/fverdoja/ros_maps_to_pedsim)
