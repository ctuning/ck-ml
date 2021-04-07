# MLPerf Inference - Object Detection - ONNX

# Installation

## Collective Knowledge (CK)

<pre>
&dollar; python3 -m pip install ck --user
</pre>

## CK repositories

<pre>
&dollar; ck pull repo --url=https://github.com/krai/ck-mlperf
</pre>

## ONNX library and runtime

<pre>
&dollar; ck install package --tags=python-package,onnx
&dollar; ck install package --tags=python-package,onnxruntime
</pre>

## Models

### SSD-ResNet34

<pre>
&dollar; ck install package --tags=model,onnx,mlperf,ssd-resnet,downloaded
</pre>

### SSD-MobileNet-v1

<pre>
&dollar; ck install package --tags=model,onnx,mlperf,ssd-mobilenet,downloaded
</pre>


## Datasets

**NB:** Using OpenCV gives better accuracy than using Pillow.

### SSD-ResNet34

<pre>
&dollar; ck install package --tags=dataset,object-detection,preprocessed,full,side.1200
</pre>

### SSD-MobileNet-v1

<pre>
&dollar; ck install package --tags=dataset,object-detection,preprocessed,full,side.300
</pre>


# Inference

## Parameters

### `CK_BATCH_COUNT`

The number of images to be processed.

Default: `1`.

### `CK_SKIP_IMAGES`

The number of images to skip.

Default: `0`.

## Models

### SSD-ResNet34

#### 50 images

<pre>
&dollar; ck run program:object-detection-onnx-py --skip_print_timers \
--dep_add_tags.dataset=preprocessed,using-opencv,side.1200 \
--dep_add_tags.weights=ssd-resnet \
--env.CK_BATCH_COUNT=50
...
Convert results to coco ...

Evaluate metrics as coco ...
loading annotations into memory...
Done (t=0.53s)
creating index...
index created!
Loading and preparing results...
DONE (t=0.03s)
creating index...
index created!
Running per image evaluation...
Evaluate annotation type *bbox*
DONE (t=0.99s).
Accumulating evaluation results...
DONE (t=0.32s).
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.256
 Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.450
 Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.255
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.153
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.420
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.389
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.258
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.363
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.381
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.210
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.517
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.485

Summary:
-------------------------------
All images loaded in 1.812857s
Average image load time: 0.036257s
All images detected in 53.678096s
Average detection time: 1.071682s
Total NMS time: 0.000000s
Average NMS time: 0.000000s
mAP: 0.2555006861214358
Recall: 0.38062334131440473
--------------------------------
</pre>


#### 5,000 images

<pre>
&dollar; ck run program:object-detection-onnx-py --skip_print_timers \
--dep_add_tags.dataset=preprocessed,using-opencv,side.1200 \
--dep_add_tags.weights=ssd-resnet \
--env.CK_BATCH_COUNT=5000
...
Convert results to coco ...

Evaluate metrics as coco ...
loading annotations into memory...
Done (t=0.45s)
creating index...
index created!
Loading and preparing results...
DONE (t=6.37s)
creating index...
index created!
Running per image evaluation...
Evaluate annotation type *bbox*
DONE (t=89.64s).
Accumulating evaluation results...
DONE (t=14.66s).
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.200
 Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.381
 Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.183
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.119
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.257
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.233
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.200
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.321
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.344
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.174
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.406
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.416

Summary:
-------------------------------
All images loaded in 176.739452s
Average image load time: 0.035348s
All images detected in 5474.896789s
Average detection time: 1.094935s
Total NMS time: 0.000000s
Average NMS time: 0.000000s
mAP: 0.19952640873605498
Recall: 0.343745110610767
--------------------------------
</pre>


### SSD-MobileNet-v1

#### 50 images

<pre>
&dollar; ck run program:object-detection-onnx-py --skip_print_timers \
--dep_add_tags.dataset=preprocessed,using-opencv,side.300 \
--dep_add_tags.weights=ssd-mobilenet \
--env.CK_BATCH_COUNT=50
...
executing code ...
Traceback (most recent call last):
  File "../detect.py", line 16, in <module>
    from coco_helper import (load_preprocessed_batch, image_filenames, original_w_h,
  File "/home/anton/CK/ck-mlperf/soft/lib.python.coco-helper/coco_helper/__init__.py", line 70, in <module>
    ) or os.environ['ML_MODEL_CLASS_LABELS']
  File "/usr/local/lib/python3.7/os.py", line 681, in __getitem__
    raise KeyError(key) from None
KeyError: 'ML_MODEL_CLASS_LABELS'
</pre>
