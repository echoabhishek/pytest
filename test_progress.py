import pytest

def test_pass():
    assert True

def test_fail():
    assert False

@pytest.mark.skip(reason="skipped test")
def test_skip():
    pass

@pytest.mark.xfail(reason="expected failure")
def test_xfail():
    assert False

def test_error():
    raise Exception("This is an error")
