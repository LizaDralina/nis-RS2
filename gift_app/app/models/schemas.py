from pydantic import BaseModel
from typing import Optional

class RecipientCreate(BaseModel):
    name: str
    relation: str
    age: Optional[int] = None

class RecipientRead(BaseModel):
    id: int
    name: str
    relation: str
    age: Optional[int] = None