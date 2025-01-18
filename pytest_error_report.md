
# Pytest Configuration Error Report

## Issue Description

When attempting to run pytest, the following error occurs:

```
ERROR: while parsing the following warning configuration:

  default::pytest.PytestFDWarning

This error occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.10/dist-packages/_pytest/config/__init__.py", line 1918, in parse_warning_filter
    category: type[Warning] = _resolve_warning_category(category_)
  File "/usr/local/lib/python3.10/dist-packages/_pytest/config/__init__.py", line 1957, in _resolve_warning_category
    cat = getattr(m, klass)
AttributeError: module 'pytest' has no attribute 'PytestFDWarning'. Did you mean: 'PytestWarning'?
```

## Environment Information

- Python version: 3.10
- Pytest version: 8.3.4

## Steps to Reproduce

1. Create a minimal test file:

```python
import pytest

def test_simple():
    assert True

if __name__ == "__main__":
    pytest.main([__file__])
```

2. Run the test file using Python:

```
python3 minimal_test.py
```

3. The error occurs before any tests are run.

## Additional Information

- This error occurs even with a minimal test file and no custom configuration.
- The error mentions 'PytestFDWarning', which doesn't seem to be a standard pytest warning.
- We've checked pyproject.toml and tox.ini files, but found no relevant configuration that could cause this issue.

## Possible Causes

The error suggests that there might be a mismatch between the installed pytest version and the expected warnings. It's possible that:

1. There's a conflict between installed pytest versions.
2. A plugin or external configuration is trying to use a non-existent warning type.
3. There's an issue with the pytest installation itself.

## Request for Assistance

We would appreciate any guidance on how to resolve this issue or further steps to diagnose the problem. Thank you for your time and assistance.
