from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db
from .service import HistoryService

history = HistoryService()

router = APIRouter(
    prefix="/history",
    tags=["History"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get-all-history", response_model=list)
def get_all_history(db: Session = Depends(get_db)):
    """
    Fetch all history.
    """
    return history.get_logs(db)

@router.delete("/clear-logs")
async def clear_all_logs(db: Session = Depends(get_db)):
    """
    Clear all history logs.
    """
    await history.clear_logs(db)
    return {"message": "All logs cleared successfully."}