import pytest
from terminal_reporter import ProgressReporter

def pytest_addoption(parser):
    parser.addoption(
        "--enable-terminal-progress",
        action="store_true",
        default=False,
        help="Enable progress reporting in terminal tab"
    )

@pytest.fixture
def enable_terminal_progress(request):
    return request.config.getoption("--enable-terminal-progress")

def pytest_configure(config):
    if config.getoption("enable_terminal_progress"):
        progress_reporter = ProgressReporter(config)
        config.pluginmanager.register(progress_reporter, "progress_reporter")

