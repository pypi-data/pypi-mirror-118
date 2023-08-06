_GIT_IGNORE = """# Development Environment
.vscode/
**/.DS_Store

# Python Files
.venv/
**/*.pyc
**/__pycache__/
*.egg*

# Testing Files
**/.coverage
**.err
"""

_SETUP_CFG = """[metadata]
name = {package_name}
author = {author_name}
author_email = {author_email}
description = {package_description}
long_description = file: README.md
long_description_content_type = text/markdown

[options]
packages = find:
install_requires =

[options.extras_require]
develop =
    nose
    nose-cov
    flake8

[nosetests]
with-coverage = True
cover-package = {package_name}
cover-erase = True
tests = tests/unit
with-doctest = True

[coverage:run]
branch = True

[coverage:report]
ignore_errors = True

[flake8]
max-line-length = 120
"""

_SETUP_PY = """from setuptools import setup

try:
    version = open('version', 'r').read().strip()
except IOError:
    version = '9999+dev'

if __name__ == "__main__":
    setup()
"""

_TEST_SH = """#!/usr/bin/env bash
set -ex

if [[ -z $VIRTUAL_ENV ]]; then
    virtualenv -p $(which python3) venv
    source venv/bin/activate
fi

pip install -e .[develop]

python setup.py nosetests || error=1

if [[ $error -ne 1 ]]; then
    flake8 {package_name}  || true
fi

exit $error
"""

_MANIFEST_IN = "include version"

TEMPLATES = {".gitignore": _GIT_IGNORE,
             "setup.py": _SETUP_PY,
             "setup.cfg": _SETUP_CFG,
             "test.sh": _TEST_SH,
             "MANIFEST.in": _MANIFEST_IN}
