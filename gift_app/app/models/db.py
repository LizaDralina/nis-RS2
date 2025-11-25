from typing import Any

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base: Any = declarative_base()


class RecipientDB(Base):
    __tablename__ = "recipients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    relation = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
