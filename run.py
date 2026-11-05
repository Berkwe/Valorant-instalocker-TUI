"""One-click launcher for Instalocker.

Double-click run.bat, or run `py run.py`. The first run creates a private
.venv and installs requirements.txt into it; later runs start straight away.
Any arguments are passed through to Instalocker.py (--agent, --mode, ...).

Keep this file free of newer syntax: it has to start on old Pythons too, so it
can find a suitable one.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "Instalocker.py"
REQUIREMENTS = ROOT / "requirements.txt"
VENV = ROOT / ".venv"
VENV_PYTHON = VENV / "Scripts" / "python.exe"
STAMP = VENV / ".requirements.sha256"

# src/app.py nests quotes inside f-strings, which is a SyntaxError before 3.12.
MIN_VERSION = (3, 12)
PY_LAUNCHER_VERSIONS = ("3.14", "3.13", "3.12")


def find_python():
    """Return the command for a new enough Python, or None."""
    if sys.version_info >= MIN_VERSION:
        return [sys.executable]
    for version in PY_LAUNCHER_VERSIONS:
        command = ["py", "-" + version]
        try:
            found = subprocess.run(command + ["-c", "pass"], capture_output=True)
        except OSError:
            return None  # no py launcher at all
        if found.returncode == 0:
            return command
    return None


def venv_is_usable():
    """False if .venv is missing, or broken (e.g. its Python was uninstalled)."""
    check = "import sys; sys.exit(sys.version_info < {!r})".format(MIN_VERSION)
    try:
        return subprocess.run([str(VENV_PYTHON), "-c", check]).returncode == 0
    except OSError:
        return False


def ensure_venv():
    if venv_is_usable():
        return True
    python = find_python()
    if python is None:
        print("Instalocker needs Python 3.12 or newer, and none was found.")
        print("Install it from https://www.python.org/downloads/ and try again.")
        return False
    print("Setting up Python environment (first run only)...")
    subprocess.check_call(python + ["-m", "venv", "--clear", str(VENV)])
    return True


def ensure_requirements():
    digest = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()
    if STAMP.exists() and STAMP.read_text().strip() == digest:
        return
    print("Installing dependencies...")
    subprocess.check_call([
        str(VENV_PYTHON), "-m", "pip", "install", "--quiet",
        "--disable-pip-version-check", "-r", str(REQUIREMENTS),
    ])
    STAMP.write_text(digest)


def main():
    try:
        if not ensure_venv():
            return 1
        ensure_requirements()
    except subprocess.CalledProcessError as error:
        print("Setup failed (exit code {}). Check your internet connection "
              "and try again.".format(error.returncode))
        return 1
    return subprocess.call([str(VENV_PYTHON), str(APP)] + sys.argv[1:], cwd=str(ROOT))


if __name__ == "__main__":
    try:
        exit_code = main()
    except KeyboardInterrupt:
        exit_code = 130
    # Keep the window open so messages like "Valorant is not open" can be read.
    try:
        input("\nPress Enter to close...")
    except (EOFError, KeyboardInterrupt):
        pass
    sys.exit(exit_code)
