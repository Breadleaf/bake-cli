import bake

b = bake.Bakery()


def get_version():
    """get the current version of the pyproject.toml"""
    DEFAULT_VERSION = "0.0.0"
    try:
        with open("pyproject.toml", "r") as pyproject:
            for line in pyproject:
                if line.startswith("version = "):
                    return line.split(" = ")[1].strip().strip('"')
    except FileNotFoundError:
        return DEFAULT_VERSION
    return DEFAULT_VERSION


VERSION = get_version()
DIST_DIR = "dist"


@b.target
def clean() -> bool:
    """remove all build artifacts"""
    b.shell_pass(f"rm -rf {DIST_DIR} .mypy_cache *.egg-info")
    b.shell_pass("rm -i *.pyc")

    remove_pycache = [
        "find .",
        '-name "__pycache__"',
        '-a -not -path "./.git*"',
        '-a -not -path "./venv*"',
        "| xargs rm -rf",
    ]
    b.shell_pass(" ".join(remove_pycache))

    return True


@b.target
def format() -> bool:
    """format all files in the project"""
    b.shell_pass("black . -v")
    return True


@b.target
def build() -> bool:
    """build bake distribution packages"""
    b.shell_strict("./venv/bin/python -m build")
    return True


@b.target
def type_check() -> bool:
    """ensure type checks pass with mypy"""
    b.shell_strict("./venv/bin/mypy .")
    return True


@b.target
def install() -> bool:
    """install package in editable mode"""
    b.run("clean")
    b.run("build")
    b.run("uninstall")
    b.shell_strict("./venv/bin/pip install -e .")
    return True


@b.target
def uninstall() -> bool:
    """uninstall package"""
    b.shell_strict("./venv/bin/pip uninstall -y breadmake")
    return True


@b.target
def publish() -> bool:
    """publish package to PyPI"""
    b.shell_strict("./venv/bin/python -m twine upload dist/*")
    return True


@b.target
def version() -> bool:
    """print current version"""
    print(f"Version: {VERSION}")
    return True


@b.target
def init_env() -> bool:
    """setup the python venv environment"""
    python = b.shell_strict("which python3")
    b.shell_strict(f"{python} -m venv venv")
    b.shell_strict("./venv/bin/pip install --upgrade pip")
    b.shell_strict("./venv/bin/pip install -r ./requirements.txt")
    print("To finish setup run: `source ./venv/bin/activate`")
    return True


@b.target
def minimum_python_version() -> bool:
    """use vermin to find the minimum python version"""
    find_command = [
        "find .",
        '-not -path "./.git*"',
        '-a -not -path "./venv*"',
        '-a -not -path "./.mypy*"',
        '-a -name "*.py"',
    ]

    vermin_command = [
        b.shell_strict("which vermin"),
        "--no-tips",
        "-v",
    ]

    b.shell(" ".join(find_command) + " | xargs " + " ".join(vermin_command))
    return True


if __name__ == "__main__":
    b.compile()
