#! /usr/bin/env python
#
# evaluation.py
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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
"""Evaluate a review graph mining algorithm with the synthetic dataset.
"""
# pylint: disable=invalid-name
from __future__ import absolute_import
import json
import math
from os import path
import sys
import logging
from logging import getLogger
import dsargparse

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
    def create_fraudar_graph(nblock):
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


def threshold(method, loop, output, param):
    """Threshold based classification.

    Runs a given algorithm and classifies reviewers whose anomalous degree is
    grator than or equal to a threshold as anomalous.
    Moving the threshold from 0.0 to 1.0, evaluates the precision and recall of
    reviewers classfied in anomalous reviewers.

    The output is a list of JSON object which has a threshold value,
    the precision and recall values for the threshold.

    Some algorithm requires a set of parameters.

    Args:
      method: name of algorithm.
      loop: the number of iteration.
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
    """
    kwargs = {key: float(value)
              for key, value in [v.split("=") for v in param]}
    g = ALGORITHMS[method](**kwargs)
    synthetic.load(g)

    num_of_anomalous = sum(calc_anomalous_reviews(g.reviewers))

    # If method is ONE, the graph is updated only one time.
    for _ in xrange(loop if method != "one" else 1):
        g.update()

    for th in [v / 100. for v in range(0, 101)]:
        a = [r for r in g.reviewers if r.anomalous_score >= th]
        found = sum(calc_anomalous_reviews(a))

        json.dump({
            "threshold": th,
            "precision": found / len(a) if a else 0,
            "recall": found / num_of_anomalous if num_of_anomalous else 0
        }, output)
        output.write("\n")


def ranking(method, loop, output, param):  # pylint: disable=too-many-locals
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

    Args:
      method: name of algorithm.
      loop: the number of iteration.
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
    """
    kwargs = {key: float(value)
              for key, value in [v.split("=") for v in param]}
    g = ALGORITHMS[method](**kwargs)
    synthetic.load(g)

    num_of_reviewers = len(g.reviewers)
    num_of_type1, num_of_type2, num_of_type3 = calc_anomalous_reviews(
        g.reviewers)

    for i in xrange(loop if method != "one" else 1):
        g.update()

        a = sorted(g.reviewers, key=lambda r: r.anomalous_score,
                   reverse=True)[:57]
        type1, type2, type3 = calc_anomalous_reviews(a)
        error = len(a) - (type1 + type2 + type3)

        json.dump({
            "a1": int(type1),
            "a1-precision": type1 / num_of_type1,
            "a2": int(type2),
            "a2-precision": type2 / num_of_type2,
            "a3": int(type3),
            "a3-precision": type3 / num_of_type3,
            "error": int(error),
            "error-rate": error / num_of_reviewers,
            "loop": i
        }, output)
        output.write("\n")


def dcg(method, loop, output, param):
    """Evaluate an anomalous degree ranking by DCG.

    Runs a given algorithm and outputs Discounted Cumulative Gain (DCG) score
    for each k in 1 to 57.

    Args:
      method: name of algorithm.
      loop: the number of iteration.
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
    """
    kwargs = {key: float(value)
              for key, value in [v.split("=") for v in param]}
    g = ALGORITHMS[method](**kwargs)
    synthetic.load(g)

    for _ in xrange(loop if method != "one" else 1):
        g.update()

    for k in range(1, synthetic.ANOMALOUS_REVIEWER_SIZE + 1):
        json.dump({"k": k, "score": DCG(g.reviewers, k) / IDCG(k)}, output)
        output.write("\n")


def main():
    """The main function.
    """
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
    threshold_cmd.add_argument("--loop", type=int, default=100)
    threshold_cmd.add_argument(
        "--param", action="append", default=[],
        help=(
            "key and value pair which are connected with '='.\n"
            "This option can be set multiply."))

    ranking_cmd = subparsers.add_parser(ranking)
    ranking_cmd.add_argument("method", choices=TYPE)
    ranking_cmd.add_argument("--loop", type=int, default=100)
    ranking_cmd.add_argument(
        "--param", action="append", default=[],
        help=(
            "key and value pair which are connected with '='.\n"
            "This option can be set multiply."))

    dcg_cmd = subparsers.add_parser(dcg)
    dcg_cmd.add_argument("method", choices=TYPE)
    dcg_cmd.add_argument("--loop", type=int, default=100)
    dcg_cmd.add_argument(
        "--param", action="append", default=[],
        help=(
            "key and value pair which are connected with '='.\n"
            "This option can be set multiply."))

    parser.parse_and_run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:  # pylint: disable=broad-except
        logging.exception("Untracked exception occurred.")
    finally:
        logging.shutdown()
