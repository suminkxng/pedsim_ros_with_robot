#!/usr/bin/env python3
# for test data

import rospy
# from pedsim_msgs.msg import AgentStates
from leg_tracker.msg import Person, PersonArray

# 각 agent 별로 저장된 데이터 수를 추적하는 딕셔너리
agent_data_count = {}

# ROS 메시지 콜백 함수 정의


def callback(data):
    # 파일을 한번만 열기 위해 'with' 문 밖에서 for 문을 시작합니다.
    with open('people_input2.txt', 'a') as f:
        frame_number = data.header.seq

        if frame_number % 10 != 0:  # frame_number가 10의 배수가 아닌 경우 건너뜁니다.
            return

        for person in data.people:
            # 메시지에서 필요한 정보를 추출
            # frame_number = data.header.stamp.secs
            ped_id = person.id

            # 이미 30개의 데이터가 저장되었다면 무시
            if agent_data_count.get(ped_id, 0) >= 20:
                continue
            x_coord = person.position.x
            y_coord = person.position.y

            # 추출한 정보를 원하는 형식의 문자열로 변환
            # formatted_message = f"{frame_number}\n{ped_id}\n{y_coord}\n{x_coord}\n"
            # 모든 정보를 한 줄에 나열
            formatted_message = f"{frame_number} {ped_id} {y_coord} {x_coord}\n"

            # 변환된 메시지를 파일에 기록
            f.write(formatted_message)

            agent_data_count[ped_id] = agent_data_count.get(ped_id, 0) + 1


# ROS 노드 초기화
rospy.init_node('message_converter', anonymous=True)

# 토픽 구독
rospy.Subscriber("people", PersonArray, callback)

# spin()은 콜백이 호출될 때까지 노드를 유지합니다.
rospy.spin()
