:description: This package provides a method to load a synthetic review dataset.
    The synthetic review dataset has been introduced in the paper
    published in the 22nd International Conference on Database and Expert Systems
    Applications.

.. _top:

A Synthetic Review Dataset
===================================
.. raw:: html

   <div class="addthis_inline_share_toolbox"></div>

This package provides a method to load a synthetic review dataset,
and a script to evaluate mining algorithms with the dataset.

The synthetic review dataset has been introduced in the paper [#DEXA11]_
published in the 22nd International Conference on Database and Expert Systems
Applications.


Installation
--------------
Use `pip` to install this package.

.. code-block:: bash

   pip install --upgrade rgmining-synthetic-dataset


Usage
-------
This package provides `load` method which takes a graph object and adds
reviewers, products and reviews to the graph.
To use this dataset, the graph must implement
the :ref:`graph interface <dataset-io:graph-interface>`.

.. code-block:: python

   # `graph` is an instance of a graph class.
   import synthetic
   synthetic.load(graph)


API Reference
---------------
.. toctree::
  :glob:
  :maxdepth: 2

  modules/*


Scripts
--------
.. toctree::
  :maxdepth: 1

  scripts


License
---------
This software is released under The GNU General Public License Version 3,
see COPYING for more detail.


References
------------

.. [#DEXA11] Kazuki Tawaramoto, `Junpei Kawamoto`_, `Yasuhito Asano`_, and
    `Masatoshi Yoshikawa`_, "|springer| `A Bipartite Graph Model and Mutually Reinforcing
    Analysis for Review Sites
    <http://www.anrdoezrs.net/links/8186671/type/dlg/http://link.springer.com/chapter/10.1007%2F978-3-642-23088-2_25>`_,"
    Proc. of `the 22nd International Conference on Database and Expert Systems
    Applications <http://www.dexa.org/previous/dexa2011/index.html>`_ (DEXA 2011),
    pp.341-348, Toulouse, France, August 31, 2011.

.. _Junpei Kawamoto: https://www.jkawamoto.info
.. _Yasuhito Asano: http://www.iedu.i.kyoto-u.ac.jp/intro/member/asano
.. _Masatoshi Yoshikawa: http://www.db.soc.i.kyoto-u.ac.jp/~yoshikawa/

.. |springer| image:: img/springer.png
