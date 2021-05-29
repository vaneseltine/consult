# import pytest

from time import time

import pytest

from consult import Technobabbler, run_consult, technobabble


class TestTechnobabble:
    def t_does_not_just_break(self, trials: int = 100):
        for _ in range(trials):
            technobabble(Technobabbler)

    def t_no_longer_than_twenty_milliseconds(self, trials: int = 5):
        for _ in range(trials):
            start = time()
            technobabble(Technobabbler)
            elapsed = time() - start
            assert elapsed <= 0.02

    def t_prints_match(self, capsys):
        technobabble(Technobabbler, match="x")
        captured = capsys.readouterr()
        assert "x" in captured.out.lower()
        assert not captured.err

    def t_does_not_crash(self, capsys):
        technobabble(Technobabbler, match="zzzzz")
        captured = capsys.readouterr()
        assert not captured.err


class TestConsult:
    def t_prints_single_line(self, cli_runner):
        result = cli_runner.invoke(run_consult, [])
        assert len(result.output.splitlines()) == 1

    @pytest.mark.parametrize("term", ["a", "j", "x", "v"])
    def t_prints_match(self, cli_runner, term: str):
        result = cli_runner.invoke(run_consult, ["--match", term])
        assert term in result.output.lower()

    @pytest.mark.parametrize("term", ["xyzzy", "aviaeur"])
    def t_does_not_crash_on_bad_match(self, cli_runner, term: str):
        result = cli_runner.invoke(run_consult, ["--match", term])
        assert term not in result.output.lower()
