from pydantic import BaseModel, Field , field_validator
from typing import Optional
from datetime import datetime


class BookValidator(BaseModel):
    book_id: int
    title: str
    author: str
    price: float
    quantity: int
    userid: int

    
