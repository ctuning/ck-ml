﻿# Demo of MLPerf dashboards for ML Systems DSE (Linux and Windows)

This Docker image demonstrates how to run CK experiments and record results 
from the Docker in the local "ck-experiments" repository on the host machine
to be processed in Jupyter notebooks or visualized using CK dashboards.

## Install CK
```
python3 -m pip install ck
```

## Pull this repository via CK
```
ck pull repo:ck-ml
```

## Create local ck-experiments repo
```
ck add repo:ck-experiments --quiet
```

## Build this docker
```
ck build docker:ck-mlperf-local-dashboard-demo
```

## Run this docker

You must run this container using a special script from this directory:
* Linux: [docker-start.sh](docker-start.sh)
* Windows: [docker-start.bat](docker-start.bat)

This script will mount local CK ck-experiments repo inside Docker
to be able to record experiments there from the Docker container.

This script will call a helper script [docker-helper.sh] with benchmarks
that you can modify to run different experiments.

## View CK dashboard localy

Run the following command from your host machine to visualize results:
```
ck display dashboard --scenario=mlperf.mobilenets
```

## Feedbacok

Contact [Grigori Fursin](https://cKnowledge.io/@gfursin)