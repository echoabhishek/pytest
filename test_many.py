import pytest

@pytest.mark.parametrize("i", range(50))
def test_many(i):
    assert i < 40
