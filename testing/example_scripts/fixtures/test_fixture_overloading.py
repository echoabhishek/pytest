
import pytest

@pytest.fixture()
def f1():
    return 1

@pytest.fixture(name="f1")
def f0():
    return 0

@pytest.fixture()
def f2():
    return 2

@pytest.fixture(name="f2")
def f3():
    return 3

@pytest.fixture()
def f4():
    return 4

class TestLib:
    def test_1(self, f1):
        assert f1 == 0

    def test_2(self, f2):
        assert f2 == 3

    def test_3(self, f1, f2):
        assert f1 == 0
        assert f2 == 3

    def test_4(self, f4):
        assert f4 == 4

    def test_5(self, f1, f2, f4):
        assert f1 == 0
        assert f2 == 3
        assert f4 == 4

@pytest.mark.parametrize("fixture_name,expected_value", [
    ("f1", 0),
    ("f2", 3),
    ("f4", 4)
])
def test_parametrized(fixture_name, expected_value, request):
    value = request.getfixturevalue(fixture_name)
    assert value == expected_value
