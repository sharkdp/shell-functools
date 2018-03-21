#!/usr/bin/env python
from __future__ import absolute_import, print_function
import os

from setuptools import setup, find_packages

from ft import ft

NAME = 'shell-functools'
VERSION = ft.__version__
PACKAGES = find_packages(
    'ft', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']
)
PACKAGE_DIR = {
    '': 'ft'
}
PACKAGE_DATA = {
    '': ['']
}
AUTHOR = 'David Peter'
AUTHOR_EMAIL = 'mail@david-peter.de'
URL = 'https://github.com/sharkdp/shell-functools'


REQUIRES = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt', 'r') as ifile:
        for line in ifile:
            REQUIRES.append(line.strip())
DESCRIPTION = 'A collection of functional programming tools for the shell.'
KEYWORDS = 'shell functional-programming filesystem string-manipulation command-line'
with open('README.md') as ifile:
    LONG_DESC = ifile.read()

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    url=URL,
    keywords=KEYWORDS,
    license='MIT',
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    install_requires=REQUIRES,
    python_requires='>=3.5',
    scripts=[
        'ft/filter',
        'ft/foldl',
        'ft/ft-functions',
        'ft/map',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
    ],
)
