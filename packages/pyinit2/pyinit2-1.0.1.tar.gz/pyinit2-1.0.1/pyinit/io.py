import os

from pyinit.templates import TEMPLATES


def add_file(file_name, package_information, location="."):
    """Add file to package."""
    content = TEMPLATES[file_name].format_map(package_information)

    with open(os.path.join(location, file_name), 'w') as fh:
        fh.write(content)
