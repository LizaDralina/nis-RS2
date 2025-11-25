import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.models.db import Base, RecipientDB
from app.models.domain import Recipient
from app.models.schemas import RecipientCreate, RecipientRead


class TestModels:
    def test_recipient_db_model(self):

        recipient = RecipientDB(id=1, name="Test User", relation="friend", age=25)
        assert recipient.id == 1
        assert recipient.name == "Test User"
        assert recipient.relation == "friend"
        assert recipient.age == 25
        assert recipient.__tablename__ == "recipients"

    def test_recipient_domain_model(self):

        recipient = Recipient(id=1, name="Test User", relation="friend", age=25)
        assert recipient.id == 1
        assert recipient.name == "Test User"
        assert recipient.relation == "friend"
        assert recipient.age == 25

    def test_recipient_domain_without_id(self):

        recipient = Recipient(id=None, name="Test User", relation="friend", age=25)
        assert recipient.id is None
        assert recipient.name == "Test User"

    def test_recipient_create_schema(self):

        schema = RecipientCreate(name="Test User", relation="friend", age=25)
        assert schema.name == "Test User"
        assert schema.relation == "friend"
        assert schema.age == 25

    def test_recipient_create_schema_without_age(self):

        schema = RecipientCreate(name="Test User", relation="friend")
        assert schema.name == "Test User"
        assert schema.relation == "friend"
        assert schema.age is None

    def test_recipient_read_schema(self):

        schema = RecipientRead(id=1, name="Test User", relation="friend", age=25)
        assert schema.id == 1
        assert schema.name == "Test User"
        assert schema.relation == "friend"
        assert schema.age == 25

    def test_base_metadata(self):

        assert hasattr(Base, "metadata")
