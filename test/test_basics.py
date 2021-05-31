import os
from time import time

import pytest
from click.testing import CliRunner

from consult import STATEMENTS_FILE, capitalize_sentences, get_babble, run_consult

IMPOSSIBLE_MATCH = "unladen swallow"


@pytest.fixture(scope="function")
def cli_runner():
    return CliRunner()


def t_impossible_match_is_impossible():
    assert IMPOSSIBLE_MATCH not in STATEMENTS_FILE.read_text()


class TestCapitalize:
    @pytest.mark.parametrize(
        "raw, fixed",
        [
            ["Spam", "Spam"],
            ["spam", "Spam"],
            ["spam, eggs. spam", "Spam, eggs. Spam"],
            ["eggs, spam? spam! spam.", "Eggs, spam? Spam! Spam."],
        ],
    )
    def t_caps(self, raw: str, fixed: str):
        assert capitalize_sentences(raw) == fixed


class TestTechnobabble:
    def t_does_not_just_break(self, trials: int = 100):
        for _ in range(trials):
            get_babble()

    def t_no_longer_than_twenty_milliseconds(self, trials: int = 5):
        for _ in range(trials):
            start = time()
            get_babble()
            elapsed = time() - start
            assert elapsed <= 0.02

    def t_matches(self):
        assert "x" in get_babble(match="x")

    def t_does_not_crash(self):
        get_babble(match=IMPOSSIBLE_MATCH)


class TestCLI:
    def t_works(self):
        exit_status = os.system("consult")
        assert exit_status == 0

    def t_works1(self):
        exit_status = os.system("python -m consult")
        assert exit_status == 0


class TestClick:
    def t_prints_single_line(self, cli_runner: CliRunner):
        result = cli_runner.invoke(run_consult, [])
        assert len(result.output.splitlines()) == 1

    @pytest.mark.parametrize("term", ["?", "x", "cross", "reading"])
    def t_prints_match(self, cli_runner: CliRunner, term: str):
        result = cli_runner.invoke(run_consult, ["--match", term])
        assert term in result.output.lower()

    def t_does_not_crash_on_bad_match(self, cli_runner: CliRunner):
        result = cli_runner.invoke(run_consult, ["--match", IMPOSSIBLE_MATCH])
        assert IMPOSSIBLE_MATCH not in result.output.lower()
