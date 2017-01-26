#! /usr/bin/env python
#
# synthetic_evaluation.py
#
# Copyright (c) 2016-2017 Junpei Kawamoto
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
# along with rgmining-synthetic-dataset. If not, see <http://www.gnu.org/licenses/>.
#
"""Evaluate a review graph mining algorithm with the synthetic dataset.
"""
# pylint: disable=invalid-name
from __future__ import absolute_import, division
import json
import logging
from logging import getLogger
import math
from os import path
import sys

import dsargparse
from matplotlib import pyplot
import numpy as np

sys.path.append(path.join(path.dirname(__file__), "../"))
import synthetic  # pylint: disable=import-error,wrong-import-position

LOGGER = getLogger(__name__)

#--------------------------
# Loading algorithms
#--------------------------
ALGORITHMS = {}
"""Dictionary of graph loading functions associated with installed algorithms.
"""

# Load and register RIA.
try:
    import ria
except ImportError:
    LOGGER.info("rgmining-ria is not installed.")
else:
    def ignore_args(func):
        """Returns a wrapped function which ignore given arguments."""
        def _(*_args):
            """The function body."""
            return func()
        return _
    ALGORITHMS["ria"] = ria.ria_graph
    ALGORITHMS["one"] = ignore_args(ria.one_graph)
    ALGORITHMS["onesum"] = ignore_args(ria.one_sum_graph)
    ALGORITHMS["mra"] = ignore_args(ria.mra_graph)


# Load and register RSD.
try:
    import rsd  # pylint: disable=wrong-import-position
except ImportError:
    LOGGER.info("rgmining-rsd is not installed.")
else:
    ALGORITHMS["rsd"] = rsd.ReviewGraph


# Load and register Fraud Eagle.
try:
    import fraud_eagle  # pylint: disable=wrong-import-position
except ImportError:
    LOGGER.info("rgmining-fraud-eagle is not installed.")
else:
    ALGORITHMS["feagle"] = fraud_eagle.ReviewGraph


# Load and register FRAUDAR.
try:
    import fraudar  # pylint: disable=wrong-import-position
except ImportError:
    LOGGER.info("rgmining-fraudar is not installed.")
else:
    def create_fraudar_graph(nblock=1):
        """Create a review graph defined in Fraud Eagle package.
        """
        return fraudar.ReviewGraph(int(nblock))
    ALGORITHMS["fraudar"] = create_fraudar_graph


TYPE = sorted(ALGORITHMS.keys())
"""List of supported algorithm types.
"""


#--------------------------
def DCG(reviewers, k):
    """Computes a DCG score for a top-k ranking.

    Args:
      reviewers: A collection of reviewers.
      k: An integer specifying the k.

    Returns:
      The DCG score of the top-k ranking.
    """
    res = 0.
    i = 1.
    for r in sorted(reviewers, key=lambda r: r.anomalous_score, reverse=True)[:k]:
        if r.name.find("anomaly") != -1:
            res += 1. / math.log(i, 2) if i != 1 else 1
        i += 1
    return res


def IDCG(k):
    """Computes an IDCG score.

    Args:
      k: An integer specifying the length of an ideal ranking.

    Returns:
      The IDCG score of a l-length ideal ranking.
    """
    res = 0.
    for i in range(1, k + 1):
        res += 1. / math.log(i, 2) if i != 1 else 1
    return res


def calc_anomalous_reviews(reviewers):
    """Counts the number of anomalous reviewers.

    Args:
      reviewers: A collection of reviewers.

    Returns:
      A tuple consisted in the number of type-1 anomalous reviewers,
      the number of type-2 anomalous reviewers, and the number of type-3
      anomalous reviewers in the collection.
    """
    type1 = type2 = type3 = 0.
    for r in reviewers:
        if r.name.find("anomaly") != -1:
            if r.name.find("_1") != -1:
                type2 += 1
            elif r.name.find("_2") != -1:
                type3 += 1
            else:
                type1 += 1
    return (type1, type2, type3)


