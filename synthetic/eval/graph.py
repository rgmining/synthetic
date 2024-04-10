#
#  graph.py
#
#  Copyright (c) 2016-2024 Junpei Kawamoto
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
import logging
from collections.abc import Collection
from functools import wraps
from typing import Any, Callable

from synthetic.eval import Reviewer
from synthetic.loader import Graph as _Graph

LOGGER = logging.getLogger(__name__)


class Graph(_Graph):
    """Protocol class that a graph needs to have for eval package."""

    reviewers: Collection[Reviewer]

    def update(self) -> Any: ...


GraphConstructor = Callable[..., Graph]


def ignore_args(func: GraphConstructor) -> GraphConstructor:
    """Returns a wrapped function which ignores given arguments."""

    @wraps(func)
    def new_func(*_args: Any) -> Graph:
        """The function body."""
        return func()

    return new_func


def int_args(func: GraphConstructor) -> GraphConstructor:
    """Returns a wrapped function which converts each given argument with int."""

    @wraps(func)
    def new_func(*args: str) -> Graph:
        return func(*(int(v) for v in args))

    return new_func


def list_installed_graphs() -> dict[str, GraphConstructor]:
    """Returns a dictionary of installed graph constructors."""
    res: dict[str, Callable[..., Graph]] = {}

    # Load and register RIA.
    try:
        import ria as _ria

        res["ria"] = _ria.ria_graph
        res["one"] = ignore_args(_ria.one_graph)
        res["onesum"] = ignore_args(_ria.one_sum_graph)
        res["mra"] = ignore_args(_ria.mra_graph)
    except ImportError:
        LOGGER.info("rgmining-ria is not installed.")
        _ria = None

    # Load and register RSD.
    try:
        import rsd as _rsd

        res["rsd"] = _rsd.ReviewGraph
    except ImportError:
        LOGGER.info("rgmining-rsd is not installed.")
        _rsd = None

    # Load and register Fraud Eagle.
    try:
        import fraud_eagle as _fraud_eagle

        res["feagle"] = _fraud_eagle.ReviewGraph
    except ImportError:
        LOGGER.info("rgmining-fraud-eagle is not installed.")
        _fraud_eagle = None

    # Load and register FRAUDAR.
    try:
        import fraudar as _fraudar

        res["fraudar"] = int_args(_fraudar.ReviewGraph)
    except ImportError:
        LOGGER.info("rgmining-fraudar is not installed.")
        _fraudar = None

    return res
