
from app.models.domain import Recipient
from app.repositories.recipient_repo import InMemoryRecipientRepository
from typing import Optional

class RecipientService:
    def __init__(self, repo: InMemoryRecipientRepository):
        self.repo = repo

    def create_recipient(self, name: str, relation: str, age: Optional[int] = None) -> Recipient:
        recipient = Recipient(id=None, name=name, relation=relation, age=age)
        return self.repo.create(recipient)

    def get_recipient(self, recipient_id: int) -> Optional[Recipient]:
        return self.repo.get(recipient_id)

    def get_all_recipients(self) -> list[Recipient]:
        return self.repo.get_all()

    def update_recipient(self, recipient_id: int, updates: dict) -> Optional[Recipient]:
        return self.repo.update(recipient_id, updates)

    def delete_recipient(self, recipient_id: int) -> bool:
        return self.repo.delete(recipient_id)