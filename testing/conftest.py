import pytest

@pytest.fixture(autouse=True)
def override_fixtures(request):
    def get_fixture_value(name):
        try:
            return request.getfixturevalue(name)
        except pytest.FixtureLookupError:
            return None

    original_f1 = get_fixture_value('f1')
    original_f2 = get_fixture_value('f2')
    
    @pytest.fixture(name='f1')
    def f1_override():
        if 'f1' in request.fixturenames and request.param_index is not None:
            return request.param
        return 0 if original_f1 == 1 else original_f1
    
    @pytest.fixture(name='f2')
    def f2_override():
        return "named_f2" if original_f2 == 2 else original_f2
    
    request.fixturenames.append('f1')
    request.fixturenames.append('f2')
