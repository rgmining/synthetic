# A Synthetic Review Dataset
[![GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/copyleft/gpl.html)
[![Build Status](https://travis-ci.org/rgmining/synthetic.svg?branch=master)](https://travis-ci.org/rgmining/synthetic)
[![wercker status](https://app.wercker.com/status/41b8ce3d4b5522780908f816eae1a63d/s/master "wercker status")](https://app.wercker.com/project/byKey/41b8ce3d4b5522780908f816eae1a63d)
[![Code Climate](https://codeclimate.com/github/rgmining/synthetic/badges/gpa.svg)](https://codeclimate.com/github/rgmining/synthetic)
[![Release](https://img.shields.io/badge/release-0.9.0-brightgreen.svg)](https://github.com/rgmining/synthetic/releases/tag/v0.9.0)

This package provides a method to load a synthetic review dataset.


## Installation
Use `pip` to install this package.

```shell
pip install --upgrade rgmining-synthetic-dataset
```


## Usage
This package provides `load` method which takes a graph object and adds
reviewers, products and reviews to the graph.

```py
# `graph` is an instance of a graph class.
import synthetic
synthetic.load(graph)
```


## License
This software is released under The GNU General Public License Version 3,
see [COPYING](COPYING) for more detail.
