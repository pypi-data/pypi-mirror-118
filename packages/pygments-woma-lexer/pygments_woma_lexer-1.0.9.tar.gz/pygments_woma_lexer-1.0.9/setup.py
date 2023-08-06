
from pathlib import Path
from setuptools import setup, find_packages

__version__ = '1.0.9'
__title__ = 'pygments_woma_lexer'
__description__ = "A pygments lexer for the Woma Programming Language"
__author__ = 'Ross J. Duff'
__license__ = "MIT"


def read(fname):
    return open(Path(fname).absolute()).read()


setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email="rjdbcm@mail.umkc.edu",
    description=__description__,
    license=__license__,
    keywords="lexer",
    url="https://github.com/rjdbcm/pygments_woma_lexer",
    install_requires=read('requirements.txt'),
    packages=find_packages(),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Other",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
