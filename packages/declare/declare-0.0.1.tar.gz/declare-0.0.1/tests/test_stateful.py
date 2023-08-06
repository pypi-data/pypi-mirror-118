import pytest
import uuid
from declare import Stateful


@pytest.fixture
def stateful():
    return Stateful("app")


def test_stateful_has_name(stateful):
    assert stateful.name == "app"


def test_controller_has_uuid(stateful):
    assert isinstance(stateful.uuid, uuid.UUID)


# Stateful should have CRUD methods
# A list method is also probably useful
