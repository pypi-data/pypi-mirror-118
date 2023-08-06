import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lazyt",
    version="1.1.1",
    description="Usefull methods cause i'm lazy and they made everything easier and fancier(check project link for a decent README)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ThomasAndreatta/lazyt",
    author="Andreatta",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["lazyt"],
    include_package_data=True,
    install_requires=["sty"],
    #entry_points={"console_scripts": [ "lazyt=lazyt.__main__:main", ] },
)
