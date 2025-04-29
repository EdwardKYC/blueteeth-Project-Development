from config import connected_devices

async def cancel_device_navigation(device_id, color):
    from nrf_command import send_message_to_ble_device
    print(f"[DEBUG] 當前連線裝置: {[dev.__repr__() for dev in connected_devices]}")
    device = next((dev for dev in connected_devices if dev.name == device_id), None)
    if device is None:
        print(f"[ERROR] 裝置名稱 {device_id} 不存在於 connected_devices 中。")
        return
    if device.client is None or not device.client.is_connected:
        print(f"[ERROR] 裝置 {device_id} 尚未連線或已斷線，無法傳送指令。")
        return
    message = f"Can:{color}"
    await send_message_to_ble_device(device.client, message)
    print(f"取消 {color} 指令已傳送到裝置 {device_id}")

async def add_device_color(device_id, color):
    from nrf_command import send_message_to_ble_device
    print(f"[DEBUG] 當前連線裝置: {[dev.__repr__() for dev in connected_devices]}")
    device = next((dev for dev in connected_devices if dev.name == device_id), None)
    if device is None:
        print(f"[ERROR] 裝置 ID {device_id} 不存在於 connected_devices 中。")
        return
    if device.client is None or not device.client.is_connected:
        print(f"[ERROR] 裝置 {device_id} 尚未連線或已斷線，無法傳送指令。")
        return
    message = f"Add color:{color}"
    await send_message_to_ble_device(device.client, message)
    print(f"已將顏色 {color} 傳送到裝置 {device_id}")