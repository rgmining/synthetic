#
#  graph.py
#
#  Copyright (c) 2016-2022 Junpei Kawamoto
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
from collections import defaultdict
from datetime import datetime
from typing import Optional


class Graph:
    """A mock object of graph object."""

    reviewers: set[str]
    products: set[str]
    reviews: defaultdict[str, dict[str, float]]

    def __init__(self) -> None:
        self.reviewers = set()
        self.products = set()
        self.reviews = defaultdict(dict)

    def new_reviewer(self, name: str) -> str:
        """Create a new reviewer."""
        if name in self.reviewers:
            raise ValueError(f"{name} already exists")
        self.reviewers.add(name)
        return name

    def new_product(self, name: str) -> str:
        """Create a new product."""
        if name in self.products:
            raise ValueError(f"{name} already exists")
        self.products.add(name)
        return name

    def add_review(self, reviewer: str, product: str, score: float, _date: Optional[datetime] = None) -> None:
        """Add a review."""
        if reviewer not in self.reviewers:
            raise ValueError(f"{reviewer} doesn't exist")
        if product not in self.products:
            raise ValueError(f"{product} doesn't exist")
        self.reviews[reviewer][product] = score
