# Blueteeth project development

## 描述

本專案是 **圖書館物聯網導航系統** 的 **雲端與前端 Dashboard**，幫助使用者選擇目標書籍，並透過 **Raspberry Pi + BLE 設備** 指引用戶方向。

## 技術棧

- **後端**：FastAPI（Python 3.10）
- **前端**：React + Vite
- **通信**：Mosquitto MQTT Broker
- **代理**：Nginx
- **容器化**：Docker + Docker Compose
- **資料庫**：SQLite

## 專案架構

```
📂 project-root
├── 📂 backend/        
│  ├── Dockerfile     
│  ├── requirements.txt  
│  ├── 📂 src/        
│  │  ├── main.py    
│  │  ├── 📂 books/    # 書籍邏輯、導航端口
│  │  ├── 📂 history/    # 歷史紀錄
│  │  ├── 📂 rasp/   # 樹莓派邏輯
│  │  ├── 📂 services/  
│  │  │  ├── 📂 maps/ # 地圖建立
│  │  │  ├── 📂 mqtt/ # MQTT 通訊
│  │  │  ├── 📂 navigation/ # 導航主體
│  │  ├── 📂 users/ # 使用者邏輯
│  │  ├── 📂 websockets/ # WebSocket 通訊
│  │  ├── database.py
│  │  ├── config.py
│  │  ├── dependencies.py
│  ├── database.db  # 資料庫
├── 📂 frontend/       
│  ├── Dockerfile    
│  ├── package.json    
│  ├── 📂 src/        # 前端主要程式碼
│  │  ├── App.jsx    
│  │  ├── 📂 components/  
│  │  ├── 📂 pages/     
│  │  ├── 📂 services/   # API 請求
│  │  ├── 📂 store/     
├── 📂 mosquitto/       
│  ├── mosquitto.conf   
├── nginx.conf     
├── docker-compose.yml   
├── .env   
├── .gitignore          
```

---

## 安裝與啟動

**1️⃣ 安裝 Docker & Docker Compose**

請確保你的系統已安裝 [Docker](https://www.docker.com/) 和 [Docker Compose](https://docs.docker.com/compose/)。

**2️⃣ 啟動專案**

```bash
docker compose up --build
```

**3️⃣ 停止專案**

```
docker compose down
```

## 環境變數設定

請在 .env 配置以下變數：

```py
GLOBAL_SECRET_KEY=自選
GLOBAL_ALGORITHM=自選
GLOBAL_AUTH_TOKEN_URL=/api/v1/users/login
GLOBAL_DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES=30000
GLOBAL_API_PREFIX=/api/v1
GLOBAL_DATABASE_URL=sqlite:///database.db

USER_ACCESS_TOKEN_EXPIRE_MINUTES=15000

VITE_BASE_URL=https://d247-49-159-183-84.ngrok-free.app
```

其中 VITE_BASE_URL 是 optional，可利用 ngrok 開設暫時的 url，將 url 貼到 VITE_BASE_URL 後即可用之測試。

## API 端點示例

登入

```json
POST /api/v1/users/login
Content-Type: application/x-www-form-urlencoded

username=yozen0405&password=test1234

RESPONSE
{
  "message": "Logged in successfully.",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5b3plbjA0MDUiLCJleHAiOjE3NDAyNjUyNjN9.9PubGm7MOsqUx_yLCFoctQcnzJG_TXDUEnFUfkw-tvg",
  "token_type": "bearer"
}
```

> 登入的部分可能不太清楚，這邊是 curl 的範例

```bash
curl -X POST "http://localhost/api/v1/users/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=yozen0405&password=test1234"
```

註冊

```json
POST /api/v1/users/register
{
    "username": "yozen0405",
    "password": "test1234"
}

RESPONSE
{
  "message": "User registered successfully.",
  "username": "yozen0405"
}
```

搜尋書籍

```json
POST /api/v1/books/search_book
{
  "search_term": "我"
}

RESPONSE（有找到書）
[
  {
    "id": 2,
    "name": "關於我轉生變成史萊姆這檔事",
    "description": "當命運賜予平凡的靈魂一具史萊姆之軀，他卻以智慧與勇氣翻轉世界，成為萬眾敬畏的傳奇。"
  },
  {
    "id": 5,
    "name": "我的英雄學院 第5卷：轟焦凍",
    "description": "冰火交織的少年，掙脫宿命枷鎖，尋求自我救贖。"
  }
]

RESPONSE（沒找到書）
{
  "detail": "No books found matching the search term."
}
```

執行導航

```json
POST /api/v1/books/navigate
{
  "book_id": 1
}

RESPONSE
{
  "message": "Successfully navigate for user yozen0405",
  "displayed_color": "#b7b106"
}
```

取消導航

```json
POST /api/v1/books/cancel-navigation

RESPONSE
{
  "message": "Successfully canceled navigation!"
}
```

註冊樹莓派

```json
POST /api/v1/rasp/register-rasp
{
  "cord_x": 0,
  "cord_y": 0,
  "facing": "SOUTH",
  "rasp_id": "rasp1"
}

RESPONSE
{
  "Successfully registered Rasp 'rasp1"
}
```


註冊裝置

```json
POST /api/v1/rasp/register-device
{
  "battery": 57,
  "cord_x": 0,
  "cord_y": 0,
  "rasp_id": "rasp1",
  "device_id": "device1"
}

RESPONSE
{
  "Successfully registered Device 'device1"
}
```

更新裝置電量

```json
POST /api/v1/rasp/udpate-device-battery
{
  "battery": 100,
  "device_id": "device1"
}

RESPONSE
{
  "Successfully update the battery of device1"
}
```

## MQTT 訊息

訂閱示例，rasp/rasp2 可換成想訂閱的樹莓派 id：

```bash
mosquitto_sub -h localhost -p 1883 -t "rasp/rasp2"
```

訊息格式總覽：

```json
{"action": "cancel_rasp_navigation", "userName": "yozen0405"}

{"action": "cancel_device_navigation", "userName": "yozen0405", "deviceId": "device3"}

{"action": "add_rasp_direction", "userName": "yozen0405", "direction": "RIGHT", "color": "#038fc2"}

{"action": "add_device_color", "userName": "yozen0405", "color": "#038fc2", "deviceId": "device3"}
```