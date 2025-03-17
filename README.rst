A Synthetic Review Dataset
==========================

|GPLv3| |Build Status| |Maintainability| |Test Coverage| |PyPi| |Japanese|

|Logo|

This package provides a method to load a synthetic review dataset.

The synthetic review dataset has been introduced in the following paper:

-  Kazuki Tawaramoto, `Junpei Kawamoto <https://www.jkawamoto.info>`__,
   `Yasuhito
   Asano <http://ris.toyo.ac.jp/profile/en.d83b3a53c4e08dc39c5613ee8954ad37.html>`__, and
   `Masatoshi
   Yoshikawa <http://www.db.soc.i.kyoto-u.ac.jp/~yoshikawa/>`__,
   "`A Bipartite Graph Model and Mutually Reinforcing Analysis for
   Review
   Sites <http://www.anrdoezrs.net/links/8186671/type/dlg/http://link.springer.com/chapter/10.1007%2F978-3-642-23088-2_25>`__,"
   Proc. of `the 22nd International Conference on Database and Expert
   Systems
   Applications <http://www.dexa.org/previous/dexa2011/index.html>`__
   (DEXA 2011),
   pp.341-348, Toulouse, France, August 31, 2011.

Installation
------------

Use ``pip`` to install this package.

.. code:: shell

    pip install --upgrade rgmining-synthetic-dataset

Usage
-----

This package provides ``load`` method which takes a graph object and
adds reviewers, products and reviews to the graph.

.. code:: py

    # `graph` is an instance of a graph class.
    import synthetic
    synthetic.load(graph)

This package also provides an executable script, ``rgmining-synthetic-dataset``.
See the `document <https://rgmining.github.io/synthetic/scripts.html>`__
for more information.

License
-------

This software is released under The GNU General Public License Version 3,
see `COPYING <COPYING>`__ for more detail.

.. |GPLv3| image:: https://img.shields.io/badge/license-GPLv3-blue.svg
   :target: https://www.gnu.org/copyleft/gpl.html
.. |Build Status| image:: https://github.com/rgmining/synthetic/actions/workflows/python-lib.yaml/badge.svg
   :target: https://github.com/rgmining/synthetic/actions/workflows/python-lib.yaml
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/6e956b0cf348d6a23c19/maintainability
   :target: https://codeclimate.com/github/rgmining/synthetic/maintainability
.. |Test Coverage| image:: https://api.codeclimate.com/v1/badges/6e956b0cf348d6a23c19/test_coverage
   :target: https://codeclimate.com/github/rgmining/synthetic/test_coverage
.. |PyPi| image:: https://img.shields.io/badge/pypi-0.9.4-brightgreen.svg
   :target: https://pypi.python.org/pypi/rgmining-synthetic-dataset
.. |Japanese| image:: https://img.shields.io/badge/qiita-%E6%97%A5%E6%9C%AC%E8%AA%9E-brightgreen.svg
   :target: http://qiita.com/jkawamoto/items/9a7647c47998fab4a1ad
.. |Logo| image:: https://rgmining.github.io/synthetic/_static/image.png
   :target: https://rgmining.github.io/synthetic/
