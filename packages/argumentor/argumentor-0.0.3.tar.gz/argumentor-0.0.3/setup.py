#!/usr/bin/env python
# TBlock - An anti-capitalist ad-blocker that uses the hosts file
# Copyright (C) 2021 Twann <twann@ctemplar.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Import modules

import os.path
import sys
from argumentor.__init__ import __version__

# Check if setuptools is installed

try:
    from setuptools import setup
except ImportError:
    setup = None
    sys.exit("Error: setuptools is not installed\nTry to run python -m pip install setuptools --upgrade")

# Open README to define long description

with open(os.path.join(os.path.dirname(__file__), "README.md"), "rt") as readme:
    long_description = readme.read()

setup(
        name="argumentor",
        version=__version__,
        description="A library to work with command-line arguments",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://codeberg.org/twann/python-argumentor",
        author="Twann",
        author_email="twann@ctemplar.com",
        license="GPLv3",
        packages=["argumentor"],
        classifiers=[
            "Environment :: Console",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: OS Independent",
        ],
)
