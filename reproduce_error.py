
import pytest

@pytest.fixture()
def f1():
    return 1

@pytest.fixture(name="f1")
def f1_override():
    return 0

@pytest.fixture()
def original_f1():
    return 1

class TestLib:
    def test_1(self, f1):
        assert f1 == 0

    def test_2(self, f1):
        assert f1 == 0

    def test_original_f1(self, original_f1):
        assert original_f1 == 1

if __name__ == "__main__":
    pytest.main([__file__])
