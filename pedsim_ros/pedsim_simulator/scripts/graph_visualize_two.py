import matplotlib.pyplot as plt
import numpy as np

# 파일 경로 설정
file_path1 = '/home/sumin/0620_output_3.txt'  # 첫 번째 파일 경로
file_path2 = '/home/sumin/catkin_ws/src/social-lstm/result/SOCIALLSTM/LSTM/pedsim/0620_output.txt'  # 두 번째 파일 경로

# 두 텍스트 파일을 열고 내용을 읽음
with open(file_path1, 'r') as f:
    data_text1 = f.read()

with open(file_path2, 'r') as f:
    data_text2 = f.read()

# 두 데이터를 한꺼번에 처리하기 위해 리스트에 넣음
data_texts = [data_text1, data_text2]

plt.figure(figsize=(10, 10))

# 파일 이름 지정
file_names = ['Ground Truth', 'Predicted']

# 두 데이터에 대해 같은 처리를 반복
for data_index, data_text in enumerate(data_texts):
    # 줄별로 데이터 분리
    lines = data_text.strip().split('\n')

    # 데이터를 numpy array로 변환
    data = []
    for line in lines:
        split_line = line.strip().split()
        if '?' not in split_line:  # 각 줄이 '?'를 포함하고 있는지 확인
            data.append([float(val) for val in split_line])
    data = np.array(data)

    # ped_id별로 데이터 분리
    ped_ids = np.unique(data[:, 1])
    ped_data = {ped_id: data[data[:, 1] == ped_id, 2:] for ped_id in ped_ids}

    # 각 ped_id에 대한 scatter plot 그리기
    for ped_id, coords in ped_data.items():
        if file_names[data_index] == 'Ground Truth':
            plt.plot(coords[:, 0], coords[:, 1], linestyle='dotted',
                     label=f'{file_names[data_index]}, Ped {ped_id}')
        else:
            plt.scatter(coords[:, 0], coords[:, 1],
                        label=f'{file_names[data_index]}, Ped {ped_id}')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Pedestrian Locations')
plt.legend()
plt.show()
