import os
from typing import List, Union
from setuptools import setup, find_packages

BASE_PATH = os.path.abspath(os.path.dirname(__file__))


def _read_readme() -> Union[str, None]:
    """Read the readme as a string"""
    try:
        with open(os.path.join(BASE_PATH, 'README.md'), 'r') as readme_file:
            return readme_file.read()
    except FileNotFoundError:
        return None


def _read_requirements() -> Union[List[str], None]:
    """Read the requriements as a list of required values"""
    try:
        with open(os.path.join(BASE_PATH, 'requirements.txt'), 'r') as reqs:
            return [line.strip() for line in reqs]
    except FileNotFoundError:
        return None


def _get_version() -> str:
    """Get the version string from inside the module"""
    from wordle import __version__
    return __version__


setup(
    name='wordle-cli',
    version=_get_version(),
    description='A Wordle Clone for your Terminal, written in Python.',
    long_description=_read_readme(),
    author='Jack McVeigh',
    author_email='jmcveigh55@gmail.com',
    packages=find_packages(),
    package_data={
        'wordle': [
            'data/wordle_list.txt',
            'data/words_list.txt'
        ]
    },
    entry_points={
        'console_scripts': [
            'wordle-cli=wordle.cli:entry_point',
        ],
    },
    install_requires=_read_requirements()
)
