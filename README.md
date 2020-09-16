# Social-Distance-Monitoring

## Introduction

This repository holds the implementation of detecting vehicles and monitoring their distances using  [YOLACT++: Better Real-time Instance Segmentation](https://arxiv.org/abs/1912.06218)) for object detection.

It is based on the repository [Social-Distance-Monitoring](https://github.com/paul-pias/Social-Distance-Monitoring) by Paul Pias.

## User Guideline

### System Requirements

- For utilizing GPU you'll need CUDA version 10.x
- Python 3.7

### Installation

This repo is modified to be used on Windows 10 (2004).
You can install all packages by running:

```console
    pip install -r requirements.txt
```

or manually installing all packages listed there.

For the installation of torch using "pip" kindly follow the instructions from [Pytorch](https://pytorch.org/).

First, you need to clone the repository.

```console
    git clone https://github.com/ArVar/Vehicle-Distance.git
```

You can run the inference using `inference.py` from command line (options see below).
If you want to see your output in your browser, please execute the "server.py" script, which starts a flask app.

If you want to run the inference on a ip camera need to use `WebcamVideoStream` with the following command:

```console
    "rtsp://assigned_name_of_the_camera:assigned_password@camer_ip/"
```

An example stream is available at:

```console
    "rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa"
```

To use YOLACT++, make sure you have the latest [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) installed. Further, you need to compile deformable convolutional layers (from [DCNv2](https://github.com/CharlesShang/DCNv2/tree/pytorch_1.0)). You can achieve this by running:

```console
    cd external/DCNv2
    python setup.py build develop
```

In the official [Yolact repository](https://github.com/dbolya/yolact) are several pre-trained model available:
|    Image Size            |Model File (-m)                       |Config (-c)                   |
|----------------|-------------------------------|-----------------------------|
|550|[yolact_resnet50_54_800000.pth](https://drive.google.com/file/d/1yp7ZbbDwvMiFJEq4ptVKTYTI2VeRDXl0/view?usp=sharing)            |yolact_resnet50            |
|550          |[yolact_darknet53_54_800000.pth](https://drive.google.com/file/d/1dukLrTzZQEuhzitGkHaGjphlmRJOjVnP/view?usp=sharing)           |yolact_darknet53            |
|550          |[yolact_base_54_800000.pth](https://drive.google.com/file/d/1UYy3dMapbH1BnmtZU4WH1zbYgOzzHHf_/view?usp=sharing)|yolact_base|
|700|[yolact_im700_54_800000.pth](https://drive.google.com/file/d/1lE4Lz5p25teiXV-6HdTiOJSnS7u7GBzg/view?usp=sharing)            |yolact_im700            |
|550         |[yolact_plus_resnet50_54_800000.pth](https://drive.google.com/file/d/1ZPu1YR2UzGHQD0o1rEqy-j5bmEm3lbyP/view?usp=sharing)            |yolact_plus_resnet50            |
|550          |[yolact_plus_base_54_800000.pth](https://drive.google.com/file/d/15id0Qq5eqRbkD-N3ZjDZXdCvRyIaHpFB/view?usp=sharing)|yolact_plus_base|

### Things to consider

Download the pre-trained weights and save in the folder `./weights` (related to your project root), then from your terminal run the following command based on your preference:

```console
    python inference.py -m=weights/yolact_base_54_800000.pth -c=yolact_base -i 0
```

Here 0 as id passed if you want to run the inference on webcam feed. If you don't parse any argument it will run with the default values. You can tweak the following values according to your preference.

|      Input          |Value                        |Description                         |
|----------------|-------------------------------|-----------------------------|
|width, height      |`1280 x 720`   | Resolution of the output video.
|display_lincomb    |`False`
|crop               |`True`         | For better segmentation use this flag as `True`.
|score_threshold    |`0.15`         | The higher the value, the less objects are detected, the better the performance.
|top_k              |`30`           | At max how many objects will the model consider to detect in a given frame.
|display_masks      |`True`         | Draw segmentation masks.
|display_fps        |`False`        |
|display_text       |`True`
|display_bboxes     |`True`
|display_scores     |`False`
|fast_nms           |`True`
|cross_class_nms    |`True`
|display_text       |`True`

### Measuring the Distances

To measure distance between two vehicles Euclidean distance is used. **Euclidean distance** or **Euclidean metric** is the "ordinary" [straight-line](https://en.wikipedia.org/wiki/Straight_line "Straight line")  [distance](https://en.wikipedia.org/wiki/Distance "Distance") between two points in [Euclidean space](https://en.wikipedia.org/wiki/Euclidean_space "Euclidean space").

The **Euclidean distance** between two points **p** and **q** is the length of the [line segment](https://en.wikipedia.org/wiki/Line_segment "Line segment") connecting them ![\overline{\mathbf{p}\mathbf{q}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/6d397a90d8e00a9fbb6e7eb908cda31009fde6ee).
In the [Euclidean plane](https://en.wikipedia.org/wiki/Euclidean_plane "Euclidean plane"), if **p** = (p1, p2) and **q** = (q1, q2) then the distance is given by

![{\displaystyle d(\mathbf {p} ,\mathbf {q} )={\sqrt {(q_{1}-p_{1})^{2}+(q_{2}-p_{2})^{2}}}.}](https://wikimedia.org/api/rest_v1/media/math/render/svg/4febdae84cbc320c19dd13eac5060a984fd438d8)

This formula was applied in the **draw_distance(boxes)** function where we got all the bounding boxes of vehicle classes `car` and `truck` in a given frame from the model where each bounding is a regression value consisting `(x,y,w,h)` . Where `x` and `y` represent 2 coordinates of the vehicle. `w` and `h` represent width and height correspondingly. All combinations of boxes are used to calculate the distances between them.

### Acknowledgements

Thanks to **Paul Pias** for providing his [repository](https://github.com/paul-pias/Social-Distance-Monitoring) on github. It was a very good starting point with just very few caveats when running on Windows. I recommend, checking out his other repos as well.

Thanks to **Daniel Bolya** et. el for introducing Single Shot detection (SSD) implementation for segmentation in  [YOLACT](https://arxiv.org/abs/1904.02689) & [YOLACT++](https://arxiv.org/abs/1912.06218) as it becomes less memory hungry.
