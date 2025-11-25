from typing import Optional

from pydantic import BaseModel


class RecipientCreate(BaseModel):
    name: str
    relation: str
    age: Optional[int] = None


class RecipientRead(BaseModel):
    id: int
    name: str
    relation: str
    age: Optional[int] = None
