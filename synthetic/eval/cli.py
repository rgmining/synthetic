#
#  cli.py
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
"""This module defines a CLI command that evaluates a review graph algorithm with the synthetic dataset."""

import json
import logging
import sys
from typing import BinaryIO, Final, Optional, TextIO

import click
import numpy as np
from matplotlib import pyplot

import synthetic
from synthetic.eval.graph import Graph, list_installed_graphs
from synthetic.eval.score import calc_anomalous_reviews
from synthetic.eval.score import dcg as dc_gain
from synthetic.eval.score import ideal_dcg

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

LOGGER: Final = logging.getLogger(__name__)

INSTALLED_GRAPHS = list_installed_graphs()
"""A dictionary of installed graph constructors.
"""

GRAPH_TYPES = sorted(INSTALLED_GRAPHS.keys())
"""List of supported algorithm types.
"""


def load_graph(method: str, params: list[tuple[str, str]]) -> Graph:
    try:
        return synthetic.load(INSTALLED_GRAPHS[method](**{k: float(v) for k, v in params}))
    except TypeError as e:
        sys.exit(f"Failed to initialize a graph object. Some parameter might need to be given via --param flag:\n{e}")


@click.group()
@click.version_option(click.__version__)
def main() -> None:
    """Evaluate a review graph mining algorithm with the synthetic dataset."""
    if not INSTALLED_GRAPHS:
        LOGGER.error("No algorithms are installed.")


@main.command()
@click.argument("method", type=click.Choice(GRAPH_TYPES, case_sensitive=False))
@click.option("--loop", type=int, default=20, metavar="LOOP", help="Number of iteration (default: 20).")
@click.option(
    "--param",
    type=(str, str),
    multiple=True,
    metavar="KEY VALUE",
    help="Key and value pair passed to the chosen algorithm. This option can be set multiply.",
)
@click.option(
    "--output", type=click.File("w"), default=sys.stdout, help="File path to store results (default: stdout)."
)
@click.option("--plot", type=click.File("bw"), help="File name of the result graph. If set, plot an ROC curve")
def threshold(
    method: str, loop: int, param: list[tuple[str, str]], output: TextIO, plot: Optional[BinaryIO] = None
) -> None:
    """Threshold based classification.

    Runs a given algorithm and classifies reviewers whose anomalous degree is
    grater than or equal to a threshold as anomalous.
    Moving the threshold from 0.0 to 1.0, evaluates true positive score,
    true negative score, false positive score, and false negative score.

    The output is a list of JSON object which has a threshold value,
    true positive score, true negative score, false positive score,
    and false negative score.

    Some algorithm requires a set of parameters. For example, feagle requires
    parameter `epsilon`. Option `param` specifies those parameters, and
    if you want to set 0.1 to the `epsilon`, pass `--param epsilon 0.1`.

    If a file name is given via `plot`, a ROC curve will be plotted and
    stored in the file.
    \f

    Args:
      method: name of algorithm.
      loop: the number of iteration (default: 20).
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
      plot: file name of the result graph. If set, plot an ROC curve.
    """
    g = load_graph(method, param)

    # If method is ONE, the graph is updated only one time.
    for _ in range(loop if method != "one" else 1):
        g.update()

    x, y = [], []
    normal_reviewer_size = len(g.reviewers) - synthetic.ANOMALOUS_REVIEWER_SIZE
    for th in np.linspace(0, 1, 100):
        a = [r for r in g.reviewers if r.anomalous_score >= th]

        tp = sum(calc_anomalous_reviews(a))
        fp = len(a) - tp
        fn = synthetic.ANOMALOUS_REVIEWER_SIZE - tp
        tn = normal_reviewer_size - fp

        json.dump(
            {"threshold": th, "true-positive": tp, "true-negative": tn, "false-positive": fp, "false-negative": fn},
            output,
        )
        output.write("\n")

        x.append(fp / normal_reviewer_size)
        y.append(tp / synthetic.ANOMALOUS_REVIEWER_SIZE)

    if plot:
        pyplot.plot(x, y)
        pyplot.xlabel("False positive rate")
        pyplot.ylabel("True positive rate")
        pyplot.xlim(0, 1)
        pyplot.ylim(0, 1)
        pyplot.title("AUC: {0}".format(-round(np.trapezoid(y, x), 5)))
        pyplot.tight_layout()
        pyplot.savefig(plot)


