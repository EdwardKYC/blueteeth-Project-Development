from pydantic import BaseModel, Field
from typing import Optional

class SearchBookSchema(BaseModel):
    search_term: str = Field(..., min_length=0, max_length=255, description="The term to search for books")

class RegisterBookSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="The name of the book")
    device_id: str = Field(..., min_length=1, max_length=100, description="The ID of the device associated with the book")
    description: Optional[str] = Field(None, max_length=1000, description="A brief description of the book")

class NavigateBookSchema(BaseModel):
    book_id: int = Field(..., gt=0, description="The ID of the book to navigate to")