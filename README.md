# Blueteeth project development

## 描述

本專案結合手機 App 與圖書館內的樹莓派屏幕，透過 BLE 導航技術，協助讀者快速定位書籍，提升檢索效率與使用體驗。

## 實際場景

![Image](https://github.com/user-attachments/assets/7c4e54ff-cc5e-4f61-9699-a41fd9805952)

## 架構圖

### 前期部署

![Image](https://github.com/user-attachments/assets/0de63b8c-2181-4d22-ba46-371b9ee31f15)

### 使用者開啟 app

![Image](https://github.com/user-attachments/assets/df3c50a8-02e4-46e1-af1a-66cb8a000202)

### 使用者選取書籍

![Image](https://github.com/user-attachments/assets/4a4dab76-305a-4db3-969c-f291c137bedd)

### 使用者取消書籍

![Image](https://github.com/user-attachments/assets/dab8da77-9539-4206-a9d1-e40ae19293da)

### 實時更新

![Image](https://github.com/user-attachments/assets/9940d1e9-d2a8-437e-a7dc-f116dd2d0488)

## API 端點示例

以下端點預設都是 `Content-Type: application/json`

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

RESPONSE（導航成功）
{
  "message": "Successfully navigate for user yozen0405",
  "displayed_color": "#b7b106"
}
RESPONSE（導航失敗，status_code=400）
{
  "detail": "Can't find a path for book id 1."
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


## MQTT 訊息

### 樹莓派訂閱雲端MQTT

訂閱示例，rasp/rasp2 可換成想訂閱的樹莓派 id：

```bash
mosquitto_sub -h localhost -p 1883 -t "rasp/rasp2"
```

訊息格式總覽：

```json
{"action": "cancel_rasp_navigation", "userName": "yozen0405"}

{"action": "cancel_device_navigation", "userName": "yozen0405", "deviceId": "device3"}

{"action": "add_rasp_direction", "userName": "yozen0405", "direction": "RIGHT", "color": "#038fc2"}

{"action": "add_device_color", "color": "#038fc2", "deviceId": "device3"}
```