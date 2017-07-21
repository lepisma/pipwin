#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = [
    "argparse",
    "requests",
    "robobrowser",
    "pyprind",
    "six",
    "js2py",
    "packaging",
]

setup(
    name="pipwin",
    version="0.3.2",
    description="pipwin installs compiled python binaries on windows provided by Christoph Gohlke",
    long_description=readme,
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
    },
    classifiers=[
        "Development Status :: 3 - Alpha", "Environment :: Console",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ])
