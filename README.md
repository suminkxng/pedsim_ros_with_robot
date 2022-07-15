# pedsim_with_robot

## Todo List ...

- [X] Humans avoid robot
- [X] Rviz 하나로 합치기
- [ ] 문에서 사람 튀어나옴
- [ ] 코너 너머의 사람이 코너 안쪽으로 코너링
- [ ] etc...


## Requirments
* Ubuntu 20.04 with ROS Noetic and Gazebo11
* [Husky UR3 package](https://github.com/QualiaT/husky_ur3_simulator)


## Sample Usage
* For visualization
```
$ roslaunch pedsim_simulator doors.launch # rviz
$ roslaunch pedsim_gazebo_plugin doors.launch # Gazebo
```
* For control
```
$ roslaunch husky_ur3_gripper_moveit_config Omni_control.launch
$ roslaunch husky_ur3_nav_without_map execution_without_map.launch
```
* **Recommendation**
```
$ roslaunch pedsim_simulator doors_with_Omni.launch
$ roslaunch pedsim_gazebo_plugin doors.launch
$ roslaunch husky_ur3_nav_without_map execution_without_map.launch
```

## Acknowledgement
Part of this simulation is based on:
  * [pedsim_ros](https://github.com/srl-freiburg/pedsim_ros)
  * [ros_maps_to_pedsim](https://github.com/fverdoja/ros_maps_to_pedsim)
