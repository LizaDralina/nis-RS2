
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.repositories.recipient_repo import InMemoryRecipientRepository
from app.models.domain import Recipient


def test_in_memory_repository():
    repo = InMemoryRecipientRepository()

    recipient = Recipient(id=None, name="Анна", relation="friend", age=25)
    created = repo.create(recipient)
    assert created.id == 1
    assert created.name == "Анна"
    print("Тест создания прошел")

    found = repo.get(1)
    assert found.name == "Анна"
    print("Тест получения прошел")

    not_found = repo.get(999)
    assert not_found is None
    print("Тест получения несуществующего прошел")

    all_recipients = repo.get_all()
    assert len(all_recipients) == 1
    assert all_recipients[0].name == "Анна"
    print("Тест получения всех прошел")

    updated = repo.update(1, {"name": "Анна-Мария"})
    assert updated.name == "Анна-Мария"
    print("Тест обновления прошел")

    deleted = repo.delete(1)
    assert deleted is True
    assert repo.get(1) is None
    print("Тест удаления прошел")


if __name__ == "__main__":
    test_in_memory_repository()