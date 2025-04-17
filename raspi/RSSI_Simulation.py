import numpy as np
import matplotlib.pyplot as plt

# 圖書館參數
WIDTH, HEIGHT = 50, 30  
NUM_DEVICES = 15  
NUM_SAMPLES = 10000  
P_t = -20  # 發射功率 (dBm)
n = 2.5  # 路徑損耗指數
A = 10  # 環境衰減 (dBm)
NOISE_STD = 3  # 噪聲標準差 (dBm)

def simulate_rssi(pos, device_pos):
    """計算 RSSI（包含噪聲）"""
    distance = np.sqrt(np.sum((pos - device_pos) ** 2))
    if distance < 0.1: 
        distance = 0.1
    rssi = P_t - 10 * n * np.log10(distance) - A
    rssi += np.random.normal(0, NOISE_STD) 
    return rssi

def generate_dataset():
    """生成 RSSI 數據集"""
    data = []
    labels = []
    device_positions = np.random.uniform([0, 0], [WIDTH, HEIGHT], (NUM_DEVICES, 2))
    
    for _ in range(NUM_SAMPLES):
        pos = np.random.uniform([0, 0], [WIDTH, HEIGHT])  
        rssi = np.array([simulate_rssi(pos, dev_pos) for dev_pos in device_positions])
        data.append(rssi)
        labels.append(pos)
    
    return np.array(data), np.array(labels), device_positions


data, labels, device_positions = generate_dataset()

plt.figure(figsize=(10, 6))
plt.scatter(device_positions[:, 0], device_positions[:, 1], c='red', label='BLE Devices', marker='^')
plt.scatter(labels[:100, 0], labels[:100, 1], c='blue', label='User Positions', alpha=0.5)
plt.title('Simulated Library Environment')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.legend()
plt.grid(True)
plt.savefig('library_simulation.png')