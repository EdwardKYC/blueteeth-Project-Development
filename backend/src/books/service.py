from sqlalchemy.orm import Session
from src.books.models import Book

def search_books(db: Session, search_term: str):
    """
    在書名或描述中搜尋匹配的書籍。
    :param db: SQLAlchemy Session
    :param search_term: 搜尋關鍵字
    :return: 匹配的書籍列表
    """
    return db.query(Book).filter(
        (Book.name.ilike(f"%{search_term}%")) | (Book.description.ilike(f"%{search_term}%"))
    ).all()

