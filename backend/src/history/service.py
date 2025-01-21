from sqlalchemy.orm import Session
from datetime import datetime
from .models import HistoryLog
from .constant import LogType 
from src.websockets import WebSocketMessageHandler
import pytz

websocket_message_handler = WebSocketMessageHandler()

class HistoryService:
    async def _insert_log(self, db: Session, log_type: LogType, action: str, details: dict):
        """
        Add a history log entry.
        """
        taipei_tz = pytz.timezone("Asia/Taipei")

        log = HistoryLog(
            type=log_type.value,
            action=action,
            details=details,
            timestamp=datetime.now(taipei_tz),
        )
        db.add(log)
        db.commit()

        await websocket_message_handler.add_history_log(log)

    async def log_info(self, db: Session, action: str, details: dict):
        """
        Log an informational message.
        """
        await self._insert_log(db, LogType.INFO, action, details)

    async def log_warning(self, db: Session, action: str, details: dict):
        """
        Log a warning message.
        """
        await self._insert_log(db, LogType.WARNING, action, details)

    async def log_error(self, db: Session, action: str, details: dict):
        """
        Log an error message.
        """
        await self._insert_log(db, LogType.ERROR, action, details)

    def get_logs(self, db: Session, log_type: LogType = None):
        """
        Retrieve all history logs, optionally filtered by type.
        """
        query = db.query(HistoryLog).order_by(HistoryLog.timestamp.desc())
        if log_type:
            query = query.filter(HistoryLog.type == log_type.value)
        logs = query.all()

        return [self._format_log(log) for log in logs]

    async def clear_logs(self, db: Session):
        try:
            db.query(HistoryLog).delete() 
            db.commit()
        except Exception as e:
            db.rollback() 
            raise RuntimeError(f"Failed to clear logs: {str(e)}")
        
        await websocket_message_handler.clear_all_history()

    def _format_log(self, log: HistoryLog) -> dict:
        """
        Format a single history log.
        """
        return {
            "id": log.id,
            "type": log.type,
            "action": log.action,
            "timestamp": log.timestamp.isoformat(),
            "details": log.details,
        }