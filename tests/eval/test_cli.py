#
#  test_cli.py
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
from typing import NoReturn

import pytest
from pytest_mock import MockerFixture

from synthetic.eval import cli
from synthetic.eval.cli import load_graph


def test_load_graph(mocker: MockerFixture) -> None:
    method = "test-method"
    params = {"positive": random(), "negative": -random(), "zero": 0.0}

    graph = mocker.MagicMock()
    graph_constructor = mocker.MagicMock(return_value=graph)
    mocker.patch.object(cli, "INSTALLED_GRAPHS", {method: graph_constructor})
    load = mocker.patch("synthetic.load", side_effect=lambda v: v)

    g = load_graph(method, [(key, str(value)) for key, value in params.items()])
    assert g == graph

    graph_constructor.assert_called_with(**params)
    load.assert_called_with(graph)


def test_load_graph_error(mocker: MockerFixture) -> None:
    method = "test-method"
    msg = "test error message"

    def raise_error() -> NoReturn:
        raise TypeError(msg)

    graph_constructor = mocker.MagicMock(side_effect=raise_error)
    mocker.patch.object(cli, "INSTALLED_GRAPHS", {method: graph_constructor})

    with pytest.raises(SystemExit) as e:
        load_graph(method, [])
    assert msg in str(e.value)
