# mypy: allow-untyped-defs
from __future__ import annotations

from collections.abc import Sequence
import dataclasses
import importlib.metadata
import os
from pathlib import Path
import re
import sys
import textwrap
from typing import Any

import _pytest._code
from _pytest.config import _get_plugin_specs_as_list
from _pytest.config import _iter_rewritable_modules
from _pytest.config import _strtobool
from _pytest.config import Config
from _pytest.config import ConftestImportFailure
from _pytest.config import ExitCode
from _pytest.config import parse_warning_filter
from _pytest.config.argparsing import get_ini_default_for_type
from _pytest.config.argparsing import Parser
from _pytest.config.exceptions import UsageError
from _pytest.config.findpaths import determine_setup
from _pytest.config.findpaths import get_common_ancestor
from _pytest.config.findpaths import locate_config
from _pytest.monkeypatch import MonkeyPatch
from _pytest.pathlib import absolutepath
from _pytest.pytester import Pytester
import pytest


class TestParseIni:
    @pytest.mark.parametrize(
        "section, filename", [("pytest", "pytest.ini"), ("tool:pytest", "setup.cfg")])
    def test_getcfg_and_config(
        self,
        pytester: Pytester,
        tmp_path: Path,
        section: str,
        filename: str,
        monkeypatch: MonkeyPatch,
    ) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        monkeypatch.chdir(sub)
        (tmp_path / filename).write_text(
            textwrap.dedent(
                f"""\
                [{section}]
                name = value
                """
            ),
            encoding="utf-8",
        )
        _, _, cfg = locate_config(Path.cwd(), [sub])
        assert cfg["name"] == "value"
        config = pytester.parseconfigure(str(sub))
        assert config.inicfg["name"] == "value"

    def test_setupcfg_uses_toolpytest_with_pytest(self, pytester: Pytester) -> None:
        p1 = pytester.makepyfile("def test(): pass")
        pytester.makefile(
            ".cfg",
            setup=f"""
                [tool:pytest]
                testpaths={p1.name}
                [pytest]
                testpaths=ignored
        """,
        )
        result = pytester.runpytest()
        result.stdout.fnmatch_lines(["configfile: setup.cfg", "* 1 passed in *"])
        assert result.ret == 0

    def test_append_parse_args(
        self, pytester: Pytester, tmp_path: Path, monkeypatch: MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PYTEST_ADDOPTS", '--color no -rs --tb="short"')
        tmp_path.joinpath("pytest.ini").write_text(
            textwrap.dedent(
                """\
                [pytest]
                addopts = --verbose
                """
            ),
            encoding="utf-8",
        )
        config = pytester.parseconfig(tmp_path)
        assert config.option.color == "no"
        assert config.option.reportchars == "s"
        assert config.option.tbstyle == "short"
        assert config.option.verbose

    def test_tox_ini_wrong_version(self, pytester: Pytester) -> None:
        pytester.makefile(
            ".ini",
            tox="""
            [pytest]
            minversion=999.0
        """,
        )
        result = pytester.runpytest()
        assert result.ret != 0
        result.stderr.fnmatch_lines(
            ["*tox.ini: 'minversion' requires pytest-999.0, actual pytest-*"])

    @pytest.mark.parametrize(
        "section, name",
        [
            ("tool:pytest", "setup.cfg"),
            ("pytest", "tox.ini"),
            ("pytest", "pytest.ini"),
            ("pytest", ".pytest.ini"),
        ],
    )
    def test_ini_names(self, pytester: Pytester, name, section) -> None:
        pytester.path.joinpath(name).write_text(
            textwrap.dedent(
                f"""
            [{section}]
            minversion = 3.36
        """
            ),
            encoding="utf-8",
        )
        config = pytester.parseconfig()
        assert config.getini("minversion") == "3.36"

    def test_pyproject_toml(self, pytester: Pytester) -> None:
        pyproject_toml = pytester.makepyprojecttoml(
            """
            [tool.pytest.ini_options]
            minversion = "1.0"
        """
        )
        config = pytester.parseconfig()
        assert config.inipath == pyproject_toml
        assert config.getini("minversion") == "1.0"

    def test_empty_pyproject_toml(self, pytester: Pytester) -> None:
        """An empty pyproject.toml is considered as config if no other option is found."""
        pyproject_toml = pytester.makepyprojecttoml("")
        config = pytester.parseconfig()
        assert config.inipath == pyproject_toml

    def test_empty_pyproject_toml_found_many(self, pytester: Pytester) -> None:
        """
        In case we find multiple pyproject.toml files in our search, without a [tool.pytest.ini_options]
        table and without finding other candidates, the closest to where we started wins.
        """
        pytester.makefile(
            ".toml",
            **{
                "pyproject": "",
                "foo/pyproject": "",
                "foo/bar/pyproject": "",
            },
        )
        config = pytester.parseconfig(pytester.path / "foo/bar")
        assert config.inipath == pytester.path / "foo/bar/pyproject.toml"

    def test_pytest_ini_trumps_pyproject_toml(self, pytester: Pytester) -> None:
        """A pytest.ini always take precedence over a pyproject.toml file."""
        pytester.makepyprojecttoml("[tool.pytest.ini_options]")
        pytest_ini = pytester.makefile(".ini", pytest="")
        config = pytester.parseconfig()
        assert config.inipath == pytest_ini

    def test_toxini_before_lower_pytestini(self, pytester: Pytester) -> None:
        sub = pytester.mkdir("sub")
        sub.joinpath("tox.ini").write_text(
            textwrap.dedent(
                """
            [pytest]
            minversion = 2.0
        """
            ),
            encoding="utf-8",
        )
        pytester.path.joinpath("pytest.ini").write_text(
            textwrap.dedent(
                """
            [pytest]
            minversion = 1.5
        """
            ),
            encoding="utf-8",
        )
        config = pytester.parseconfigure(sub)
        assert config.getini("minversion") == "2.0"

    def test_ini_parse_error(self, pytester: Pytester) -> None:
        pytester.path.joinpath("pytest.ini").write_text(
            "addopts = -x", encoding="utf-8"
        )
        result = pytester.runpytest()
        assert result.ret != 0
        result.stderr.fnmatch_lines("ERROR: *pytest.ini:1: no section header defined")

    def test_toml_parse_error(self, pytester: Pytester) -> None:
        pytester.makepyprojecttoml(
            """
            \\"
            """
        )
        result = pytester.runpytest()
        assert result.ret != 0
        result.stderr.fnmatch_lines("ERROR: *pyproject.toml: Invalid statement*")

    def test_confcutdir(self, pytester: Pytester) -> None:
        sub = pytester.mkdir("sub")
        os.chdir(sub)
        pytester.makeini(
            """
            [pytest]
            addopts = -v
        """
        )
        result = pytester.inline_run("--confcutdir=.")
    @pytest.mark.parametrize(
        "ini_file_text, invalid_keys, warning_output, exception_text",
        [
            pytest.param(
                """
                [pytest]
                unknown_ini = value1
                another_unknown_ini = value2
                """,
                ["unknown_ini", "another_unknown_ini"],
                [
                    "=*= warnings summary =*=",
                    "*PytestConfigWarning:*Unknown config option: another_unknown_ini",
                    "*PytestConfigWarning:*Unknown config option: unknown_ini",
                ],
                None,
                id="2-unknowns"
            ),
            pytest.param(
                """
                [pytest]
                unknown_ini = value1
                minversion = 5.0.0
                """,
                ["unknown_ini"],
                [
                    "=*= warnings summary =*=",
                    "*PytestConfigWarning:*Unknown config option: unknown_ini",
                ],
                "Unknown config option: unknown_ini",
                id="1-unknown"
            ),
            pytest.param(
                """
                [some_other_header]
                unknown_ini = value1
                [pytest]
                minversion = 5.0.0
                """,
                [],
                [],
                None,
                id="no-unknowns"
            ),
        ]
    )
    def test_unknown_ini_warning(self, pytester, ini_file_text, invalid_keys, warning_output, exception_text):
        pytester.makeini(ini_file_text)
        result = pytester.runpytest()
        if exception_text:
            result.stdout.fnmatch_lines([f"*{exception_text}*"])
        else:
            result.stderr.no_fnmatch_line("*Unknown config option*")
        if warning_output:
            result.stdout.fnmatch_lines(warning_output)
        else:
            result.stdout.no_fnmatch_line("*PytestConfigWarning*")
