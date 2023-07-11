def process_and_remove_invalid_data(input_file, output_file):
    # 파일 불러오기
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # 데이터 처리
    agent_data = {}
    for line in lines:
        values = line.split()
        agent_id = values[1]

        # 각 숫자를 소수점 둘째 자리까지 반올림합니다.
        for i in range(2, len(values)):  # 첫 두 숫자를 제외하고 시작합니다.
            # check if it is a number
            if values[i].lstrip('-').replace('.', '', 1).isdigit():
                values[i] = str(round(float(values[i]), 3))

        # 마지막 5줄의 3번째와 4번째 값을 '?'로 변경합니다.
        if len(agent_data.get(agent_id, [])) >= 15:
            values[2] = '?'
            values[3] = '?'

        line = ' '.join(values) + '\n'

        if agent_id not in agent_data:
            agent_data[agent_id] = []
        agent_data[agent_id].append(line)

    # 20개 이상인 agent_id만 선택하여 유효한 데이터로 구성
    valid_data = []
    for agent_id, data in agent_data.items():
        if len(data) == 20:
            valid_data.extend(data)

    # 각 라인을 첫 번째 값(즉, id)를 기준으로 정렬합니다. 이때, id는 소수점이 있는 경우 float로 변환하고, 그렇지 않으면 int로 변환합니다.
    valid_data.sort(key=lambda x: float(x.split()[1]))  # 첫 번째 값으로 정렬합니다.

    # 파일 저장
    with open(output_file, 'w') as file:
        file.writelines(valid_data)


input_file = '/home/sumin/0620_input.txt'
output_file = '/home/sumin/0620_output_3.txt'
process_and_remove_invalid_data(input_file, output_file)
