from dataclasses import dataclass
from typing import Optional

@dataclass
class Recipient:
    id: Optional[int]
    name: str
    relation: str
    age: Optional[int] = None