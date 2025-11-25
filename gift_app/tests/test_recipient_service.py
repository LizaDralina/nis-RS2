import os
import sys

import allure

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.models.domain import Recipient
from app.repositories.recipient_repo import InMemoryRecipientRepository
from app.services.recipient_service import RecipientService


@allure.epic("Gift Helper API")
@allure.feature("Business Logic")
class TestRecipientService:

    def setup_method(self):
        self.repo = InMemoryRecipientRepository()
        self.service = RecipientService(self.repo)

    @allure.story("Recipient Service")
    @allure.title("Test creating recipient via service")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_recipient(self):
        with allure.step("Create recipient through service"):
            recipient = self.service.create_recipient("Анна", "friend", 25)

        with allure.step("Verify recipient data"):
            assert recipient.id == 1
            assert recipient.name == "Анна"
            assert recipient.relation == "friend"
            assert recipient.age == 25

    @allure.story("Recipient Service")
    @allure.title("Test creating recipient without age via service")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_recipient_without_age(self):
        with allure.step("Create recipient without age"):
            recipient = self.service.create_recipient("Иван", "family")

        with allure.step("Verify recipient data with null age"):
            assert recipient.id == 1
            assert recipient.name == "Иван"
            assert recipient.relation == "family"
            assert recipient.age is None

    @allure.story("Recipient Service")
    @allure.title("Test getting existing recipient via service")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_existing_recipient(self):
        with allure.step("Create recipient first"):
            self.service.create_recipient("Анна", "friend", 25)

        with allure.step("Get recipient by ID"):
            recipient = self.service.get_recipient(1)

        with allure.step("Verify recipient data"):
            assert recipient is not None
            assert recipient.name == "Анна"

    @allure.story("Recipient Service")
    @allure.title("Test getting non-existent recipient via service")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_recipient(self):
        with allure.step("Try to get non-existent recipient"):
            recipient = self.service.get_recipient(999)

        with allure.step("Verify result is None"):
            assert recipient is None

    @allure.story("Recipient Service")
    @allure.title("Test getting all recipients via service")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_recipients_with_data(self):
        with allure.step("Create multiple recipients"):
            self.service.create_recipient("Анна", "friend", 25)
            self.service.create_recipient("Иван", "family", 30)

        with allure.step("Get all recipients"):
            recipients = self.service.get_all_recipients()

        with allure.step("Verify recipients list"):
            assert len(recipients) == 2
            assert recipients[0].name == "Анна"
            assert recipients[1].name == "Иван"


@allure.epic("Gift Helper API")
@allure.feature("Data Access Layer")
class TestInMemoryRecipientRepository:

    def setup_method(self):
        self.repo = InMemoryRecipientRepository()

    @allure.story("Repository")
    @allure.title("Test repository create operation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_recipient(self):
        with allure.step("Create recipient in repository"):
            recipient = Recipient(id=None, name="Анна", relation="friend", age=25)
            created = self.repo.create(recipient)

        with allure.step("Verify created recipient"):
            assert created.id == 1
            assert created.name == "Анна"

    @allure.story("Repository")
    @allure.title("Test repository get operation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_recipient(self):
        with allure.step("Create and then get recipient"):
            recipient = Recipient(id=None, name="Анна", relation="friend", age=25)
            self.repo.create(recipient)
            found = self.repo.get(1)

        with allure.step("Verify retrieved recipient"):
            assert found.name == "Анна"

    @allure.story("Repository")
    @allure.title("Test repository update operation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_recipient(self):
        with allure.step("Create recipient and then update"):
            self.repo.create(Recipient(id=None, name="Анна", relation="friend", age=25))
            updated = self.repo.update(1, {"name": "Анна-Мария", "age": 26})

        with allure.step("Verify updated recipient"):
            assert updated.name == "Анна-Мария"
            assert updated.age == 26

    @allure.story("Repository")
    @allure.title("Test repository delete operation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_recipient(self):
        with allure.step("Create and then delete recipient"):
            self.repo.create(Recipient(id=None, name="Анна", relation="friend", age=25))
            result = self.repo.delete(1)

        with allure.step("Verify deletion result"):
            assert result is True
            assert self.repo.get(1) is None