@main.command()
@click.argument("method", type=click.Choice(GRAPH_TYPES, case_sensitive=False))
@click.option("--loop", type=int, default=20, metavar="LOOP", help="Number of iteration (default: 20).")
@click.option(
    "--param",
    type=(str, str),
    multiple=True,
    metavar="KEY VALUE",
    help="Key and value pair passed to the chosen algorithm. This option can be set multiply.",
)
@click.option(
    "--output", type=click.File("w"), default=sys.stdout, help="File path to store results (default: stdout)."
)
@click.option("--plot", type=click.File("bw"), help="File name of the result graph. If set, plot an ROC curve")
def ranking(
    method: str, loop: int, param: list[tuple[str, str]], output: TextIO, plot: Optional[BinaryIO] = None
) -> None:
    """Ranking based classification.

    Runs a given algorithm and classifies reviewers who have top 57 highest
    anomalous degree as anomalous.
    After every iteration, outputs precision of anomalous reviewers in JSON
    format.

    a1, a2, and a3 means the number of independent, collude, and the other
    anomalous reviewers in the top 57 anomalous reviewers, respectively,
    a1-precision, a2-precision, and a3-precision are the precisions of them.

    error and error-rate are the number of normal reviewers in the top 57
    anomalous reviewers and its rate, respectively.

    Some algorithm requires a set of parameters. For example, feagle requires
    parameter `epsilon`. Option `param` specifies those parameters, and
    if you want to set 0.1 to the `epsilon`, pass `--param epsilon 0.1`.

    If a file name is given via `--plot` flag, a ROC curve will be plotted and
    stored in the file.
    \f

    Args:
      method: name of algorithm.
      loop: the number of iteration (default: 20).
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
      plot: file name of the result graph. If set, plot a graph.
    """
    g = load_graph(method, param)

    num_of_reviewers = len(g.reviewers)
    num_of_type1, num_of_type2, num_of_type3 = calc_anomalous_reviews(g.reviewers)

    a1_list, a2_list, a3_list, e_list = [], [], [], []
    for i in range(loop if method != "one" else 1):
        g.update()

        a = sorted(g.reviewers, key=lambda r: r.anomalous_score, reverse=True)[:57]
        type1, type2, type3 = calc_anomalous_reviews(a)
        error = len(a) - (type1 + type2 + type3)

        a1 = type1 / num_of_type1
        a2 = type2 / num_of_type2
        a3 = type3 / num_of_type3
        e = error / num_of_reviewers

        json.dump(
            {
                "a1": int(type1),
                "a1-precision": a1,
                "a2": int(type2),
                "a2-precision": a2,
                "a3": int(type3),
                "a3-precision": a3,
                "error": int(error),
                "error-rate": e,
                "loop": i,
            },
            output,
        )
        output.write("\n")

        a1_list.append(a1)
        a2_list.append(a2)
        a3_list.append(a3)
        e_list.append(e)

    if plot:
        x = np.arange(len(a1_list))
        pyplot.plot(x, a1_list, label="a1")
        pyplot.plot(x, a2_list, label="a2")
        pyplot.plot(x, a3_list, label="a3")
        pyplot.plot(x, e_list, label="error")
        pyplot.xlim(1, len(a1_list))
        pyplot.ylim(0)
        pyplot.xlabel("iteration")
        pyplot.legend()
        pyplot.tight_layout()
        pyplot.savefig(plot)


@main.command()
@click.argument("method", type=click.Choice(GRAPH_TYPES, case_sensitive=False))
@click.option("--loop", type=int, default=20, metavar="LOOP", help="Number of iteration (default: 20).")
@click.option(
    "--param",
    type=(str, str),
    multiple=True,
    metavar="KEY VALUE",
    help="Key and value pair passed to the chosen algorithm. This option can be set multiply.",
)
@click.option(
    "--output", type=click.File("w"), default=sys.stdout, help="File path to store results (default: stdout)."
)
@click.option("--plot", type=click.File("bw"), help="File name of the result graph. If set, plot an ROC curve")
def dcg(method: str, loop: int, param: list[tuple[str, str]], output: TextIO, plot: Optional[BinaryIO] = None) -> None:
    """Evaluate an anomalous degree ranking by DCG.

    Runs a given algorithm and outputs Discounted Cumulative Gain (DCG) score
    for each k in 1 to 57.

    Some algorithm requires a set of parameters. For example, feagle requires
    parameter `epsilon`. Option `param` specifies those parameters, and
    if you want to set 0.1 to the `epsilon`, pass `--param epsilon=0.1`.

    If a file name is given via `--plot` flag, a nDCG curve will be plotted and
    stored in the file.
    \f

    Args:
      method: name of algorithm.
      loop: the number of iteration (default: 20).
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
      plot: file name of the result graph. If set, plot a nDCG curve.
    """
    g = load_graph(method, param)

    for _ in range(loop if method != "one" else 1):
        g.update()

    x, y = [], []
    for k in range(1, synthetic.ANOMALOUS_REVIEWER_SIZE + 1):
        score = dc_gain(g.reviewers, k) / ideal_dcg(k)
        json.dump({"k": k, "score": score}, output)
        output.write("\n")

        x.append(k)
        y.append(score)

    if plot:
        pyplot.plot(x, y)
        pyplot.xlabel("k")
        pyplot.ylabel("nDCG")
        pyplot.xlim(1, synthetic.ANOMALOUS_REVIEWER_SIZE)
        pyplot.ylim(0, 1.1)
        pyplot.tight_layout()
        pyplot.savefig(plot)
