# MLPerf Inference - Image Classification - TFLite

1. [Default image](#image_default) (based on [Ubuntu](https://hub.docker.com/_/ubuntu/) 18.04 latest)
    - [Download](#image_default_download) or [Build](#image_default_build)
    - [Run](#image_default_run)
        - [Image Classification (default command)](#image_default_run_default)
        - [Image Classification (custom command)](#image_default_run_custom)
        - [Bash](#image_default_run_bash)

**NB:** You may need to run commands below with `sudo`, unless you
[manage Docker as a non-root user](https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user).

<a name="image_default"></a>
## Default image

<a name="image_default_build"></a>
### Build
```bash
$ ck build docker:image-classification-tflite
```
<a name="image_default_run"></a>
### Run

<a name="image_default_run_default"></a>
#### Image Classification (default command)
```bash
$ ck run docker:image-classification-tflite
```

<a name="image_default_run_custom"></a>
#### Image Classification (custom command)
```bash
$ ck run docker:image-classification-tflite \
  --command="ck run program:image-classification-tflite --dep_add_tags.weights=resnet,no-argmax --env.CK_BATCH_COUNT=10"
```

<a name="image_default_run_bash"></a>
#### Bash
```bash
$ ck run docker:image-classification-tflite --bash
```
