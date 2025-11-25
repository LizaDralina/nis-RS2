from typing import Any, Dict, List, Optional

from app.models.domain import Recipient


class InMemoryRecipientRepository:
    def __init__(self) -> None:
        self.storage: Dict[int, Recipient] = {}
        self.next_id: int = 1

    def create(self, recipient: Recipient) -> Recipient:
        new_recipient = Recipient(
            id=self.next_id,
            name=recipient.name,
            relation=recipient.relation,
            age=recipient.age,
        )
        self.storage[self.next_id] = new_recipient
        self.next_id += 1

        return new_recipient

    def get(self, recipient_id: int) -> Optional[Recipient]:
        return self.storage.get(recipient_id)

    def get_all(self) -> List[Recipient]:
        return list(self.storage.values())

    def update(self, recipient_id: int, updates: Dict[str, Any]) -> Optional[Recipient]:
        if recipient_id not in self.storage:
            return None

        current = self.storage[recipient_id]

        name = updates.get("name", current.name)
        relation = updates.get("relation", current.relation)
        age = updates.get("age", current.age)

        updated_recipient = Recipient(
            id=current.id,
            name=str(name),
            relation=str(relation),
            age=(age if age is None or isinstance(age, int) else current.age),
        )

        self.storage[recipient_id] = updated_recipient
        return updated_recipient

    def delete(self, recipient_id: int) -> bool:
        if recipient_id in self.storage:
            del self.storage[recipient_id]
            return True
        return False

    def clear(self) -> None:
        self.storage.clear()
        self.next_id = 1
