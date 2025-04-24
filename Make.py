import breadmake

bm = breadmake.BreadMake()

def get_version():
    """get the current version of the pyproject.toml"""
    DEFAULT_VERSION = "0.0.0"
    try:
        with open("pyproject.toml", "r") as pyproject:
            for line in pyproject:
                if line.startswith("version = "):
                    return line.split("=")[1].strip().split("\"")
    except FileNotFoundError:
        return DEFAULT_VERSION
    return DEFAULT_VERSION

VERSION = get_version()
DIST_DIR = "dist"

@bm.target
def clean() -> bool:
    """remove all build artifacts"""
    return True

@bm.target
def build() -> bool:
    """build breadmake distribution packages"""
    return True

@bm.target
def test() -> bool:
    """ensure type checks pass with mypy"""
    return True

@bm.target
def package() -> bool:
    """build and package"""
    return True

@bm.target
def install() -> bool:
    """install package in editable mode"""
    return True

@bm.target
def uninstall() -> bool:
    """uninstall package"""
    return True

@bm.target
def publish() -> bool:
    """publish package to PyPI"""
    return True

@bm.target
def version() -> bool:
    """print current version"""
    return True

@bm.target
def init_env() -> bool:
    """setup the python venv environment"""
    return True

if __name__ == "__main__":
    bm.compile()
