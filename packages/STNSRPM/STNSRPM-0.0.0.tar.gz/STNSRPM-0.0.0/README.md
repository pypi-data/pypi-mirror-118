[![DOI](https://zenodo.org/badge/XXXXXXXX.svg)](https://zenodo.org/badge/latestdoi/XXXXXXX)

## Repository supporting the STNSRPM (Spatio-Temporal Newman Scott Rectangular Pulse Model) for synthetic rainfall generation.

This repository contains the utilities for calibrating the STNSRPM and simulate synthetic rainfall series which mimic the observed rainfall statistics (mean, variance, skewness, proportion of dry/wet days, wet/dry transitions probabilities, temporal autocorrelation and spatial correlation) at different temporal aggregations (hourly and daily). The functionality presented here might be very useful to disaggregate rainfall series (from daily to hourly) or for extreme event analysis, among others.

The description of the STNSRPM can be found at [doc](doc).

Overview of STNSRPM: Paper in Environmental Modelling and Software (not available yet)\
Others papers which make use of the STNSRPM: [Paper in Water](https://www.mdpi.com/2073-4441/11/1/125)

## Contents

| Directory | Contents |
| :-------- | :------- |
| [NSRP](NSRP) | Python code for calibrate the NSRPM (Newman Scott Rectangular Pulse Model) and simulate synthetic rainfall series.
  [STNSRP](STNSRP) | Python code for calibrate the STNSRPM (Spatio-Temporal Newman Scott Rectangular Pulse Model) and simulate multisite rainfall series.
| [doc](doc) | Description of the model.
| [notebooks](notebooks) |  Jupyter notebooks with specific examples to calibrate, simulate and validate the STNSRPM.

## Requirements

Scripts and (jupyter) notebooks are provided in [python](https://www.python.org/) language to ensure reproducibility and reusability of the results. The simplest way to match all these requirements is by using a dedicated [conda](https://docs.conda.io) environment, which can be easily installed by issuing:
```sh
conda create -n STNSRPM
conda activate STNSRPM
pip install STNSRPM
```

## Errata and problem reporting

To report an issue with the problem please:
 1. Make sure that the problem has not been reported yet. Check [here](https://github.com/navass11/STNSRPM/issues?q=label%3Aerrata).
 2. Follow [this GitHub issue template](https://github.com/navass11/STNSRPM/issues/new?labels=errata&template=problem-report.md).
