import pytest

@pytest.fixture()
def f1_factory():
    def _factory(override=False):
        return 0 if override else 1
    return _factory

class TestLib:
    def test_original(self, f1_factory):
        f1 = f1_factory()
        assert f1 == 1

    def test_overridden(self, f1_factory):
        f1 = f1_factory(override=True)
        assert f1 == 0

