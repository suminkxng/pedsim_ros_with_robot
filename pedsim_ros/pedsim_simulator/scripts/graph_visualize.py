import matplotlib.pyplot as plt
import numpy as np

# 데이터 파일 열기
with open('/home/sumin/simulated_agents.txt', 'r') as f:
    lines = f.readlines()

# 데이터를 numpy array로 변환
data = []
for line in lines:
    split_line = line.strip().split()
    # 각 줄이 '?'을 포함하고 있지 않은지 확인
    if '?' not in split_line and len(split_line) == 4:
        data.append([float(val) for val in split_line])
data = np.array(data)

# ped_id별로 데이터 분리
ped_ids = np.unique(data[:, 1])
ped_data = {ped_id: data[data[:, 1] == ped_id, 2:] for ped_id in ped_ids}

# 각 ped_id에 대한 scatter plot 그리기
plt.figure(figsize=(10, 10))
for ped_id, coords in ped_data.items():
    plt.scatter(coords[:, 0], coords[:, 1], label=f'Ped {ped_id}')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Pedestrian Locations')
plt.legend()
plt.show()
