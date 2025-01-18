import pytest

def test_fixture_overriding(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.fixture()
        def f1():
            return 1

        @pytest.fixture(name="f1")
        def f0():
            return 0

        def test_1(f1):
            assert f1 == 0
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

def test_fixture_overriding_in_different_scopes(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.fixture(scope="module")
        def f1():
            return 1

        @pytest.fixture(name="f1")
        def f0():
            return 0

        def test_1(f1):
            assert f1 == 0

        def test_2(f1):
            assert f1 == 0
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)