def threshold(method, loop, output, param, plot=None):
    """Threshold based classification.

    Runs a given algorithm and classifies reviewers whose anomalous degree is
    grator than or equal to a threshold as anomalous.
    Moving the threshold from 0.0 to 1.0, evaluates true positive score,
    true negative score, false positive score, and false negative score.

    The output is a list of JSON object which has a threshold value,
    true positive score, true negative score, false positive score,
    and false negative score.

    Some algorithm requires a set of parameters. For example, feagle requires
    parameter `epsilon`. Argument `param` specifies those parameters, and
    if you want to set 0.1 to the `epsilon`, pass `epsilon=0.1` via the
    argument.

    If a file name is given via `plot`, a ROC curve will be plotted and
    stored in the file.

    Args:
      method: name of algorithm.
      loop: the number of iteration (default: 20).
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
      plot: file name of the result graph. If set, plot an ROC curve.
    """
    kwargs = {key: float(value)
              for key, value in [v.split("=") for v in param]}
    g = ALGORITHMS[method](**kwargs)
    synthetic.load(g)

    # If method is ONE, the graph is updated only one time.
    for _ in xrange(loop if method != "one" else 1):
        g.update()

    X, Y = [], []
    normal_reviewer_size = len(g.reviewers) - synthetic.ANOMALOUS_REVIEWER_SIZE
    for th in np.linspace(0, 1, 100):
        a = [r for r in g.reviewers if r.anomalous_score >= th]

        tp = sum(calc_anomalous_reviews(a))
        fp = len(a) - tp
        fn = synthetic.ANOMALOUS_REVIEWER_SIZE - tp
        tn = normal_reviewer_size - fp

        json.dump({
            "threshold": th,
            "true-positive": tp,
            "true-negative": tn,
            "false-positive": fp,
            "false-negative": fn
        }, output)
        output.write("\n")

        X.append(fp / normal_reviewer_size)
        Y.append(tp / synthetic.ANOMALOUS_REVIEWER_SIZE)

    if plot:
        pyplot.plot(X, Y)
        pyplot.xlabel("False positive rate")
        pyplot.ylabel("True positive rate")
        pyplot.xlim(0, 1)
        pyplot.ylim(0, 1)
        pyplot.title("AUC: {0}".format(-round(np.trapz(Y, X), 5)))
        pyplot.tight_layout()
        pyplot.savefig(plot)


def ranking(
        method, loop, output,
        param, plot=None):  # pylint: disable=too-many-locals
    """Ranking based classification.

    Runs a given algorithm and classifies reviewers who have top 57 highest
    anomalous degree as anomalous.
    After every iteration, outputs precision of anomalous reviewers in JSON
    format.

    a1, a2, and a3 means the number of independent, collude, and the other
    anomalous reviewers in the top 57 anomalous reviewers, respectively,
    a1-presicion, a2-precision, and a3-precision are the precisions of them.

    error and error-rate are the number of normal reviwers in the top 57
    anomalous reviewers and its rate, respectively.

    Some algorithm requires a set of parameters. For example, feagle requires
    parameter `epsilon`. Argument `param` specifies those parameters, and
    if you want to set 0.1 to the `epsilon`, pass `epsilon=0.1` via the
    argument.

    If a file name is given via `--plot` flag, a ROC curve will be plotted and
    stored in the file.

    Args:
      method: name of algorithm.
      loop: the number of iteration (default: 20).
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
      plot: file name of the result graph. If set, plot a graph.
    """
    kwargs = {key: float(value)
              for key, value in [v.split("=") for v in param]}
    g = ALGORITHMS[method](**kwargs)
    synthetic.load(g)

    num_of_reviewers = len(g.reviewers)
    num_of_type1, num_of_type2, num_of_type3 = calc_anomalous_reviews(
        g.reviewers)

    A1, A2, A3, E = [], [], [], []
    for i in xrange(loop if method != "one" else 1):
        g.update()

        a = sorted(g.reviewers, key=lambda r: r.anomalous_score,
                   reverse=True)[:57]
        type1, type2, type3 = calc_anomalous_reviews(a)
        error = len(a) - (type1 + type2 + type3)

        a1 = type1 / num_of_type1
        a2 = type2 / num_of_type2
        a3 = type3 / num_of_type3
        e = error / num_of_reviewers

        json.dump({
            "a1": int(type1),
            "a1-precision": a1,
            "a2": int(type2),
            "a2-precision": a2,
            "a3": int(type3),
            "a3-precision": a3,
            "error": int(error),
            "error-rate": e,
            "loop": i
        }, output)
        output.write("\n")

        A1.append(a1)
        A2.append(a2)
        A3.append(a3)
        E.append(e)

    if plot:
        X = np.arange(len(A1))
        pyplot.plot(X, A1, label="a1")
        pyplot.plot(X, A2, label="a2")
        pyplot.plot(X, A3, label="a3")
        pyplot.plot(X, E, label="error")
        pyplot.xlim(1, len(A1))
        pyplot.ylim(0)
        pyplot.xlabel("iteration")
        pyplot.legend()
        pyplot.tight_layout()
        pyplot.savefig(plot)


