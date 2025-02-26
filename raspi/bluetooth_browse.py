import asyncio
from bleak import BleakScanner, BleakClient
from nrf_command import send_message_to_ble_device , list_services , notification_handler

def load_target_names(filename="bluelist.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"檔案 {filename} 未找到，請確保該檔案存在！")
        return []

async def connect_and_listen(device):
    """與 BLE 裝置連線並保持連線"""
    while True:
        try:
            async with BleakClient(device.address) as client:
                print(f"已成功連線到 {device.name} ({device.address})")
                await send_message_to_ble_device(client, "change color")

                print(f"訊息已發送: change color")
                
                #await list_services(client)
                while True:
                    await asyncio.sleep(10) 

        except Exception as e:
            print(f"{device.name} 連線中斷: {e}")
            print(f"2 秒後重新嘗試連線 {device.name}...")
            await asyncio.sleep(2) 

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

if __name__ == "__main__":
    asyncio.run(main())
