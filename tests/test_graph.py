#
#  test_graph.py
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
from random import random

import pytest

from tests.graph import Graph


def test_new_reviewer() -> None:
    """If create same reviewers, mock should rise an error."""
    graph = Graph()
    name = "test-reviewer"
    assert graph.new_reviewer(name) == name
    with pytest.raises(ValueError):
        graph.new_reviewer(name)


def test_new_product() -> None:
    """If create same products, mock should rise an error."""
    graph = Graph()
    name = "test-product"
    assert graph.new_product(name) == name
    with pytest.raises(ValueError):
        graph.new_product(name)


def test_add_review() -> None:
    """Test add_review method."""
    graph = Graph()
    reviewer = "test-reviewer"
    product = "test-product"
    graph.new_reviewer(reviewer)
    graph.new_product(product)

    score = random()
    graph.add_review(reviewer, product, score)
    assert graph.reviews[reviewer][product] == score

    with pytest.raises(ValueError):
        graph.add_review(reviewer, reviewer, score)
    with pytest.raises(ValueError):
        graph.add_review(product, product, score)
