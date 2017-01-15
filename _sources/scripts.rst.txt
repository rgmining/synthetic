:description: synthetic-evaluation command evaluates review graph mining
  algorithms with the synthetic dataset,
  and provides three evaluation methods; threthold, ranking, dcg.

synthetic-evaluation command
==============================
This command evaluates review graph mining algorithms with the synthetic dataset,
and provides three evaluation methods; threthold, ranking, dcg, as sub commands.

It checkes installed algorithms automatically, but at least one algorithm
provided by the `Review Graph Mining Project <https://rgmining.github.io/>`_
is required to run this command.


threshold
-----------
`threshold` sub command uses a threshold based classification to evaluate
algorithms.

It runs a given algorithm and classifies reviewers whose anomalous degree is
grator than or equal to a threshold as anomalous.

Moving the threshold from 0.0 to 1.0, evaluates true positive score,
true negative score, false positive score, and false negative score.

The output is a list of JSON object which has a threshold value,
true positive score, true negative score, false positive score,
and false negative score.

The output is a list of JSON object which has a threshold value,
the precision and recall values for the threshold.

Some algorithm requires a set of parameters. For example, feagle requires
parameter `epsilon`. Argument `param` specifies those parameters, and
if you want to set 0.1 to the `epsilon`, pass `epsilon=0.1` via the
argument.

If a file name is given via `--plot` flag, a ROC curve will be plotted and
stored in the file.

The formal usage of this sub command is

.. code-block:: none

  usage: synthetic-evaluation threshold [-h] [--loop LOOP] [--param PARAM]
                                        <algorithm>

  positional arguments:
    <algorithm>    name of algorithm.

  optional arguments:
    -h, --help     show this help message and exit
    --loop LOOP    the number of iteration (default:20).
    --param PARAM  key and value pair which are connected with '='.
                   This option can be set multiply.
    --plot FILE    file name of the result graph. If set, plot an ROC curve.

ranking
--------
`ranking` sub command uses a ranking based classification to evaluate an
algorithm.

It runs a given algorithm and classifies reviewers who have top 57 highest
anomalous degree as anomalous.
After every iteration, it outputs precision of anomalous reviewers in JSON
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

If a file name is given via `--plot` flag, a graph will be plotted and
stored in the file.

The formal usage of this sub command is

.. code-block:: none

  usage: synthetic-evaluation ranking [-h] [--loop LOOP] [--param PARAM]
                                      <algorithm>

  positional arguments:
    <algorithm>    name of algorithm.

  optional arguments:
    -h, --help     show this help message and exit
    --loop LOOP    the number of iteration (default:20).
    --param PARAM  key and value pair which are connected with '='.
                   This option can be set multiply.
    --plot FILE    file name of the result graph. If set, plot a graph.

dcg
----
`dcg` sub command uses Discounted Cumulative Gain (DCG) to evaluate an
algorithm.

It runs a given algorithm and outputs DCG score for each :math:`k` in 1 to 57.

Some algorithm requires a set of parameters. For example, feagle requires
parameter `epsilon`. Argument `param` specifies those parameters, and
if you want to set 0.1 to the `epsilon`, pass `epsilon=0.1` via the
argument.

If a file name is given via `--plot` flag, a nDCG curve will be plotted and
stored in the file.

The formal usage of this sub command is

.. code-block:: none

  usage: synthetic-evaluation dcg [-h] [--loop LOOP] [--param PARAM]
                                      <algorithm>

  positional arguments:
    <algorithm>    name of algorithm.

  optional arguments:
    -h, --help     show this help message and exit
    --loop LOOP    the number of iteration (default:20).
    --param PARAM  key and value pair which are connected with '='.
                   This option can be set multiply.
    --plot FILE    file name of the result graph. If set, plot a nDCG curve.
