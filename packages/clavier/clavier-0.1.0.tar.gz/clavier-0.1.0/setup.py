import setuptools
from pathlib import Path

with open(Path(__file__).parent / "README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clavier",
    version="0.1.0",
    author="Neil Souza, Expanded Performance Inc",
    author_email="src@expand.live",
    description="A light and not-so-bright CLI framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/experf/clavier",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
    ],
    # NOTE  This is a guess. I haven't explored using old Python versions. Core
    #       support 3.8 and 3.9. As of writing (2021-08-28) 3.6 is the oldest
    #       Python supported, and it has `typing`, so I've put that.
    python_requires='>=3.6',
    install_requires=[
        # Pretty terminal printing
        "rich>=9.13.0,<10",
        # Automatic argument completion for `builtins.argparse`
        "argcomplete>=1.12.1,<2",
        # Used for _creating_ Markdown, believe it or not
        "mdutils>=1.3.0,<2",
        # Sorted containers used in `clavier.cfg`
        "sortedcontainers>=2.3.0,<3",
    ],
)
