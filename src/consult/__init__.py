import random
import re
from copy import deepcopy
from pathlib import Path
from platform import python_version
from typing import Dict, List, Sequence

import click
import yaml

__version__ = "0.1"

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
STATEMENTS_FILE = Path(__file__).parent / "inputs.yaml"
STATEMENTS_CONTENT: Dict[str, List[str]] = yaml.safe_load(STATEMENTS_FILE.read_text())
PROG_DIR = Path(__file__).parent


@click.command(help="Receive a quick consultation from Engineering!")
@click.option(
    "--match",
    type=str,
    default="",
    help="Try to receive consultation(s) including MATCH.",
)
@click.version_option(
    __version__,
    "--version",
    "-V",
    message=(f"%(prog)s {__version__} from {PROG_DIR} (Python {python_version()})"),
)
def run_consult(match: str = ""):
    """Simple program that greets NAME for a total of COUNT times."""
    babble = get_babble(match)
    click.echo(babble)


def get_babble(match: str = ""):
    if match:
        babble = Technobabbler.find(match)
    else:
        babble = Technobabbler().babble()
    return babble


class Technobabbler:

    _content = {**STATEMENTS_CONTENT}

    def __init__(self) -> None:
        self.content: Dict[str, List[str]] = deepcopy(self._content)
        for key in self.content:
            random.shuffle(self.content[key])

    def babble(self) -> str:
        raw_babble = self.generate("statement")
        return capitalize_sentences(raw_babble)

    @classmethod
    def find(cls, match: str = "", tries: int = 1000) -> str:
        if not match:
            return cls().babble()
        for _ in range(tries):
            attempt = cls().babble()
            if re.search(match, attempt, flags=re.IGNORECASE):
                return attempt
        return cls().generate("apology")

    def generate(self, item: str) -> str:
        if item.startswith("verb_"):
            verb_info = self.content["verb"].pop().split(",")
            verb = ModifiableVerb(verb_info)
            verb_version = item[5:]
            result = verb[verb_version]
        else:
            result = (
                self.content[item].pop()
                # if len(self.content[item]) > 1
                # else self.content[item][0]
            )
        result = result.format_map(self)
        return result

    def __getitem__(self, item: str) -> str:
        return self.generate(item)


def capitalize_sentences(complete_statement: str) -> str:
    sentence_splitter = re.compile(r"([!?.] +)")
    sentences = sentence_splitter.split(complete_statement)
    return "".join(x.capitalize() for x in sentences)


class ModifiableVerb:
    def __init__(self, verb_info: Sequence[str]):
        self.root, self.s_present, self.s_past, self.s_gerund, *prefixes = verb_info
        prefixes = prefixes or [""]
        self.prefix = random.choice(prefixes)

    @property
    def present(self):
        return self.prefix + self.root + self.s_present

    @property
    def past(self):
        return self.prefix + self.root + self.s_past

    @property
    def gerund(self):
        return self.prefix + self.root + self.s_gerund

    def __getitem__(self, version: str) -> str:
        return getattr(self, version)


if __name__ == "__main__":
    run_consult()
