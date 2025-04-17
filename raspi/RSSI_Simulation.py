import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 圖書館參數
WIDTH, HEIGHT = 50, 30  # 圖書館尺寸（米）
NUM_DEVICES = 15  # 藍芽裝置數量
NUM_SAMPLES = 100000  # 訓練數據樣本數
P_t = -20  # 發射功率 (dBm)
n = 2.5  # 路徑損耗指數
A = 10  # 環境衰減 (dBm)
NOISE_STD = 3  # 噪聲標準差 (dBm)

def simulate_rssi(pos, device_pos):
    """計算 RSSI（包含噪聲）"""
    distance = np.sqrt(np.sum((pos - device_pos) ** 2))
    if distance < 0.1:  # 避免除零
        distance = 0.1
    rssi = P_t - 10 * n * np.log10(distance) - A
    rssi += np.random.normal(0, NOISE_STD)
    return rssi

def generate_dataset(num_samples):
    """生成 RSSI 數據集"""
    device_positions = np.random.uniform([0, 0], [WIDTH, HEIGHT], (NUM_DEVICES, 2))
    data = []
    labels = []
    for _ in range(num_samples):
        pos = np.random.uniform([0, 0], [WIDTH, HEIGHT])
        rssi = np.array([simulate_rssi(pos, dev_pos) for dev_pos in device_positions])
        data.append(rssi)
        labels.append(pos)
    return np.array(data), np.array(labels), device_positions

def train_cnn_model(data, labels):
    """訓練 CNN 模型"""
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    data_reshaped = data_scaled.reshape(-1, 5, 3, 1)  # 假設 15 個裝置，組織為 5x3

    X_train, X_val, y_train, y_val = train_test_split(data_reshaped, labels, test_size=0.2, random_state=42)

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(5, 3, 1), padding='same'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(2)  # 輸出 (x, y) 座標
    ])

    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50, batch_size=32, verbose=0)
    
    return model, scaler

def simulate_user_path(num_points=100):
    """模擬用戶移動路徑（例如沿曲線移動）"""
    t = np.linspace(0, 2 * np.pi, num_points)
    x = 25 + 15 * np.cos(t)  # 橢圓路徑
    y = 15 + 10 * np.sin(t)
    return np.vstack((x, y)).T

def predict_user_path(model, scaler, path, device_positions):
    """使用 CNN 預測用戶位置"""
    rssi_data = np.array([simulate_rssi(pos, device_pos) for pos in path for device_pos in device_positions])
    rssi_data = rssi_data.reshape(len(path), NUM_DEVICES)
    rssi_scaled = scaler.transform(rssi_data)
    rssi_reshaped = rssi_scaled.reshape(-1, 5, 3, 1)
    predictions = model.predict(rssi_reshaped, verbose=0)
    return predictions

def plot_results(actual_path, predicted_path, device_positions):
    """繪製實際和預測位置圖表"""
    plt.figure(figsize=(12, 8))
    # 繪製藍芽裝置
    plt.scatter(device_positions[:, 0], device_positions[:, 1], c='red', marker='^', s=100, label='BLE Devices')
    # 繪製實際路徑
    plt.plot(actual_path[:, 0], actual_path[:, 1], 'b-', label='Actual Path')
    # 繪製預測路徑
    plt.plot(predicted_path[:, 0], predicted_path[:, 1], 'r--', label='Predicted Path')
    # 設置圖表
    plt.title('Actual vs Predicted User Path in Library')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, WIDTH)
    plt.ylim(0, HEIGHT)
    plt.savefig('location_prediction.png')
    plt.close()

# 主程序
if __name__ == "__main__":
    # 生成訓練數據
    data, labels, device_positions = generate_dataset(NUM_SAMPLES)
    
    # 訓練 CNN 模型
    model, scaler = train_cnn_model(data, labels)
    
    # 模擬用戶移動路徑
    actual_path = simulate_user_path()
    
    # 預測用戶位置
    predicted_path = predict_user_path(model, scaler, actual_path, device_positions)
    
    # 繪製結果
    plot_results(actual_path, predicted_path, device_positions)
    
    # 計算平均定位誤差
    errors = np.sqrt(np.sum((predicted_path - actual_path) ** 2, axis=1))
    print(f"平均定位誤差: {np.mean(errors):.2f} 米")