def dcg(method, loop, output, param, plot=None):
    """Evaluate an anomalous degree ranking by DCG.

    Runs a given algorithm and outputs Discounted Cumulative Gain (DCG) score
    for each k in 1 to 57.

    Some algorithm requires a set of parameters. For example, feagle requires
    parameter `epsilon`. Argument `param` specifies those parameters, and
    if you want to set 0.1 to the `epsilon`, pass `epsilon=0.1` via the
    argument.

    If a file name is given via `--plot` flag, a nDCG curve will be plotted and
    stored in the file.

    Args:
      method: name of algorithm.
      loop: the number of iteration (default: 20).
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
      plot: file name of the result graph. If set, plot a nDCG curve.
    """
    kwargs = {key: float(value)
              for key, value in [v.split("=") for v in param]}
    g = ALGORITHMS[method](**kwargs)
    synthetic.load(g)

    for _ in xrange(loop if method != "one" else 1):
        g.update()

    X, Y = [], []
    for k in range(1, synthetic.ANOMALOUS_REVIEWER_SIZE + 1):
        score = DCG(g.reviewers, k) / IDCG(k)
        json.dump({"k": k, "score": score}, output)
        output.write("\n")

        X.append(k)
        Y.append(score)

    if plot:
        pyplot.plot(X, Y)
        pyplot.xlabel("k")
        pyplot.ylabel("nDCG")
        pyplot.xlim(1, synthetic.ANOMALOUS_REVIEWER_SIZE)
        pyplot.ylim(0, 1.1)
        pyplot.tight_layout()
        pyplot.savefig(plot)


def main():
    """The main function.
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    if not ALGORITHMS:
        logging.error("No algorithms are installed.")
        sys.exit(1)

    parser = dsargparse.ArgumentParser(main=main)
    parser.add_argument(
        "--output", default=sys.stdout,
        type=dsargparse.FileType("w"),  # pylint: disable=no-member
        help="file path to store results (Default: stdout).")
    subparsers = parser.add_subparsers()

    threshold_cmd = subparsers.add_parser(threshold)
    threshold_cmd.add_argument("method", choices=TYPE)
    threshold_cmd.add_argument("--loop", type=int, default=20)
    threshold_cmd.add_argument(
        "--param", action="append", default=[],
        help=(
            "key and value pair which are connected with '='.\n"
            "This option can be set multiply."))
    threshold_cmd.add_argument("--plot", metavar="FILE")

    ranking_cmd = subparsers.add_parser(ranking)
    ranking_cmd.add_argument("method", choices=TYPE)
    ranking_cmd.add_argument("--loop", type=int, default=20)
    ranking_cmd.add_argument(
        "--param", action="append", default=[],
        help=(
            "key and value pair which are connected with '='.\n"
            "This option can be set multiply."))
    ranking_cmd.add_argument("--plot", metavar="FILE")

    dcg_cmd = subparsers.add_parser(dcg)
    dcg_cmd.add_argument("method", choices=TYPE)
    dcg_cmd.add_argument("--loop", type=int, default=20)
    dcg_cmd.add_argument(
        "--param", action="append", default=[],
        help=(
            "key and value pair which are connected with '='.\n"
            "This option can be set multiply."))
    dcg_cmd.add_argument("--plot", metavar="FILE")

    try:
        return parser.parse_and_run()
    except KeyboardInterrupt:
        return "Canceled"
    except Exception as e:  # pylint: disable=broad-except
        logging.exception("Untracked exception occurred.")
        return e.message
    finally:
        logging.shutdown()


if __name__ == "__main__":
    sys.exit(main())
