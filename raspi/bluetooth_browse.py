import asyncio
from bleak import BleakScanner, BleakClient
from config import connected_devices , ConnectedDevice
from nrf_command import send_message_to_ble_device , list_services , notification_handler

NOTIFY_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

def load_target_names(filename="bluelist.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"檔案 {filename} 未找到，請確保該檔案存在！")
        return []

async def connect_and_listen(device):
    """與 BLE 裝置連線並保持監聽"""
    try:
        async with BleakClient(device.address) as client:
            print(f"✅ 已成功連線到 {device.name} ({device.address})")

            for dev in connected_devices:
                if dev.mac_address == device.address:
                    dev.client = client  # ✅ 存入 `BleakClient` 實例
                    break

            # 送出初始指令
            await send_message_to_ble_device(client, "change color")
            print(f"📩 訊息已發送: change color")

            # 啟用通知
            await client.start_notify(NOTIFY_UUID, notification_handler)
            print("🔔 已啟用通知功能，等待資料...")

            # 持續監聽
            while await client.is_connected():
                await asyncio.sleep(10)

    except Exception as e:
        print(f"[Error] {device.name} 連線中斷: {e}")

    finally:
        if client.is_connected:
            await client.disconnect()
            print(f"🔌 {device.name} 已斷線")

        if device in connected_devices:
            connected_devices.remove(device)  # ✅ **從列表中移除裝置**
        print(f"⚠️ {device.name} 斷線，等待重新掃描...")


async def main():
    target_names = load_target_names()

    while True:
        print("開始 BLE 掃描 (5 秒)...")
        devices = await BleakScanner.discover(timeout=5.0)
    
        target_devices = [d for d in devices if d.name in target_names]

        if target_devices:
            print("找到目標裝置：")
            for d in target_devices:
                print(f"   - {d.name} ({d.address})")

            await asyncio.gather(*(connect_and_listen(d) for d in target_devices))
        else:
            print("未掃描到目標裝置，5 秒後重試...")
        
        await asyncio.sleep(5) 

def run_nrf():
    asyncio.run(main())
