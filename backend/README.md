# 雲端架構說明

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

在根目錄下打上

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
