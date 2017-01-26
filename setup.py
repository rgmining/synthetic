#
# setup.py
#
# Copyright (c) 2016-2017 Junpei Kawamoto
#
# This file is part of rgmining-synthetic-dataset.
#
# rgmining-synthetic-dataset is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-synthetic-dataset is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rgmining-synthetic-dataset. If not, see <http://www.gnu.org/licenses/>.
#
"""Package information about a synthetic dataset for review graph mining.
"""
from setuptools import setup, find_packages


def _load_requires_from_file(filepath):
    """Read a package list from a given file path.

    Args:
      filepath: file path of the package list.

    Returns:
      a list of package names.
    """
    with open(filepath) as fp:
        return [pkg_name.strip() for pkg_name in fp.readlines()]


setup(
    name='rgmining-synthetic-dataset',
    use_scm_version=True,
    author="Junpei Kawamoto",
    author_email="kawamoto.junpei@gmail.com",
    description="A synthetic dataset for Review graph mining project",
    url="https://github.com/rgmining/synthetic",
    py_modules=[
        "synthetic_evaluation"
    ],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "synthetic-evaluation = synthetic_evaluation:main",
        ],
    },
    setup_requires=[
        "setuptools_scm"
    ],
    install_requires=_load_requires_from_file("requirements.txt"),
    extras_require={
        "ria": ["rgmining-ria"],
        "rsd": ["rgmining-rds"],
        "fraud-eagle": ["rgmining-fraud-eagle"],
        "fraudar": ["rgmining-fraudar"],
    },
    test_suite='tests.suite',
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ]
)
