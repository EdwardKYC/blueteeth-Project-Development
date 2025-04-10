import asyncio
import json
import threading
import paho.mqtt.client as mqtt
from bleak import BleakScanner, BleakClient
from config import connected_devices, ConnectedDevice
import cloud_receive  # ✅ 確保 UI 可用
from nrf_command import send_message_to_ble_device, notification_handler

# MQTT 設定
BROKER_ADDRESS = "0.tcp.jp.ngrok.io"
PORT = 19785
DEVICE = "rasp1"
TOPIC = "rasp/" + DEVICE 
NOTIFY_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
COMMAND_CATEGORIES = {
    "cancel_rasp_navigation": "cancel_rasp_navigation",
    "cancel_device_navigation": "cancel_device_navigation",
    "add_rasp_direction": "add_rasp_direction",
    "add_device_color": "add_device_color"
}

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    """當 MQTT 連線成功時觸發"""
    if rc == 0:
        print("[Info] 成功連線到 MQTT Broker")
        client.subscribe(TOPIC)
    else:
        print(f"[Error] 連線失敗，返回碼: {rc}")

def on_message(client, userdata, message):
    """處理 MQTT 訊息，並將其傳給 `cloud_receive.py`"""
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        action = payload.get("action")

        if action in COMMAND_CATEGORIES:
            category = COMMAND_CATEGORIES[action]
            print(f"[MQTT] 收到指令: {category}")
            cloud_receive.handle_command(category, payload)  # ✅ 更新 UI
        else:
            print(f"[Warning] 未知的指令: {action}")
    except json.JSONDecodeError:
        print("[Error] 無法解析收到的 JSON 資料")

def on_disconnect(client, userdata, rc):
    """當 MQTT 斷線時自動重連"""
    print("[Warning] 與 MQTT 斷線，嘗試重新連線...")
    while True:
        try:
            client.reconnect()
            print("[Info] MQTT 重新連線成功")
            break
        except Exception as e:
            print(f"[Error] MQTT 重連失敗: {e}，5 秒後重試...")
            asyncio.sleep(5)

async def mqtt_loop():
    """讓 MQTT 在 `asyncio` 內部運行"""
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect

    try:
        mqtt_client.connect(BROKER_ADDRESS, PORT, 60)
        mqtt_client.loop_start()  # ✅ 讓 MQTT 在背景執行，不阻塞 asyncio
        while True:
            await asyncio.sleep(1)  # ✅ 避免阻塞，確保 MQTT 保持運行
    except Exception as e:
        print(f"[Error] 連接 MQTT Broker 失敗: {e}")

async def connect_and_listen(device):
    """與 BLE 裝置連線並保持連線"""
    while True:
        try:
            async with BleakClient(device.address) as client:
                print(f"✅ 已成功連線到 {device.name} ({device.address})")
                await send_message_to_ble_device(client, "change color")
                print(f"📩 訊息已發送: change color")

                await client.start_notify(NOTIFY_UUID, notification_handler)
                print("🔔 已啟用通知功能，等待資料...")

                while True:
                    await asyncio.sleep(10)
        except Exception as e:
            print(f"[Error] {device.name} 連線中斷: {e}")
            print("2 秒後重新嘗試連線...")
            await asyncio.sleep(2)

def load_target_names(filename="bluelist.txt"):
    """讀取目標藍牙裝置名稱"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"[Error] 檔案 {filename} 未找到，請確保該檔案存在！")
        return []

async def scan_and_connect():
    """掃描藍牙裝置並嘗試連接"""
    target_names = load_target_names()  # 這裡填入目標裝置名稱列表
    while True:
        cloud_receive.send_rasp_message(DEVICE)
        print("🔍 開始 BLE 掃描 (5 秒)...")
        try:
            devices = await BleakScanner.discover(timeout=5.0)
        except Exception as e:
            print(f"[Error] BLE 掃描失敗: {e}")
            await asyncio.sleep(5)
            continue  # 繼續執行下一次掃描

        target_devices = [d for d in devices if d.name in target_names]

        if target_devices:
            print("🎯 找到目標裝置：")
            for d in target_devices:
                print(f"   - {d.name} ({d.address})")

            if d.address not in [dev.address for dev in connected_devices]:
                print(f"🔗 嘗試連線到 {d.name} ({d.address})...")
                connected_devices.append(ConnectedDevice(d.name, d.address))  # ✅ 記錄裝置
                asyncio.create_task(connect_and_listen(d)) 
        else:
            print("⚠️ 未掃描到目標裝置，5 秒後重試...")
        
        await asyncio.sleep(5)  

async def main():
    """同時執行 MQTT 監聽 & BLE 掃描"""
    await asyncio.gather(mqtt_loop(), scan_and_connect())  # ✅ 讓 MQTT & BLE 並行執行

def start_asyncio():
    """在背景執行 asyncio"""
    asyncio.run(main())

if __name__ == "__main__":
    try:
        print("start")

        # ✅ 使用 threading 來讓 asyncio 在背景執行
        asyncio_thread = threading.Thread(target=start_asyncio, daemon=True)
        asyncio_thread.start()

        # ✅ 讓 Tkinter 在主執行緒執行
        cloud_receive.root.mainloop()
    
    except KeyboardInterrupt:
        print("❌ 程序終止。")
