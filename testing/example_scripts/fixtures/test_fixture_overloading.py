
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

@pytest.fixture()
def dependent_fixture(f1):
    return f1 * 2

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

    def test_dependent_fixture(self, dependent_fixture):
        assert dependent_fixture == 0  # 0 * 2 = 0

@pytest.mark.parametrize("fixture_name,expected_value", [
    ("f1", 0),
    ("f2", 3),
    ("f4", 4)
])
def test_parametrized(fixture_name, expected_value, request):
    value = request.getfixturevalue(fixture_name)
    assert value == expected_value

def test_fixture_order(f1, f2, f4):
    assert (f1, f2, f4) == (0, 3, 4)

@pytest.fixture()
def dynamic_fixture(request):
    return request.getfixturevalue('f1') + request.getfixturevalue('f2')

def test_dynamic_fixture(dynamic_fixture):
    assert dynamic_fixture == 3  # 0 + 3 = 3

class TestNestedFixtures:
    @pytest.fixture()
    def nested_f1(self):
        return 10

    def test_nested(self, f1, nested_f1):
        assert f1 == 0
        assert nested_f1 == 10
