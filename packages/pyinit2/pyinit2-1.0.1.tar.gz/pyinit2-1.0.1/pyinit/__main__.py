"""Initialize python package structure."""
import argparse
import logging
import os
import sys

from pyinit.io import add_file


def main():
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())

    parser = argparse.ArgumentParser(description="PyInit CLI")
    parser.add_argument("-f", dest="force", action="store_true", help="Force overwrite current files.")
    args = parser.parse_args()

    package_information = {
        "package_name": input("Package Name: "),
        "package_description": input("Package Description: "),
        "author_name": input("Author Name: "),
        "author_email": input("Author Email: "),
    }

    if (os.path.exists('setup.cfg') or os.path.exists('setup.py') or os.path.exists(package_information["package_name"])
            or os.path.exists('tests/unit') or os.path.exists('MANIFEST.in')) and args.force is False:
        logger.error('PyInit will overwrite current files. Use `-f` to run anyways.')
        sys.exit(1)

    # Add files to package
    for file_ in ["setup.py", "setup.cfg", "test.sh", ".gitignore", "MANIFEST.in"]:
        add_file(file_, package_information)

    # Intialize package and add __init__.py file
    os.mkdir(package_information["package_name"])
    open(os.path.join(package_information["package_name"], "__init__.py"), 'a').close()

    # Intialize tests and add __init__.py file
    os.makedirs("tests/unit")
    open(os.path.join("tests/unit", "__init__.py"), 'a').close()


if __name__ == "__main__":
    main()
