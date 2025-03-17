#
#  loader.py
#
#  Copyright (c) 2016-2025 Junpei Kawamoto
#
#  This file is part of rgmining-synthetic-dataset.
#
#  rgmining-synthetic-dataset is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  rgmining-synthetic-dataset is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with rgmining-synthetic-dataset. If not, see <http://www.gnu.org/licenses/>.
#
"""Provide a loading method of synthetic dataset."""

from os import path
from typing import Any, Final, Protocol, TypeVar

_REVIEWER_FILE: Final = "reviewer.dat"
_PRODUCT_FILE: Final = "product.dat"
_REVIEW_FILE: Final = "review.dat"


def _fullpath(filename: str) -> str:
    """Compute the full path of a given filename.

    Args:
      filename: Filename.

    Returns:
      The full path of the given filename.
    """
    return path.join(path.dirname(__file__), filename)


RT = TypeVar("RT")
PT = TypeVar("PT")


class Graph(Protocol[RT, PT]):
    """Protocol that a bipartite graph needs to provide."""

    def new_reviewer(self, name: str) -> RT:
        """Add a new reviewer to this graph.

        Args:
          name: Name of the new reviewer.

        Returns:
          The new created reviewer.
        """

    def new_product(self, name: str) -> PT:
        """Add a new product to this graph.

        Args:
          name: Name of the new product.

        Returns:
          The new created product.
        """

    def add_review(self, reviewer: RT, product: PT, score: float) -> Any:
        """Add a new review from the given reviewer to the given product.

        Args:
          reviewer: Reviewer who posts the review.
          product: Product which receives the review.
          score: The review score.
        Returns:
          The added review
        """


GT = TypeVar("GT", bound=Graph)


def load(g: GT) -> GT:
    """Load synthetic dataset.

    Args:
      g: an instance of bipartite graph.

    Returns:
      The graph instance *g*.
    """
    reviewers = {}  # Reviewers dict.
    products = {}  # Products dict.

    # Load reviewers
    with open(_fullpath(_REVIEWER_FILE)) as fp:
        for line in fp:
            rid, name = line.strip().split(" ")
            reviewers[rid] = g.new_reviewer(name=name)

    # Load products
    with open(_fullpath(_PRODUCT_FILE)) as fp:
        for line in fp:
            pid, name = line.strip().split(" ")
            products[pid] = g.new_product(name=name)

    # Load review
    with open(_fullpath(_REVIEW_FILE)) as fp:
        for line in fp:
            rid, pid, score = line.strip().split(" ")
            g.add_review(reviewers[rid], products[pid], float(score) / 5)

    return g
