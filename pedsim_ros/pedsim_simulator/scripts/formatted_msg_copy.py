#!/usr/bin/env python3

# for training data
import rospy
from leg_tracker.msg import PersonArray

# 각 agent 별로 저장된 데이터 수를 추적하는 딕셔너리
agent_data_count = {}

# 이전 secs 값을 추적하기 위한 변수 초기화
prev_secs = None

# 첫 번째 secs 값을 추적하기 위한 변수 초기화
first_secs = None

# ROS 메시지 콜백 함수 정의


def callback(data):
    global prev_secs, first_secs

    # data.header.stamp.secs가 변경되었는지 확인
    # if prev_secs is None or data.header.stamp.secs != prev_secs:
    #     prev_secs = data.header.stamp.secs

    #     # 첫 번째 secs 값 기록
    #     if first_secs is None:
    #         first_secs = prev_secs

    # 파일을 한번만 열기 위해 'with' 문 밖에서 for 문을 시작합니다.
    with open('0621_input.txt', 'a') as f:
        # frame_number = (data.header.stamp.secs - first_secs) * 10 + 10
        frame_number = data.header.seq

        for agent_state in data.people:
            # 메시지에서 필요한 정보를 추출
            ped_id = agent_state.id

            # if agent_data_count.get(ped_id, 0) >= 14:
            #     x_coord = '?'
            #     y_coord = '?'

            # 이미 20개의 데이터가 저장되었다면 무시
            if agent_data_count.get(ped_id, 0) >= 20:
                continue

            x_coord = agent_state.position.x
            y_coord = agent_state.position.y

            # 추출한 정보를 원하는 형식의 문자열로 변환
            formatted_message = f"{frame_number} {ped_id} {y_coord} {x_coord}\n"

            # 변환된 메시지를 파일에 기록
            f.write(formatted_message)

            # 해당 agent의 데이터 카운트 증가
            agent_data_count[ped_id] = agent_data_count.get(ped_id, 0) + 1


# ROS 노드 초기화
rospy.init_node('message_converter', anonymous=True)

# 토픽 구독
rospy.Subscriber("people", PersonArray, callback)

# spin()은 콜백이 호출될 때까지 노드를 유지합니다.
rospy.spin()
