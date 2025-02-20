import asyncio , json , time , requests , os
import paho.mqtt.client as mqtt
from bleak import BleakClient , BleakScanner
from datetime import datetime
from config import connected_devices , Device
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883
TOPIC = "register"
DEVICE = "rasp1"
mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER_ADDRESS, PORT, 60)


# 讀取 bluelist.txt 並將 MAC 地址存入列表
def load_device_addresses(file_path="bluelist.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            addresses = [line.strip() for line in file.readlines() if line.strip()]
            return addresses
    except FileNotFoundError:
        print(f"[ERROR] 文件 {file_path} 不存在！")
        return []

def send_mqtt_message(device):
    """
    發送 MQTT 訊息，包含裝置名稱和 MAC 地址
    :param device: Device 類實例
    """
    message = json.dumps({"device_name": device.name, "connected_mac": device.mac})
    mqtt_client.publish(TOPIC, message)
    print(f"[MQTT] 已發送訊息: {message}")

# 嘗試連接到所有藍牙裝置，並檢查 MAC 地址
async def connect_to_device(address, name, valid_addresses):    
    """
    連接藍牙裝置
    :param address: 藍牙裝置 MAC 地址
    :param name: 藍牙裝置名稱
    :param valid_addresses: 允許的 MAC 地址列表
    """
    if address.upper() in connected_devices:
        print(f"[INFO] 裝置 {address} 已連線，跳過重新連線。")
        return

    if address.upper() not in [addr.upper() for addr in valid_addresses]:
        print(f"[INFO] 裝置 {address} 不在允許的 MAC 地址列表中，跳過連接。")
        return

    try:
        async with BleakClient(address) as client:
            if client.is_connected:
                print(f"[INFO] 已成功連接到裝置 {address}")
                # 創建 Device 實例並加入字典
                device = Device(name=name if name else "Unknown", mac=address)
                connected_devices[address.upper()] = device
                send_mqtt_message(device)
            else:
                print(f"[ERROR] 無法連接到裝置 {address}")
    except Exception as e:
        print(f"[ERROR] 連接到裝置 {name} 時發生錯誤: {e}")

# 掃描藍牙裝置並嘗試連接所有裝置
async def scan_and_connect():
    # 加載 MAC 地址列表
    valid_addresses = load_device_addresses()
    print(f"[DEBUG] 加載的允許 MAC 地址列表: {valid_addresses}")
    if not valid_addresses:
        print("[INFO] MAC 地址列表為空，結束掃描。")
        return

    while True:
        print("開始掃描藍牙裝置...")
        devices = await BleakScanner.discover()
        if devices:
            print("[INFO] 掃描到的裝置:")
            for device in devices:
                print(f"名稱: {device.name if device.name else 'Unknown'}, MAC: {device.address}")

            # 比對掃描到的裝置是否在允許的列表中
            print("[INFO] 開始比對掃描到的裝置...")
            for device in devices:
                if device.address.upper() in [addr.upper() for addr in valid_addresses]:
                    print(f"[MATCH] 裝置 {device.address} 在允許列表中，檢查連線狀態...")
                    await connect_to_device(device.address, device.name, valid_addresses)
                else:
                    print(f"[NO MATCH] 裝置 {device.address} 不在允許列表中，跳過。")
        else:
            print("[INFO] 未掃描到任何裝置。")
        print("掃描結束，等待 5 秒後重新掃描...")
        print("")
        await asyncio.sleep(5)

# 主程式入口
if __name__ == "__main__":
    try:
        asyncio.run(scan_and_connect())
    except KeyboardInterrupt:
        print("程序終止。")
