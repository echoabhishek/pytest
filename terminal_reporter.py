import sys

class ProgressReporter:
    def __init__(self, config):
        self.enable_terminal_progress = config.getoption("enable_terminal_progress")
        self.total_tests = 0
        self.completed_tests = 0

    def pytest_collection_modifyitems(self, items):
        self.total_tests = len(items)

    def pytest_runtest_logreport(self, report):
        if self.enable_terminal_progress:
            if report.when == "call" or report.outcome == "skipped":
                self.completed_tests += 1
                self._update_progress()

    def pytest_terminal_summary(self):
        if self.enable_terminal_progress:
            self._update_progress(force_hundred=True)

    def _update_progress(self, force_hundred=False):
        if self.total_tests > 0:
            progress = 100 if force_hundred else int((self.completed_tests / self.total_tests) * 100)
            sys.stderr.write(f"\033]9;4;{progress};100\007")
            sys.stderr.flush()
        elif force_hundred:
            sys.stderr.write(f"\033]9;4;100;100\007")
            sys.stderr.flush()

