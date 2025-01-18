import pytest
from _pytest.config import Config
from _pytest.terminal import TerminalReporter
from _pytest.reports import TestReport
from unittest.mock import MagicMock, patch

def test_update_progress():
    config = MagicMock(spec=Config)
    config.getini.return_value = True
    reporter = TerminalReporter(config)
    reporter._total_tests = 10
    
    with patch('sys.stdout.write') as mock_write, patch('sys.stdout.flush') as mock_flush:
        reporter._update_progress(5, 10)
        mock_write.assert_called_once_with("\033]9;4;1;50\007")
        mock_flush.assert_called_once()

def test_pytest_runtest_logreport():
    config = MagicMock(spec=Config)
    config.getini.return_value = True
    reporter = TerminalReporter(config)
    reporter._total_tests = 10
    reporter._current_test = 4
    
    report = MagicMock(spec=TestReport)
    report.when = 'call'
    
    with patch.object(reporter, '_update_progress') as mock_update:
        reporter.pytest_runtest_logreport(report)
        mock_update.assert_called_once_with(5, 10)

def test_pytest_collection_modifyitems():
    config = MagicMock(spec=Config)
    reporter = TerminalReporter(config)
    session = MagicMock()
    items = [MagicMock() for _ in range(5)]
    
    reporter.pytest_collection_modifyitems(session, config, items)
    assert reporter._total_tests == 5

