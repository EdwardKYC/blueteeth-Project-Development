from bleak import BleakClient
import asyncio

BT_UUID_CUSTOM_SERVICE = "0c71e180-65d9-4497-8ca4-a65d86d5003b"
BT_UUID_CUSTOM_CHAR = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

async def send_message_to_ble_device(client, message):
    try:
        print("開始傳送訊息...")
        encoded_message = message.encode('utf-8')
        """
        services = await client.get_services()
        for service in services:
            print("Service:", service.uuid)
            for char in service.characteristics:
                print("  Characteristic:", char.uuid, "Properties:", char.properties)
        """
        await client.write_gatt_char(BT_UUID_CUSTOM_CHAR, encoded_message)
        print(f"訊息已發送: {message}")
    except Exception as e:
        print(f"發送訊息時發生錯誤: {e}")

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