import sys

import nox

# -r on CLI to override and reuse all instead
nox.options.reuse_existing_virtualenvs = False
# --no-stop-on-first-error on CLI to override
nox.options.stop_on_first_error = True

WINDOWS = sys.platform.startswith("win")


@nox.session(reuse_venv=False)
def test(session):
    session.run("poetry", "install", external=True)
    # session.install("-e", ".")
    session.run(
        "coverage",
        "run",
        "-m",
        "pytest",
    )


@nox.session()
def cli(session):
    session.run("poetry", "install", external=True)
    session.chdir("/")
    session.run("python", "-m", "consult", "--version", silent=True)
    session.run("consult", "--version", silent=True)
    session.run("consult", "--match", "diagnostic", silent=True)


@nox.session(python=False)
def lint_flake8(session):
    session.run("python", "-m", "flake8", "./src", "--show-source")


@nox.session(python=False)
def lint_pylint(session):
    session.run("pylint", "./src")  # , "-d", "import-error")


@nox.session(python=False)
def lint_black(session):
    session.run("python", "-m", "black", "./")  # , "--target-version", "py36", ".")


if __name__ == "__main__":
    sys.stderr.write(f"Invoke {__file__} by running Nox.")
    sys.exit(1)
