#
#  score.py
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
from typing import Final, NamedTuple, Protocol

ANOMALY_REVIEWER_TAG: Final = "anomaly"
TYPE2_ANOMALY_REVIEWER_TAG: Final = "_1"
TYPE3_ANOMALY_REVIEWER_TAG: Final = "_2"


class Reviewer(Protocol):
    name: str
    anomalous_score: float


def dcg(reviewers: Iterable[Reviewer], k: int) -> float:
    """Computes a DCG score for a top-k ranking.

    Args:
      reviewers: A collection of reviewers.
      k: An integer specifying the k.

    Returns:
      The DCG score of the top-k ranking.
    """
    res = 0.0
    for i, r in enumerate(sorted(reviewers, key=lambda rv: rv.anomalous_score, reverse=True)[:k], start=1):
        if ANOMALY_REVIEWER_TAG in r.name:
            res += 1.0 / math.log(i, 2) if i != 1 else 1
        i += 1
    return res


def ideal_dcg(k: int) -> float:
    """Computes an ideal DCG score.

    Args:
      k: An integer specifying the length of an ideal ranking.

    Returns:
      The IDCG score of a l-length ideal ranking.
    """
    if k == 0:
        return 0.0
    return sum((1.0 / math.log(i, 2) for i in range(2, k + 1)), start=1.0)


class AnomalousReviews(NamedTuple):
    type1: int
    type2: int
    type3: int


def calc_anomalous_reviews(reviewers: Iterable[Reviewer]) -> AnomalousReviews:
    """Counts the number of anomalous reviewers.

    Args:
      reviewers: A collection of reviewers.

    Returns:
      A named tuple AnomalousReviews that consists in the number of
      type-1 anomalous reviewers, the number of type-2 anomalous
      reviewers, and the number of type-3 anomalous reviewers in the
      collection.
    """
    type1 = type2 = type3 = 0
    for r in reviewers:
        if ANOMALY_REVIEWER_TAG in r.name:
            if TYPE2_ANOMALY_REVIEWER_TAG in r.name:
                type2 += 1
            elif TYPE3_ANOMALY_REVIEWER_TAG in r.name:
                type3 += 1
            else:
                type1 += 1
    return AnomalousReviews(type1, type2, type3)
