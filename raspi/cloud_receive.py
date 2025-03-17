# file name: cloud_receive.py
import tkinter as tk
import threading
import requests
import asyncio
from cloud_command import cancel_device_navigation, add_device_color

API_URL = "http://210.242.67.61:1160"
users = []
current_label = None

root = tk.Tk()
root.title("Direction Display App")
root.configure(bg="white")
root.attributes('-zoomed', True)  # 適用於 Linux & Windows
root.state('normal')

def resize_font(event=None):
    """自動調整字體大小"""
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    font_size = int(min(window_width, window_height) // 10)
    for label in users:
        label.config(font=("Helvetica", font_size))

root.bind('<Configure>', resize_font) 

def cancel_rasp_navigation(username):
    """從 UI 移除特定用戶"""
    global users
    for label in users:
        if username in label.cget("text"):
            label.destroy()
            users.remove(label)
            break

def add_rasp_direction(username, direction, color):
    """在 UI 添加新的方向資訊，並支援顏色"""
    global users
    user_info = f"{username}: {direction}\n"
    label = tk.Label(root, text=user_info, bg="white", fg=color, font=("Helvetica", 14))  # ✅ 設定文字顏色
    label.pack(pady=10, anchor="center", expand=True)
    users.append(label)


def cycle_users():
    """切換顯示不同的使用者"""
    global users, current_label
    if users:
        if current_label:
            current_label.pack_forget()
        current_label = users[0]
        current_label.pack(pady=10, anchor="center", expand=True)
        users.append(users.pop(0))
    root.after(2000, cycle_users)

root.after(2000, cycle_users)

def handle_command(category, payload):
    """處理來自 MQTT 的指令"""
    root.after(0, process_command, category, payload)  # ✅ 確保 Tkinter 主執行緒處理更新

def process_command(category, payload):
    """處理 UI 更新，確保在 Tkinter 主執行緒內執行"""
    if category == "cancel_rasp_navigation":
        user_name = payload.get("userName")
        print(f"取消 {user_name} 的方向指引")
        cancel_rasp_navigation(user_name)

    elif category == "add_rasp_direction":
        direction = payload.get("direction")
        user_name = payload.get("userName")
        color = payload.get("color")
        print(f"為 {user_name} 新增 Raspberry Pi 導航方向指令: {direction}")
        add_rasp_direction(user_name, direction , color)

    elif category == "add_device_color":
        device_id = payload.get("deviceId")
        color = payload.get("color")
        print(f"為裝置 {device_id} 新增顏色: {color}")
        asyncio.create_task(add_device_color(device_id, color))
    
    elif category == "cancel_device_navigation":
        color = payload.get("color")
        device_id = payload.get("deviceId")
        print(f"取消裝置 {device_id} 的顏色: {color}")
        asyncio.create_task(cancel_device_navigation(device_id, color))

def send_nrf_message(message_str):
    """透過 REST API 發送裝置資訊"""
    try:
        battery, cord_x, cord_y, device_id = message_str.split(", ")  
        battery, cord_x, cord_y = map(int, [battery, cord_x, cord_y]) 

        url = API_URL + "/api/v1/rasp/register-device"
        payload = {
            "battery": battery,
            "cord_x": cord_x,
            "cord_y": cord_y,
            "rasp_id": "rasp1",
            "device_id": device_id
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"[REST API] 訊息成功發送: {payload}")
        else:
            print(f"[REST API] 伺服器回應錯誤: {response.status_code}, {response.text}")
    
    except ValueError:
        print(f"[Error] 無法解析訊息: {message_str}")
    except Exception as e:
        print(f"[Error] 傳送 REST API 失敗: {e}")
        
def send_rasp_message(message_str):
    """發送 Raspberry Pi 位置訊息"""
    try:
        url = API_URL + "/api/v1/rasp/register-rasp"
        payload = {
            "cord_x": 0,
            "cord_y": 0,
            "facing": "SOUTH",
            "rasp_id": message_str,
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"[REST API] 訊息成功發送: {payload}")
        else:
            print(f"[REST API] 伺服器回應錯誤: {response.status_code}, {response.text}")
    
    except ValueError:
        print(f"[Error] 無法解析訊息: {message_str}")
    except Exception as e:
        print(f"[Error] 傳送 REST API 失敗: {e}")

def start_tkinter_thread():
    """在背景執行 Tkinter GUI"""
    tk_thread = threading.Thread(target=root.mainloop, daemon=True)
    tk_thread.start()
