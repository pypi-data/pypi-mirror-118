import pytest
import uuid
from declare import BaseClass


@pytest.fixture
def base():
    return BaseClass("base")


def test_base_has_name(base):
    assert base.name == "base"


def test_base_has_uuid(base):
    assert isinstance(base.uuid, uuid.UUID)
