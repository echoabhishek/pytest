# mypy: allow-untyped-defs
from __future__ import annotations

import sys
import pytest

if sys.gettrace():
    @pytest.fixture(autouse=True)
    def restore_tracing():
        """Restore tracing function (when run with Coverage.py).

        https://bugs.python.org/issue37011
        """
        orig_trace = sys.gettrace()
        yield
        if sys.gettrace() != orig_trace:
            sys.settrace(orig_trace)

@pytest.fixture(autouse=True)
def set_column_width(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Force terminal width to 80: some tests check the formatting of --help, which is sensible
    to terminal width.
    """
    monkeypatch.setenv("COLUMNS", "80")

@pytest.fixture(autouse=True)
def reset_colors(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Reset all color-related variables to prevent them from affecting internal pytest output
    in tests that depend on it.
    """
    monkeypatch.delenv("PY_COLORS", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)

@pytest.fixture
def tw_mock():
    """Returns a mock terminal writer"""

    class TWMock:
        WRITE = object()

    return TWMock()
