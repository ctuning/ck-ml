***Reproduced by [Grigori Fursin](https://cKnowledge.io/@gfursin) on 20210428***

# MLPerf Inference v1.0 - Object Detection - TFLite (with Coral EdgeTPU support)

## Prerequisites

### Install Collective Knowledge (CK)

Please follow the [installation instructions](https://github.com/ctuning/ck#installation) for your system e.g.:

```bash
$ python3 -m pip install ck --user
$ echo "export PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
$ source ~/.bashrc && ck version
```

Note that you need GCC 9+!

### Pull [CK-ML repository](https://github.com/ctuning/ck-ml)

```bash
$ ck pull repo:ck-ml
```

### Set up CK environment

```
ck detect platform.os --platform_init_uoa=generic-linux-dummy
ck detect soft:compiler.python --full_path=`which ${PYTHON_EXE}`

ck detect soft:compiler.gcc --full_path=`which gcc`
```

### Install common CK packages
```
ck install package --tags=mlperf,inference,src,r1.0
ck install package --tags=lib,mlperf,loadgen,static
```

## Setup for EdgeTPU

### Install CK packages explicitly

Note that this will install TFLite 1.15.4 and compatible models:

```
ck install package --tags=model,ssd-mobilenet,nhwc,quantized,v1 
ck install package --tags=model,ssd-mobilenet,nhwc,quantized,v2

ck install package --tags=api,model,tensorflow,r1.13.0

ck install package --tags=lib,tflite,for.coral,threads.2

```

### Run experiments

Performance:

```
ck run cmdgen:benchmark.object-detection.tflite-loadgen --verbose \
   --library=tflite-edgetpu \
   --model:=v1:v2 \
   --scenario=singlestream \
   --mode=performance \
   --target_latency=20 \
   --sut=rpi4coral
```

Accuracy:

```
ck run cmdgen:benchmark.object-detection.tflite-loadgen --verbose \
   --library=tflite-edgetpu \
   --model:=v1:v2 \
   --scenario=singlestream \
   --mode=accuracy \
   --dataset_size=5000 \
   --sut=rpi4coral
```

## Setup for RPi4 CPU

### Install CK packages explicitly

~30 min to build

```
ck install package --tags=model,tflite,object-detection,ssd-mobilenet,non-quantized

ck install package --tags=api,model,tensorflow,r2.3.0

ck install package --tags=lib,tflite,via-cmake,v2.4.1,with.ruy --env.CK_HOST_CPU_NUMBER_OF_PROCESSORS=2
```

### Run experiments

Performance:

```
ck run cmdgen:benchmark.object-detection.tflite-loadgen --verbose \
   --library=tflite-v2.4.1-ruy \
   --model=non-quantized \
   --scenario=singlestream \
   --mode=performance \
   --target_latency=170 \
   --sut=rpi4coral

```

Accuracy:
```
ck run cmdgen:benchmark.object-detection.tflite-loadgen --verbose \
   --library=tflite-v2.4.1-ruy \
   --model=non-quantized \
   --scenario=singlestream \
   --mode=accuracy \
   --dataset_size=5000 \
   --sut=rpi4coral

```

Compliance:

```
ck run cmdgen:benchmark.object-detection.tflite-loadgen --verbose \
   --library=tflite-v2.4.1-ruy \
   --model=non-quantized \
   --scenario=singlestream \
   --target_latency=170 \
   --compliance,=TEST04-A,TEST04-B,TEST01,TEST05 \
   --sut=rpi4coral

```

## Notes

* [Extra notes about benchmarking](README.singlestream.md)
* https://github.com/mlcommons/inference_results_v0.7/tree/master/closed/Dividiti/measurements/rpi4coral-tflite-v2.2.0-ruy/ssd-mobilenet-non-quantized/singlestream
* https://github.com/ctuning/ck-mlperf/blob/master/program/object-detection-tflite-loadgen/README.singlestream.md
* https://mlcommons.org/en/inference-edge-07/
* https://mlcommons.org/en/inference-edge-10/
* https://github.com/mlcommons/inference_results_v1.0/blob/master/open/Krai/measurements/rpi4coral-fan.on-tflite-v2.4.1-ruy/efficientnet-lite0-non-quantized/singlestream/README.md#mobilenet_v3


