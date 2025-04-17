import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import ReduceLROnPlateau
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import time

# 圖書館參數
WIDTH, HEIGHT = 50, 30  # 圖書館尺寸（米）
NUM_DEVICES = 15  # 藍芽裝置數量
NUM_SAMPLES = 10_000_000  # 訓練數據樣本數
P_t = -20  # 發射功率 (dBm)
n = 2.5  # 路徑損耗指數
A = 10  # 環境衰減 (dBm)
NOISE_STD = 3  # 高斯噪聲標準差 (dBm)

def simulate_rssi_vectorized(positions, device_positions, shelves=None):
    """計算向量化 RSSI（包含噪聲、書架遮擋和多路徑效應）"""
    diff = positions[:, np.newaxis, :] - device_positions[np.newaxis, :, :]
    distance = np.linalg.norm(diff, axis=2)
    distance = np.maximum(distance, 0.1)
    rssi = P_t - 10 * n * np.log10(distance) - A

    # 模擬書架遮擋
    if shelves is not None:
        for shelf in shelves:
            shelf_x, shelf_y = shelf['position']
            shelf_w, shelf_h = shelf['size']
            for i in range(len(positions)):
                for j in range(len(device_positions)):
                    if (min(positions[i, 0], device_positions[j, 0]) < shelf_x < max(positions[i, 0], device_positions[j, 0]) and
                        min(positions[i, 1], device_positions[j, 1]) < shelf_y < max(positions[i, 1], device_positions[j, 1])):
                        rssi[i, j] -= 7  # 書架遮擋衰減

    # 模擬多路徑效應（隨機反射）
    multipath = np.random.uniform(0, 3, rssi.shape)  # 額外衰減 0-3 dBm
    rssi -= multipath

    # 混合噪聲：高斯噪聲 + 突發噪聲
    gaussian_noise = np.random.normal(0, NOISE_STD, rssi.shape)
    burst_noise = np.random.choice([0, 7], size=rssi.shape, p=[0.9, 0.1])  # 10% 概率突發噪聲
    rssi += gaussian_noise + burst_noise
    return rssi.astype(np.float32)

def generate_dataset_batched(num_samples, batch_size=500_000):
    """分批生成大規模 RSSI 數據集，確保均勻分佈，並生成置信度標籤"""
    device_positions = np.random.uniform([0, 0], [WIDTH, HEIGHT], (NUM_DEVICES, 2)).astype(np.float32)
    # 模擬書架
    shelves = [
        {'position': [10, 15], 'size': [10, 1]},
        {'position': [20, 15], 'size': [10, 1]},
        {'position': [30, 15], 'size': [10, 1]},
        {'position': [40, 15], 'size': [10, 1]}
    ]
    data_list, label_list = [], []

    # 分層採樣：5m x 5m 網格
    grid_size = 5
    samples_per_grid = num_samples // ((WIDTH // grid_size) * (HEIGHT // grid_size))
    for i in range(0, int(WIDTH), grid_size):
        for j in range(0, int(HEIGHT), grid_size):
            positions = np.random.uniform([i, j], [i + grid_size, j + grid_size], (samples_per_grid, 2)).astype(np.float32)
            rssi_data = simulate_rssi_vectorized(positions, device_positions, shelves)
            # 為標籤添加置信度列（設為 1.0）
            confidences = np.ones((len(positions), 1), dtype=np.float32)
            labels_with_confidence = np.hstack((positions, confidences))
            data_list.append(rssi_data)
            label_list.append(labels_with_confidence)

    return np.vstack(data_list), np.vstack(label_list), device_positions

