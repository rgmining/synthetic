A Synthetic Review Dataset
===================================
.. raw:: html

   <div class="addthis_inline_share_toolbox"></div>

This package provides a method to load a synthetic review dataset.


Installation
--------------
Use `pip` to install this package.

.. code-block:: bash

   pip install --upgrade rgmining-synthetic-dataset


Usage
-------
This package provides `load` method which takes a graph object and adds
reviewers, products and reviews to the graph.

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


Indices and tables
--------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


License
---------
This software is released under The GNU General Public License Version 3,
see COPYING for more detail.
