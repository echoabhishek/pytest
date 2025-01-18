import pytest

@pytest.fixture(scope="module")
def f1():
    return 1

@pytest.fixture(scope="function", name="f1", autouse=True)
def f1_override():
    return 0

@pytest.fixture(scope="module")
def non_overridden():
    return "original"

class TestLib:
    def test_overridden(self, f1):
        assert f1 == 0

    def test_original(self, request):
        original_f1 = request.getfixturevalue("f1")
        assert original_f1 == 0

    @pytest.mark.parametrize("expected", [0])
    def test_parametrized(self, f1, expected):
        assert f1 == expected

    def test_non_overridden(self, non_overridden):
        assert non_overridden == "original"

    class NestedTest:
        def test_nested(self, f1):
            assert f1 == 0

def test_outside_class(f1):
    assert f1 == 0

