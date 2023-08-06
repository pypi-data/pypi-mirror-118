# pv60hz

[![CircleCI](https://circleci.com/gh/60hz-io/pv60hz/tree/main.svg?style=svg)](https://circleci.com/gh/60hz-io/pv60hz/tree/main)
[![codecov](https://codecov.io/gh/60hz-io/pv60hz/branch/main/graph/badge.svg?token=D2N9RKHCK3)](https://codecov.io/gh/60hz-io/pv60hz)
[![Documentation Status](https://readthedocs.org/projects/pv60hz/badge/?version=latest)](https://pv60hz.readthedocs.io/en/latest/?badge=latest)
[![Python: 3.6](https://img.shields.io/badge/Python-3.6-blue)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-lightgrey)](https://github.com/60hz-io/pv60hz/blob/main/LICENSE)

The pv60hz library is an solar forecast simulation powered by the 60hz company. This library provides easy download to the [Global Forecast System](https://www.nco.ncep.noaa.gov/pmb/products/gfs/), a numerical forecasting model provided by the National Oceanic and Atmospheric Administration, and preprocessing steps required for solar power generation estimation. This library uses the open source [pvlib-python](https://github.com/pvlib/pvlib-python) to simulate the predicted solar power generation.

## Intro
As interest in climate change and environmental issues is growing around the world, renewable energy power plants are continuously increasing.

However, as renewable energy increases, it becomes increasingly difficult to operate the power grid.
Renewable energy power plants are an intermittent resource whose power generation varies depending on the weather, making it difficult to balance the supply and demand for electricity.
In addition, relatively small power plants are characterized by decentralization, making them difficult to manage with traditional methods.

Therefore, if you can accurately predict the amount of renewable energy generation across the country, you can balance supply and demand by adjusting the utilization rate of flexible resources such as fossil fuels.
In addition, this generation forecasting technology can be used for grid operation, monitoring and maintenance of solar and wind power plants.


## Getting started
This library recommends a virtual environment using [conda](https://docs.conda.io/en/latest/).
```
$ conda create -y -n venv python==3.6.10
$ conda activate venv
```

And install the [cfgrib](https://github.com/ecmwf/cfgrib) library.
```
conda install -c conda-forge cfgrib
```

## Installation
```
$ pip install pv60hz
```

## Citing
William F. Holmgren, Clifford W. Hansen, and Mark A. Mikofski.
"pvlib python: a python package for modeling solar energy systems."
Journal of Open Source Software, 3(29), 884, (2018). https://doi.org/10.21105/joss.00884
