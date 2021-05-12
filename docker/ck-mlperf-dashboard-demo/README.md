﻿# Demo of MLPerf dashboards for ML Systems DSE (Linux and Windows)

## Install CK
```
python3 -m pip install ck
```

## Pull this repository via CK
```
ck pull repo:ck-ml
```

## Build this docker
```
ck build docker:ck-mlperf-dashboard-demo
```

Note that it will build and run several MLPerf benchmarks while recording results
to the CK 'experiment' entries to be used in the CK dashboard.

## Run this docker
```
ck run docker:ck-mlperf-dashboard-demo
```

## View CK dashboard in your browser

Go to http://localhost:3355/?template=dashboard&scenario=mlperf.mobilenets

## Feedbacok

Contact [Grigori Fursin](https://cKnowledge.io/@gfursin)