import sys
from _pytest.config import Config
from _pytest.reports import TestReport
from _pytest.main import Session
from typing import List, Any, TextIO

class TerminalReporter:
    def __init__(self, config: Config, file: TextIO | None = None) -> None:
        self.config = config
        self._numcollected = 0
        self._session: Session | None = None
        self._showfspath: bool | None = None
        self.stats: dict[str, list[Any]] = {}
        self._main_color: str | None = None
        self._total_tests = 0
        self._current_test = 0

    def _update_progress(self, current, total):
        if not self.config.getini("show_progress_in_tab"):
            return
        progress = int((current / total) * 100)
        sys.stdout.write(f"\033]9;4;1;{progress}\007")
        sys.stdout.flush()

    def pytest_runtest_logreport(self, report: TestReport) -> None:
        self._tests_ran = True
        rep = report
        res = self.config.hook.pytest_report_teststatus(report=rep, config=self.config)
        category, letter, word = res
        if not isinstance(word, tuple):
            markup = None
        else:
            word, markup = word
        self._add_stats(category, [rep])
        if not letter and not word:
            return
        if report.when == 'call':
            self._current_test += 1
            self._update_progress(self._current_test, self._total_tests)

    def pytest_collection_modifyitems(self, session: Session, config: Config, items: List[Any]) -> None:
        self._total_tests = len(items)

    def _add_stats(self, category: str, reports: List[TestReport]) -> None:
        if category not in self.stats:
            self.stats[category] = []
        self.stats[category].extend(reports)

