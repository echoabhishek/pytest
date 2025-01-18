
import pytest

@pytest.fixture()
def f1(request):
    return getattr(request, 'param', 0)

@pytest.fixture()
def f2():
    return 2

@pytest.fixture(name="f2")
def f2_override():
    return "named_f2"

def test_fixture_overriding(f1, f2):
    assert f1 == 0, "Explicitly named fixture f1 should take precedence"
    assert f2 == "named_f2", "Explicitly named fixture f2 should take precedence"

def test_dependent_fixture(f1, f2):
    dependent_fixture = f"{f1}_{f2}"
    assert dependent_fixture == "0_named_f2", "Dependent fixture should use explicitly named fixtures"

@pytest.mark.parametrize("f1", [3], indirect=True)
def test_parametrized(f1):
    assert f1 == 3, "Parametrized fixture should override explicitly named fixture"

@pytest.fixture()
def non_overloaded():
    return "original"

def test_non_overloaded_fixture(non_overloaded):
    assert non_overloaded == "original", "Non-overloaded fixture should keep its original value"

@pytest.fixture(scope="module")
def module_scope_fixture():
    return "module_scope"

def test_module_scope_fixture(module_scope_fixture, f1):
    assert module_scope_fixture == "module_scope", "Module scope fixture should work correctly"
    assert f1 == 0, "Function scope fixture should still be overridden"

@pytest.fixture(scope="class")
def class_scope_fixture():
    return "class_scope"

class TestClassScopeFixture:
    def test_class_scope_fixture(self, class_scope_fixture, f1):
        assert class_scope_fixture == "class_scope", "Class scope fixture should work correctly"
        assert f1 == 0, "Function scope fixture should still be overridden in class"

@pytest.fixture(autouse=True)
def autouse_fixture(request):
    f1 = request.getfixturevalue('f1')
    if 'f1' in request.fixturenames and request.node.get_closest_marker('parametrize'):
        assert f1 != 0, "Autouse fixture should use parametrized value"
    else:
        assert f1 == 0, "Autouse fixture should use overridden value"

def test_autouse_fixture():
    pass  # This test will fail if the autouse_fixture assertion fails

@pytest.mark.parametrize("f1", [4], indirect=True)
def test_direct_parametrize(f1):
    assert f1 == 4, "Direct parametrization should override named fixture"
