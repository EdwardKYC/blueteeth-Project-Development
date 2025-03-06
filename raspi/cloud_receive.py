import paho.mqtt.client as mqtt
import json
import time
import threading
import tkinter as tk
from config import connected_devices
from cloud_command import cancel_device_navigation , add_device_color 

BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883
DEVICE = "rasp1"
TOPIC = DEVICE + "/commands"

COMMAND_CATEGORIES = {
    "cancel_rasp_navigation": "cancel_rasp_navigation",
    "cancel_device_navigation": "cancel_device_navigation",
    "add_rasp_direction": "add_rasp_direction",
    "add_device_color": "add_device_color"
}

users = []
current_label = None

root = tk.Tk()
root.title("Direction Display App")
root.configure(bg="white")
root.state('zoomed')  

def resize_font(event=None):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    font_size = int(min(window_width, window_height) // 10)
    for label in users:
        label.config(font=("Helvetica", font_size))

root.bind('<Configure>', resize_font) 
root.configure(bg="white")

def cancel_rasp_navigation(username):
    global users
    for label in users:
        if username in label.cget("text"):
            label.destroy()
            users.remove(label)
            break

def add_rasp_direction(username, direction):
    global users
    user_info = f"{username}: {direction}\n"
    label = tk.Label(root, text=user_info, bg="white", font=("Helvetica", 14))
    label.pack(pady=10, anchor="center", expand=True)
    users.append(label)

def cycle_users():
    global users, current_label
    if users:
        if current_label:
            current_label.pack_forget()

        current_label = users[0]
        current_label.pack(pady=10, anchor="center", expand=True)
        users.append(users.pop(0))
    
    root.after(2000, cycle_users)

root.after(2000, cycle_users)

def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        action = payload.get("action")

        if action in COMMAND_CATEGORIES:
            category = COMMAND_CATEGORIES[action]
            handle_command(category, payload)
        else:
            print(f"[Warning] 未知的指令: {action}")
    except json.JSONDecodeError:
        print("[Error] 無法解析收到的 JSON 資料")

def handle_command(category, payload):
    if category == "cancel_rasp_navigation":
        user_name = payload.get("userName")
        print(f"取消 {user_name} 的方向指引")
        cancel_rasp_navigation(user_name)

    elif category == "add_rasp_direction":
        direction = payload.get("direction")
        user_name = payload.get("userName")
        print(f"為 {user_name} 新增 Raspberry Pi 導航方向指令: {direction}")
        add_rasp_direction(user_name, direction)

    elif category == "add_device_color":
        device_id = payload.get("deviceId")
        color = payload.get("color")
        print(f"為裝置 {device_id} 新增顏色: {color}")
        add_device_color(device_id, color)



def on_disconnect(client, userdata, rc):
    print(f"[Warning] 與 MQTT Broker 的連線斷開，等待 60 秒後嘗試重新連線...")
    try:
        client.reconnect()
        print("[Info] 重新連線成功")
    except Exception as e:
        print(f"[Error] 無法重新連線: {e}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[Info] 成功連線到 MQTT Broker")
        client.subscribe(TOPIC)
    else:
        print(f"[Error] 連線失敗，返回碼: {rc}")

mqtt_client = None

def mqtt_loop():
    global mqtt_client
    client = mqtt.Client()
    mqtt_client = client
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_connect = on_connect

    try:
        client.connect(BROKER_ADDRESS, PORT, 60)
        client.loop_forever() 
    except Exception as e:
        print(f"[Error] 连接MQTT Broker失败: {e}")

def send_message_to_mqtt(message: str):
    global mqtt_client
    if mqtt_client:
        mqtt_client.publish(TOPIC, message)
        print("已發佈訊息至 MQTT:", message)
    else:
        print("MQTT client 尚未連線，無法發佈訊息。")

mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
mqtt_thread.start()

root.mainloop()
