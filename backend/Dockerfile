# 基礎映像
FROM python:3.10-slim

# 設置工作目錄
WORKDIR /app

# 複製依賴文件
COPY ./requirements.txt /app/requirements.txt

# 安裝依賴
RUN pip install --no-cache-dir -r /app/requirements.txt

# 複製程式碼
COPY ./src /app/src

# 啟動指令
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]