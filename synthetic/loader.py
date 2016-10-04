#
# loader.py
#
# Copyright (c) 2016 Junpei Kawamoto
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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
"""Provide a loading method of synthetic dataset.
"""
from __future__ import division
from os import path

_REVIEWER_FILE = "reviewer.dat"
_PRODUCT_FILE = "product.dat"
_REVIEW_FILE = "review.dat"


def _fullpath(filename):
    """ Compute the full path of a given filename.

    Args:
      filename: Filename.

    Returns:
      The full path of the given filename.
    """
    return path.join(path.dirname(__file__), filename)


def load(g):
    """ Load synthetic dataset.

    Args:
      g: an instance of bipartite graph.

    Returns:
      The graph instance *g*.
    """
    R = {}  # Reviewers dict.
    P = {}  # Products dict.

    # Load reviewers
    with open(_fullpath(_REVIEWER_FILE)) as fp:
        for line in fp:
            rid, name = line.strip().split(" ")
            R[rid] = g.new_reviewer(name=name)

    # Load products
    with open(_fullpath(_PRODUCT_FILE)) as fp:
        for line in fp:
            pid, name = line.strip().split(" ")
            P[pid] = g.new_product(name=name)

    # Load review
    with open(_fullpath(_REVIEW_FILE)) as fp:
        for line in fp:
            rid, pid, score = line.strip().split(" ")
            if rid not in R or pid not in P:
                continue
            g.add_review(R[rid], P[pid], float(score) / 5)

    return g
