
import pytest

@pytest.fixture()
def f1():
    return 1

@pytest.fixture(name="f1")
def f0():
    return 0

class TestLib:
    def test_1(self, f1):
        assert f1 == 0  # This should pass after our fix
