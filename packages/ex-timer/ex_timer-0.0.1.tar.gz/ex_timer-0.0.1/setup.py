from setuptools import setup


__project__ = "ex_timer"
__version__ = "0.0.1"
__description__ = "ex_timer is a timer for special and non-special countdown package, for reminding you or for something else"
__packages__ = ["ex_timer"]
__author__ = "Rigved Aneesh"
__author_email__ = "rigved.bob@gmail.com"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]
__keywords__ = ["ex_timer", "timer"]
__scripts__ = ["bin/ex_timer"]
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
