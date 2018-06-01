#!/usr/bin/env python

from os import path
from setuptools import setup, find_packages

__folder__ = path.dirname(__file__)

with open(path.join(__folder__, 'README.md')) as ld_file:
    long_description = ld_file.read()
    ld_file.flush()

setup(
    name='POLAR',
    version="0.1",
    description='POLAR - Path Of LeAst Resistance',
    long_description=long_description,
    author='ezrac',
    author_email='',
    packages=find_packages(),
    py_modules=['polar'],
    entry_points={
        'console_scripts': [
            'polar-parse = polar:parse_main',
        ]
    },
    install_requires=[
        'r2pipe >= 0.9.9',
        'neomodel >= 3.2.8',
    ],
    license="",
    platforms='any',
    url='https://github.com/ezrac/POLAR',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Topic :: Security',
    ]
)
