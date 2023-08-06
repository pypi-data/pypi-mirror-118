import setuptools
import py2exe

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "probablyJustJordan",
    version = "1.0.0",
    author = "Jordan",
    author_email = None,
    description = "MBS Record Updater",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/probablyJustJordan/recordkeeper",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)