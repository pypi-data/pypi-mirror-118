import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
REQUIRE = (HERE / "requirements.txt").read_text().splitlines()
REQUIRE = [x.strip() for x in REQUIRE]

# This call to setup() does all the work
setup(
    name="huputs",
    version="0.1.1",
    description="Human-Understandable Python Unit Test System",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/windowsboy111/huputs",
    author="windowsboy111",
    author_email="wboy111@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["huputs"],
    install_requires=["colorama"]
)
