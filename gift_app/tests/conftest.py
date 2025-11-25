import pytest

from app.api.recipients import repo


@pytest.fixture(autouse=True)
def clear_repository():
    repo.clear()
