
import pytest

@pytest.fixture()
def f1():
    return 1

@pytest.fixture()
def f2():
    return 2

@pytest.fixture(name="f1")
def f1_override():
    return 0

@pytest.fixture(name="f2")
def f2_override():
    return "named_f2"

def test_fixture_overriding(f1, f2):
    assert f1 == 0, "Explicitly named fixture f1 should take precedence"
    assert f2 == "named_f2", "Explicitly named fixture f2 should take precedence"

def test_dependent_fixture(f1, f2):
    dependent_fixture = f"{f1}_{f2}"
    assert dependent_fixture == "0_named_f2", "Dependent fixture should use explicitly named fixtures"

@pytest.fixture()
def parametrized_f1(request):
    return request.param

@pytest.mark.parametrize("parametrized_f1", [3], indirect=True)
def test_parametrized(parametrized_f1):
    assert parametrized_f1 == 3, "Parametrized fixture should override explicitly named fixture"

@pytest.fixture()
def non_overloaded():
    return "original"

def test_non_overloaded_fixture(non_overloaded):
    assert non_overloaded == "original", "Non-overloaded fixture should keep its original value"
