#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    "argparse",
    "requests",
    "beautifulsoup4",
    "pyprind"
]

setup(
    name="pipwin",
    version="0.1.4",
    description="pipwin installs compiled python binaries on windows provided by Christoph Gohlke",
    long_description=readme + "\n\n" + history,
    author="lepisma",
    author_email="abhinav.tushar.vs@gmail.com",
    url="https://github.com/lepisma/pipwin",
    include_package_data=True,
    install_requires=requirements,
    packages=[
        "pipwin",
    ],
    license="BSD",
    zip_safe=False,
    keywords="pipwin windows binaries",
    entry_points={
        "console_scripts": ["pipwin=pipwin.command:main"],
    }
)
