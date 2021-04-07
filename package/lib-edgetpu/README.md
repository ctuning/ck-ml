## Coral edgetpu package

This package installs the driver required to run the Coral edgetpu.

There are two versions; std and max.

```
$ ck install package --tags=lib,edgetpu,std_14.1_arm64
$ ck install package --tags=lib,edgetpu,max_14.1_arm64
```

For instructions on how run, please see [`program:object-detection-tflite-loadgen`](https://github.com/ctuning/ck-mlperf/blob/master/program/object-detection-tflite-loadgen/README.singlestream.md).
