import pytest
import uuid
from declare import Controller


@pytest.fixture
def controller():
    return Controller("app")


def test_controller_has_name(controller):
    assert controller.name == "app"


def test_controller_has_uuid(controller):
    assert isinstance(controller.uuid, uuid.UUID)


# Controller should be able to control a stateful
# Controller should be able to compare a desired
#     state to an existing state
