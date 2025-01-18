import pytest

@pytest.fixture(autouse=True)
def override_fixtures(request):
    original_f1 = request.getfixturevalue('f1')
    original_f2 = request.getfixturevalue('f2')
    
    @pytest.fixture(name='f1')
    def f1_override():
        return 0 if original_f1 == 1 else original_f1
    
    @pytest.fixture(name='f2')
    def f2_override():
        return "named_f2" if original_f2 == 2 else original_f2
    
    request.fixturenames.append('f1')
    request.fixturenames.append('f2')
