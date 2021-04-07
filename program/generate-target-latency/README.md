# Description

This program performs "performance ranging" by extracting the mean latency over a fixed number of queries.
This latency can then be used for proper performance runs. This is especially useful for families of models
such as MobileNet and EfficientNet where the performance can range by an order of magnitude.

# Usage

## Store

Run `cmdgen:benchmark.*` with `--scenario=range_singlestream --max_query_count=<...>` arguments to store performance ranging results to the local CK repo.

### Example

```bash
$ ck run cmdgen:benchmark.image-classification.tflite-loadgen --library=tflite-v2.4.1-ruy \
--model:=`ck list_variations misc --query_module_uoa=package --tags=model,tflite,effnet --variation_prefix=lite --separator=:` \
--model_extra_tags,=non-quantized,quantized \
--mode=performance --scenario=range_singlestream --max_query_count=256 \
--sut=rpi4coral --fan_mode=on
```

## Extract

Use this script to extract the ranging results from the CK repo.
All arguments are optional.

```bash
$ ck run ck-mlperf:program:generate-target-latency \
  --env.CK_MLPERF_SUBMISSION_REPO=local \
  --env.CK_MLPERF_SUBMISSION_TAGS=foo,bar \
  --env.CK_MLPERF_SUBMISSION_OUT="$PWD"/target_latency.txt
```

Alternatively:

```bash
$ cd $(ck find program:generate-target-latency) && ./run.py \
  --repo-uoa local \
  --tags foo,bar \
  --out $(pwd)/target_latency.txt
```

### Example

```bash
$ $(ck find program:generate-target-latency)/run.py --tags=inference_engine.tflite | sort | tee $(ck find program:image-classification-tflite-loadgen)/target_latency.rpi4coral.txt
rpi4coral,tflite-v2.4.1-ruy,efficientnet-lite0-non-quantized   70 # max_query_count=256
rpi4coral,tflite-v2.4.1-ruy,efficientnet-lite0-quantized   34 # max_query_count=256
rpi4coral,tflite-v2.4.1-ruy,efficientnet-lite1-non-quantized   99 # max_query_count=256
rpi4coral,tflite-v2.4.1-ruy,efficientnet-lite1-quantized   49 # max_query_count=256
rpi4coral,tflite-v2.4.1-ruy,efficientnet-lite2-non-quantized  136 # max_query_count=256
rpi4coral,tflite-v2.4.1-ruy,efficientnet-lite2-quantized   67 # max_query_count=256
rpi4coral,tflite-v2.4.1-ruy,efficientnet-lite3-non-quantized  203 # max_query_count=256
rpi4coral,tflite-v2.4.1-ruy,efficientnet-lite3-quantized  101 # max_query_count=256
rpi4coral,tflite-v2.4.1-ruy,efficientnet-lite4-non-quantized  342 # max_query_count=256
rpi4coral,tflite-v2.4.1-ruy,efficientnet-lite4-quantized  169 # max_query_count=256
```

### Tags

The tags are related to experiments, i.e. the following query matches the same experiments as `./run.py --tags=$tags`:

```bash
$ ck search experiment --tags=mlperf,scenario.range_singlestream.$tags`
```

You can use the following one-liner to list tags for particular ranging experiments:
```bash
 $ for i in $(ck search experiment --tags=mlperf,scenario.range_singlestream); do echo $i; ck list_tags $i; echo; done
```

## Use

Run `cmdgen:benchmark.*` with `--target_latency_file=<...>` instead of `--target_latency=<...>`.

### Example

```bash
$ ck run cmdgen:benchmark.image-classification.tflite-loadgen --library=tflite-v2.4.1-ruy \
--model:=`ck list_variations misc --query_module_uoa=package --tags=model,tflite,effnet --variation_prefix=lite --separator=:` \
--model_extra_tags,=non-quantized,quantized \
--mode=performance --scenario=singlestream --sut=rpi4coral --fan_mode=on \
--target_latency_file=$(ck find program:image-classification-tflite-loadgen)/target_latency.rpi4coral.txt \
--power=yes --power_server_port=4951 --power_server_ip=192.168.0.3
```
