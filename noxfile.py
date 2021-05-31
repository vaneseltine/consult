import sys

import nox

# -r on CLI to override and reuse all instead
nox.options.reuse_existing_virtualenvs = False
# --no-stop-on-first-error on CLI to override
nox.options.stop_on_first_error = True


@nox.session()
def test(session: nox.Session):
    session.run("poetry", "install", external=True)
    session.run("python", "-m", "coverage", "run", "-m", "pytest")
    session.run("coverage", "report")
    session.run("coverage", "html")


@nox.session()
def cli(session: nox.Session):
    session.run("poetry", "install", external=True)
    session.chdir("/")
    session.run("python", "-m", "consult", "--version", silent=True)
    session.run("consult", "--version", silent=True)
    session.run("consult", "--match", "diagnostic", silent=True)


@nox.session(python=False)
def lint_pylint(session: nox.Session):
    session.run("pylint", "./src")


@nox.session(python=False)
def lint_typing(session: nox.Session):
    session.run("python", "-m", "mypy", "./src")


@nox.session(python=False)
def lint_imports(session: nox.Session):
    session.run("python", "-m", "isort", "./")


@nox.session(python=False)
def lint_black(session: nox.Session):
    session.run("python", "-m", "black", "./")


@nox.session(python=False)
def poetry_requirements(session: nox.Session):
    session.run("poetry", "export", "-o", "requirements.txt")
    session.run("poetry", "export", "--dev", "-o", "requirements-dev.txt")


if __name__ == "__main__":
    sys.stderr.write(f"Invoke {__file__} by running Nox.")
    sys.exit(1)
