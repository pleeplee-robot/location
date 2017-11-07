#!/usr/bin/env python

import io
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

path_readme = os.path.join(os.path.dirname(__file__), 'README.md')
try:
    import pypandoc
    README = pypandoc.convert(path_readme, 'rst')
except (IOError, ImportError):
    with io.open(path_readme, encoding='utf-8') as readme:
        README = readme.read()

VERSION = "0.1.0"

setup(
    name='pleeplee-location',
    version=VERSION,
    license='MIT License',
    packages=['pleeplee'],
    include_package_data=True,
    zip_safe=False,  # Because of the certificate
    install_requires=[
        'sphinx',
        'sphinxcontrib-napoleon',
        'pytest',
        'pytest-mock',
        'shapely'
        ],
    description='PleePlee robot API for location',
    long_description=README,
    author='Loic BANET',
    author_email='loic.banet@gmail.com',
    url='https://github.com/pleeplee-robot/location',
    keywords=['pleeplee', 'robot', 'gardening', 'location'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Framework :: Robot Framework',
        'Framework :: Robot Framework :: Tool',
        'Development Status :: 1 - Planning'
    ]
)
