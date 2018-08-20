import sys
import importlib

import interface


def check_interpreter():
    """Check interpreter version."""
    pass


def check_module(name):
    """Check if necessary Python modules are installed."""
    return importlib.util.find_spec(name) is not None


def check_deps(names):
    for module in names:
        if not check_module(module):
            sys.exit(f"Need to install module {module}.")


if __name__ == "__main__":
    module_names = ["PyQt5"]
    check_interpreter()
    check_deps(module_names)
    interface.Main()
