"""Provide a loading method of synthetic dataset.
"""
from __future__ import division
from os import path

_REVIEWER_FILE = "reviewer.dat"
_PRODUCT_FILE = "product.dat"
_REVIEW_FILE = "review.dat"


def _fullpath(filename):
    """ Compute the full path of a given filename.

    Args:
      filename: Filename.

    Returns:
      The full path of the given filename.
    """
    return path.join(path.dirname(__file__), filename)


def load(g):
    """ Load synthetic dataset.

    Args:
      g: an instance of bipartite graph.

    Returns:
      The graph instance *g*.
    """
    R = {}  # Reviewers dict.
    P = {}  # Products dict.

    # Load reviewers
    with open(_fullpath(_REVIEWER_FILE)) as fp:
        for line in fp:
            rid, name = line.strip().split(" ")
            R[rid] = g.new_reviewer(name=name)

    # Load products
    with open(_fullpath(_PRODUCT_FILE)) as fp:
        for line in fp:
            pid, name = line.strip().split(" ")
            P[pid] = g.new_product(name=name)

    # Load review
    with open(_fullpath(_REVIEW_FILE)) as fp:
        for line in fp:
            rid, pid, score = line.strip().split(" ")
            if rid not in R or pid not in P:
                continue
            g.add_review(R[rid], P[pid], float(score) / 5)

    return g
