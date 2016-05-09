#!/usr/bin/env python
from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='MicroPeri',
    version='0.1',
    description='MicroPeri is quick and easy to use Python 3 library for turning the BBC Microbit into an external peripheral device or sensor.',
    long_description=readme,
    author='Andrew Mulholland, Joe Glancy',
    author_email='',
    url='https://github.com/JoeGlancy/microperi',
    scripts = [],
    license='mit',
    install_requires=['pyserial', ],
    package_data={'': ['README.rst',]},
)
