#  Qolor Tyme - a Toastmaters-inspired speech timer for online scrum meetings.
#  Copyright (C) 2021 Tromgy (tromgy@yahoo.com)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os.path
from setuptools import setup

# The directory containing this file
this_dir = os.path.abspath(os.path.dirname(__file__))

# The content of the README file
with open(os.path.join(this_dir, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="qolor-tyme",
    version="1.0.1",
    description="A Toastmasters-inspired speech timer for online scrum meetings",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tromgy/qolor-tyme",
    author="Tromgy",
    author_email="tromgy@yahoo.com",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["qolor_tyme"],
    include_package_data=True,
    install_requires=["PyQt5"],
    keywords='pyqt5 scrum toastmasters-timer'
)