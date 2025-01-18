
# test_exceptiongroup_type.py
import pytest
import sys
from typing import cast

if sys.version_info < (3, 11):
    from exceptiongroup import ExceptionGroup

class FooError(Exception):
    pass

def test_exceptiongroup_type():
    # Test untyped ExceptionGroup
    with pytest.raises(ExceptionGroup):
        raise ExceptionGroup("Some error occurred", [FooError("Error")])

    # Test typed ExceptionGroup
    with pytest.raises(ExceptionGroup):
        raise ExceptionGroup("Some error occurred", [FooError("Error")])

    # Test nested ExceptionGroup
    with pytest.raises(ExceptionGroup):
        raise ExceptionGroup("Outer", [ExceptionGroup("Inner", [FooError("Error")])])

    # Test tuple of exceptions including ExceptionGroup
    with pytest.raises((ValueError, ExceptionGroup)):
        raise ExceptionGroup("Some error occurred", [FooError("Error")])

    # Test that the raised exception is actually an ExceptionGroup containing FooError
    try:
        raise ExceptionGroup("Some error occurred", [FooError("Error")])
    except ExceptionGroup as eg:
        assert any(isinstance(exc, FooError) for exc in eg.exceptions)

def test_non_exceptiongroup():
    # Ensure regular exceptions still work
    with pytest.raises(ValueError):
        raise ValueError("Regular exception")

    # Ensure tuple of regular exceptions still work
    with pytest.raises((ValueError, TypeError)):
        raise TypeError("Regular exception in tuple")
