
import pytest

@pytest.fixture()
def f1():
    return 1

@pytest.fixture()
def f2():
    return 2

@pytest.fixture()
def f3():
    return 3

class TestLib:
    @pytest.fixture(name="f1")
    def f1_override(self):
        return 0

    @pytest.fixture(name="f2")
    def f2_override(self):
        return 3

    def test_1(self, f1):
        assert f1 == 0, "Fixture with explicitly set name should override"

    def test_2(self, f2):
        assert f2 == 3, "Fixture with explicitly set name should override"

    def test_3(self, f3):
        assert f3 == 3, "Fixture without explicitly set name should work normally"

if __name__ == "__main__":
    pytest.main([__file__])
