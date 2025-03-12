import asyncio
import json
import paho.mqtt.client as mqtt
from bleak import BleakClient, BleakScanner
from cloud_receive import send_nrf_message , send_rasp_message


# 設定 MQTT Broker
BROKER_ADDRESS = "0.tcp.jp.ngrok.io"
PORT = 11067
DEVICE = "rasp1"
TOPIC = "rasp/" + DEVICE 
NOTIFY_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"


# 設定 MQTT 客戶端，並加入錯誤處理
mqtt_client = mqtt.Client()

def connect_mqtt():
    """嘗試連接 MQTT Broker，並加入重試機制"""
    while True:
        try:
            mqtt_client.connect(BROKER_ADDRESS, PORT, 60)
            print("[Info] 成功連線到 MQTT Broker")
            return
        except Exception as e:
            print(f"[Error] 連線 MQTT 失敗: {e}")
            print("5 秒後重新嘗試...")
            asyncio.sleep(5)

connect_mqtt()

# 延遲載入，避免循環導入
from nrf_command import send_message_to_ble_device, list_services, notification_handler

def load_target_names(filename="bluelist.txt"):
    """讀取目標藍牙裝置名稱"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"[Error] 檔案 {filename} 未找到，請確保該檔案存在！")
        return []

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

async def scan_and_connect():
    """掃描藍牙裝置並嘗試連接"""
    target_names = load_target_names()
    send_rasp_message(DEVICE)
    while True:
        print("🔍 開始 BLE 掃描 (5 秒)...")
        devices = await BleakScanner.discover(timeout=5.0)

        target_devices = [d for d in devices if d.name in target_names]

        if target_devices:
            print("🎯 找到目標裝置：")
            for d in target_devices:
                print(f"   - {d.name} ({d.address})")

            await asyncio.gather(*(connect_and_listen(d) for d in target_devices))
        else:
            print("⚠️ 未掃描到目標裝置，5 秒後重試...")
        
        await asyncio.sleep(5)



if __name__ == "__main__":
    try:
        asyncio.run(scan_and_connect())
    except KeyboardInterrupt:
        print("❌ 程序終止。")
