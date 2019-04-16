#!/usr/bin/env python3
import sys
import importlib.util

import interface
from files import FilesAggregator


DEPENDENCIES = "PyQt5",


def check_interpreter():
    """Check interpreter version."""
    message = "Python interpreter version should be 3.5 or newer. Your version is %d.%d" % (sys.version_info.major,
                                                                                            sys.version_info.minor)
    if sys.version_info.major < 3:
        sys.exit(message)
    elif sys.version_info.minor < 5:
        sys.exit(message)


def check_module(name):
    """Check if necessary Python module is installed."""
    return importlib.util.find_spec(name) is not None


def check_deps(names):
    not_installed = []
    for module in names:
        if not check_module(module):
            not_installed.append(module)
    if not_installed:
        sys.exit(f"Need to install following module(s): {', '.join(not_installed)}.")


if __name__ == "__main__":
    check_interpreter()
    check_deps(DEPENDENCIES)
    interface.start(FilesAggregator)
