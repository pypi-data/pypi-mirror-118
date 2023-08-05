from setuptools import setup


__project__ = "ex_battleship"
__version__ = "0.0.4"
__description__ = "ex_battleship is a free package to play the game Battleship, this is version 1, it may be different, you have to guess where the one and only ship (computer's ship) is. After you guess the first one, and it'll be easy!"
__packages__ = ["ex_battleship"]
__author__ = "Rigved Aneesh"
__author_email__ = "rigved.bob@gmail.com"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]
__keywords__ = ["battleship", "game"]
__scripts__ = ["bin/battleship"]
setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    keywords = __keywords__,
    scripts = __scripts__
)


