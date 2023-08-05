#!/bin/bash

pushd nearest_neighbors
python setup.py install --home="."
popd

pushd grid_subsampling
python setup.py build_ext --inplace
popd
