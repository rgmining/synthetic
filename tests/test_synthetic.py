#
#  test_synthetic.py
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
"""Unit test for synthetic package."""

import synthetic
from tests.graph import Graph


def test_load() -> None:
    """Test load method."""
    graph = Graph()
    assert synthetic.load(graph) == graph

    anomalous = len([r for r in graph.reviewers if "anomaly" in r.name])
    assert anomalous == synthetic.ANOMALOUS_REVIEWER_SIZE

    for pmap in graph.reviews.values():
        for score in pmap.values():
            assert 0 <= score < 1