def train_cnn_model(data, labels):
    """訓練增強的 CNN 模型"""
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    data_reshaped = data_scaled.reshape(-1, 5, 3, 1)

    X_train, X_val, y_train, y_val = train_test_split(data_reshaped, labels, test_size=0.2, random_state=42)

    model = Sequential([
        Input(shape=(5, 3, 1)),  # 顯式指定輸入形狀
        Conv2D(64, (3, 3), activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        BatchNormalization(),
        Conv2D(128, (3, 3), activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Conv2D(256, (3, 3), activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        BatchNormalization(),
        Conv2D(256, (3, 3), activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        BatchNormalization(),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.3),
        Dense(256, activation='relu'),
        Dropout(0.2),
        Dense(3)  # 輸出 (x, y, confidence)
    ])

    model.compile(optimizer='adam', loss='mse')
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1)
    history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=512, callbacks=[reduce_lr], verbose=1)
    return model, scaler, history

def simulate_user_path(num_points=100):
    """模擬用戶移動路徑（橢圓路徑）"""
    t = np.linspace(0, 2 * np.pi, num_points)
    x = 25 + 15 * np.cos(t)
    y = 15 + 10 * np.sin(t)
    return np.vstack((x, y)).T

def predict_user_path(model, scaler, path, device_positions):
    """預測用戶位置並平滑路徑"""
    rssi_data = np.array([simulate_rssi_vectorized(np.array([pos]), device_positions)[0] for pos in path])
    rssi_scaled = scaler.transform(rssi_data)
    rssi_reshaped = rssi_scaled.reshape(-1, 5, 3, 1)
    predictions = model.predict(rssi_reshaped, verbose=0)

    # 分離座標和置信度
    predicted_positions = predictions[:, :2]
    confidences = predictions[:, 2]

    # 置信度過濾（低於 0.5 的點使用移動平均替代）
    smoothed_positions = predicted_positions.copy()
    window_size = 5
    for i in range(len(predicted_positions)):
        if i >= window_size and confidences[i] < 0.5:
            smoothed_positions[i] = np.mean(predicted_positions[max(0, i-window_size):i], axis=0)

    # 移動平均平滑
    for i in range(len(smoothed_positions)):
        start = max(0, i - window_size // 2)
        end = min(len(smoothed_positions), i + window_size // 2 + 1)
        smoothed_positions[i] = np.mean(smoothed_positions[start:end], axis=0)

    return smoothed_positions, confidences

def plot_results(actual_path, predicted_path, device_positions, confidences, history):
    """繪製結果圖表並保存訓練損失曲線"""
    # 繪製路徑
    plt.figure(figsize=(12, 8))
    plt.scatter(device_positions[:, 0], device_positions[:, 1], c='red', marker='^', s=100, label='BLE Devices')
    plt.plot(actual_path[:, 0], actual_path[:, 1], 'b-', label='Actual Path')
    plt.plot(predicted_path[:, 0], predicted_path[:, 1], 'r--', label='Predicted Path')
    plt.title('Actual vs Predicted User Path in Library')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, WIDTH)
    plt.ylim(0, HEIGHT)
    plt.savefig('location_prediction.png')
    plt.close()

    # 繪製訓練損失曲線
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss (MSE)')
    plt.legend()
    plt.grid(True)
    plt.savefig('training_loss.png')
    plt.close()

if __name__ == "__main__":
    total_start = time.time()

    print("🚀 開始資料產生...")
    start = time.time()
    data, labels, device_positions = generate_dataset_batched(NUM_SAMPLES)
    print(f"✅ 資料產生完成，用時 {time.time() - start:.2f} 秒")

    print("🚀 開始模型訓練...")
    start = time.time()
    model, scaler, history = train_cnn_model(data, labels)
    print(f"✅ 模型訓練完成，用時 {time.time() - start:.2f} 秒")

    print("🚀 模擬用戶移動並預測位置...")
    start = time.time()
    actual_path = simulate_user_path()
    predicted_path, confidences = predict_user_path(model, scaler, actual_path, device_positions)
    print(f"✅ 位置預測完成，用時 {time.time() - start:.2f} 秒")

    print("🚀 繪製結果圖表...")
    start = time.time()
    plot_results(actual_path, predicted_path, device_positions, confidences, history)
    print(f"✅ 繪圖完成，用時 {time.time() - start:.2f} 秒")

    errors = np.sqrt(np.sum((predicted_path - actual_path) ** 2, axis=1))
    print(f"📍 平均定位誤差: {np.mean(errors):.2f} 米")
    print(f"📉 最大誤差: {np.max(errors):.2f} 米")
    print(f"📈 最小誤差: {np.min(errors):.2f} 米")
    print(f"🏁 全部流程總耗時: {time.time() - total_start:.2f} 秒")