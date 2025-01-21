from sqlalchemy import Column, Integer, String, DateTime, JSON
from src.database import Base
from datetime import datetime, timezone

class HistoryLog(Base):
    __tablename__ = "history_logs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    details = Column(JSON, nullable=True)