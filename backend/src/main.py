from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import asyncio
from src.utils import check_alive_status, set_main_loop
from src.database import Base, engine
from src.users.router import router as user_router
from src.books.router import router as book_router
from src.rasp.router import router as rasp_router
from src.websockets.router import router as websocket_router
from src.history.router import router as history_router
from src.services.mqtt.message import MQTTMessageHandler


Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI(
    root_path="/api",  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    set_main_loop(loop)
    asyncio.create_task(check_alive_status())
    mqtt_handler = MQTTMessageHandler()
    mqtt_handler.start()

app.include_router(user_router, prefix="/v1")
app.include_router(book_router, prefix="/v1")
app.include_router(rasp_router, prefix="/v1")
app.include_router(websocket_router, prefix="/v1")
app.include_router(history_router, prefix="/v1")


