#
#  test_score.py
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
import math
from collections.abc import Iterable
from random import random

import pytest
from numpy import testing

from synthetic.eval.score import (
    ANOMALY_REVIEWER_TAG,
    TYPE2_ANOMALY_REVIEWER_TAG,
    TYPE3_ANOMALY_REVIEWER_TAG,
    Reviewer,
    calc_anomalous_reviews,
    dcg,
    ideal_dcg,
)
from synthetic.loader import load
from tests.graph import Graph


def inv_log(v: int) -> float:
    if v == 1:
        return 1
    return 1 / math.log(v, 2)


@pytest.fixture
def reviewers() -> Iterable[Reviewer]:
    reviewers = load(Graph()).reviewers
    for r in reviewers:
        r.anomalous_score = random()
    return reviewers


@pytest.mark.parametrize("k", [0, 1, 10, 100, 1000])
def test_dcg(reviewers: Iterable[Reviewer], k: int) -> None:
    expect = 0.0
    for i, r in enumerate(sorted(reviewers, key=lambda rv: rv.anomalous_score, reverse=True)[:k], start=1):
        if ANOMALY_REVIEWER_TAG in r.name:
            expect += inv_log(i)
    testing.assert_almost_equal(dcg(reviewers, k), expect)


@pytest.mark.parametrize("k", [0, 1, 10, 100, 1000])
def test_ideal_dcg(k: int) -> None:
    expect = sum((inv_log(i + 1) for i in range(k)))
    testing.assert_almost_equal(ideal_dcg(k), expect)


def test_calc_anomalous_reviews(reviewers: Iterable[Reviewer]) -> None:
    t1 = t2 = t3 = 0
    for r in reviewers:
        if ANOMALY_REVIEWER_TAG not in r.name:
            continue
        if TYPE2_ANOMALY_REVIEWER_TAG in r.name:
            t2 += 1
        elif TYPE3_ANOMALY_REVIEWER_TAG in r.name:
            t3 += 1
        else:
            t1 += 1

    res = calc_anomalous_reviews(reviewers)
    assert res.type1 == t1
    assert res.type2 == t2
    assert res.type3 == t3
