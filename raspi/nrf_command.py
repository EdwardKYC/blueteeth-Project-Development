import asyncio
from bleak import BleakClient
from bleak.exc import BleakError
print(BleakClient)
BT_UUID_CUSTOM_SERVICE = "0c71e180-65d9-4497-8ca4-a65d86d5003b"
BT_UUID_CUSTOM_CHAR = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
NOTIFY_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

async def send_message_to_ble_device(client, message):
    """發送訊息到 BLE 設備，包含延遲和重試"""
    max_retries = 3
    retry_delay = 0.5
    write_delay = 0.2  # 寫入前的延遲

    for attempt in range(max_retries):
        try:
            if not client.is_connected:
                print(f"[Error] Client 未連線: {client}")
                return False

            # 檢查 characteristic 是否可寫
            services = await client.get_services()
            char_found = False
            for service in services:
                for char in service.characteristics:
                    if char.uuid == BT_UUID_CUSTOM_CHAR:
                        char_found = True
                        if "write" not in char.properties and "write_without_response" not in char.properties:
                            print(f"[Error] Characteristic {BT_UUID_CUSTOM_CHAR} 不支援寫入")
                            return False
                        break
                if char_found:
                    break
            if not char_found:
                print(f"[Error] 未找到 characteristic {BT_UUID_CUSTOM_CHAR}")
                return False

            # 添加寫入延遲
            await asyncio.sleep(write_delay)
            encoded_message = (message + "\n").encode('utf-8')
            await client.write_gatt_char(BT_UUID_CUSTOM_CHAR, encoded_message, response=False)
            print(f"?? 訊息已發送: {message}")
            return True

        except BleakError as e:
            print(f"[Error] 發送訊息失敗 (Bleak 錯誤): {e}")
            if attempt < max_retries - 1:
                print(f"? 等待 {retry_delay} 秒後重試...")
                await asyncio.sleep(retry_delay)
        except Exception as e:
            print(f"[Error] 發送訊息失敗 (其他錯誤): {e}")
            if attempt < max_retries - 1:
                print(f"? 等待 {retry_delay} 秒後重試...")
                await asyncio.sleep(retry_delay)
    print(f"[Error] 發送訊息失敗，已達最大重試次數")
    return False

async def list_services(client):
    services = await client.get_services()
    for service in services:
        print(f"Service: {service.uuid}")
        for char in service.characteristics:
            print(f"  Characteristic: {char.uuid}, Handle: {char.handle}, Properties: {char.properties}")
            if "write" in char.properties or "write_without_response" in char.properties:
                print(f"{char.uuid} 可以寫入！")
            else:
                print(f"{char.uuid} 可能無法寫入！")

def notification_handler(sender, data):
    from cloud_receive import send_nrf_message

    try:
        decoded = data.decode('utf-8')
    except Exception as e:
        decoded = str(data)
    print(f"收到來自 {sender} 的通知: {decoded}")
    send_nrf_message(decoded)

async def ensure_connected(device):
    """
    檢查 device.client 是否有效，
    如不存在或未連線則嘗試重新連線，
    並返回有效的 client（或 None 表示連線失敗）
    """
    from bleak import BleakClient
    if device.client is None or not device.client.is_connected:
        print(f"裝置 {device.name} 尚未連線或連線中斷，嘗試重新連線...")
        client = BleakClient(device.address)
        try:
            await client.connect()
            if client.is_connected:
                device.client = client
                print(f"裝置 {device.name} 重新連線成功")
                return client
            else:
                print(f"[Error] 裝置 {device.name} 重新連線失敗")
                return None
        except Exception as e:
            print(f"[Error] 裝置 {device.name} 重新連線時發生例外: {e}")
            return None
    else:
        return device.client

