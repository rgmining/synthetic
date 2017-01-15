#
# __init__.py
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
"""Provides a method to load a synthetic review dataset.

The synthetic review dataset has been introduced in the paper [#DEXA11]_
published in the 22nd International Conference on Database and Expert Systems
Applications.

The number of anomalous reviewers this dataset has is defined in
:data:`ANOMALOUS_REVIEWER_SIZE`, and each anomalous reviewer has `anomaly`
in theirname.

This package provides a metho `load`, which is an alias of
:meth:`synthetic.loader.load`. The method takes a graph instance and adds
reviewers, products, and reviews to the graph.

.. rubric:: References

.. [#DEXA11] Kazuki Tawaramoto, `Junpei Kawamoto`_, `Yasuhito Asano`_, and
    `Masatoshi Yoshikawa`_, "`A Bipartite Graph Model and Mutually Reinforcing
    Analysis for Review Sites
    <http://link.springer.com/chapter/10.1007%2F978-3-642-23088-2_25>`_,"
    Proc. of `the 22nd International Conference on Database and Expert Systems
    Applications <http://www.dexa.org/>`_ (DEXA 2011),
    pp.341-348, Toulouse, France, August 31, 2011. (Acceptance rate 25%)

.. _Junpei Kawamoto: https://www.jkawamoto.info
.. _Yasuhito Asano: http://www.iedu.i.kyoto-u.ac.jp/intro/member/asano
.. _Masatoshi Yoshikawa: http://www.db.soc.i.kyoto-u.ac.jp/~yoshikawa/

"""
from __future__ import absolute_import
from synthetic.loader import load

ANOMALOUS_REVIEWER_SIZE = 57
"""The number of anomalous reviewers in this synthetic dataset. """
