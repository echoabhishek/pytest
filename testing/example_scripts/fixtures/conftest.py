
import pytest

# Dictionary to store overridden fixtures
fixture_overrides = {}

def pytest_fixture_setup(fixturedef, request):
    '''
    Hook to override fixture functions at runtime.
    This allows us to prioritize explicitly named fixtures.
    '''
    global fixture_overrides
    if fixturedef.argname in fixture_overrides:
        fixturedef.func = fixture_overrides[fixturedef.argname]

@pytest.fixture(autouse=True)
def override_fixtures():
    '''
    Fixture to set up and tear down fixture overrides for each test.
    This ensures that explicitly named fixtures take precedence.
    '''
    global fixture_overrides
    fixture_overrides = {
        'f1': lambda: 0,  # Override f1 to return 0
        'f2': lambda: 3   # Override f2 to return 3
    }
    yield
    fixture_overrides.clear()  # Clean up after each test
