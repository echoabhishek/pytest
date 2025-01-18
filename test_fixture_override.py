import pytest

@pytest.fixture(scope="module")
def f1():
    return 1

@pytest.fixture(scope="function", name="f1", autouse=True)
def f1_override():
    return 0

class TestLib:
    def test_overridden(self, f1):
        assert f1 == 0

    def test_original(self, request):
        original_f1 = request.getfixturevalue("f1")
        assert original_f1 == 0  # This should now use the overridden fixture

