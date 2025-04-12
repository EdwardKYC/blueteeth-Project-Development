#cloud_command.py
from config import connected_devices
from nrf_command import ensure_connected
async def cancel_device_navigation(device_id , color):
    from nrf_command import send_message_to_ble_device
    device = next((dev for dev in connected_devices if dev.name == device_id), None)
    if device:
        #client = await ensure_connected(device)
        if device.client is None:
            print(f"[ERROR] 裝置 {device_id} 尚未連線，無法傳送指令。")
            return
        message = f"Cancel color:{color}"
        await send_message_to_ble_device(device.client, message)
        print(f"取消 {color}指令已傳送到裝置 {device_id}")
    else:   
        print(f"[ERROR] 裝置名稱 {device_id} 不存在於 connected_devices 中。")

async def add_device_color(device_id, color):
    from nrf_command import send_message_to_ble_device
    device = next((dev for dev in connected_devices if dev.name == device_id), None)
    if device:
        #client = await ensure_connected(device)
        if device.client is None:
            print(f"[ERROR] 裝置 {device_id} 尚未連線，無法傳送指令。")
            return
        message = f"Add color:{color}"
        await send_message_to_ble_device(device.client, message)
        print(f"已將顏色 {color} 傳送到裝置 {device_id}")
    else:
        print(f"[ERROR] 裝置 ID {device_id} 不存在於 connected_devices 中。")        
