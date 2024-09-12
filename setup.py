import setuptools

import pathlib

PROJECT_NAME = "place project name here"
VERSION = "0.0.0"
SHORT_DESCRIPTION = "This is a short description of what the app does."
SOURCE_CODE_LINK= ""
DOCUMENTATION_LINK = "" 
REQUIRED_DEPENDANCIES = []


setuptools.setup(
    name = PROJECT_NAME,
    version = VERSION,
    description= SHORT_DESCRIPTION,
    long_description= pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author = "Ben Payton",
    project_urls = {
        "Documentation" : DOCUMENTATION_LINK,
        "Source" : SOURCE_CODE_LINK
    },
    install_requires = REQUIRED_DEPENDANCIES,
    packages=setuptools.find_packages()
    )