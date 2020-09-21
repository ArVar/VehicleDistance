# Vehicle-Distance-Monitoring

This repository holds the implementation of detecting vehicles and indicating risky distances using  [YOLACT++: Better Real-time Instance Segmentation](https://arxiv.org/abs/1912.06218)) for object detection.

It is based on the repositories [Social-Distance-Monitoring](https://github.com/paul-pias/Social-Distance-Monitoring) by Pias Paul and [YOLACT](https://github.com/dbolya/yolact) by Daniel Bolya.

![image info](./data/output.gif)

## System Requirements

- CUDA 10.2 (for utilizing GPU you'll need CUDA version 10.x)
- Python 3.7 (3.6 should also be possible, 3.8 I haven't tested)

## Used Stack

- PyTorch 1.6.0 (with torchvision 0.7.0)
- OpenCV 4.4.0
- Flask 1.1.2

## Installation

This repo is modified to be used on Windows 10 (2004).

I highly recommend to use a virtual environment with `conda` or `virtualenv`.

First, you need to clone the repository and go into this directory (project root):

```console
    git clone https://github.com/ArVar/VehicleDistance.git
    cd VehicleDistance
```

You can install all packages by running:

```console
    pip install -r requirements.txt
```

You can also manually install all packages listed in this file.

Feel free to experiment with different versions of the packages (as I've done).
When trying to build up on a newer stack, keep in mind to use the right CUDA toolkit and PyTorch combination.
For the installation of PyTorch with "pip" please follow the instructions from [Pytorch](https://pytorch.org/).

This repo is mainly meant to watch the inference stream in your browser. When executing the `server.py` script a flask app will start and provide the interface.
You can also run the inference using `inference.py` from command line (options see below).

If you want to run the inference on a ip camera need to use `WebcamVideoStream` with the following source in `webapp.py`:

```console
    "rtsp://assigned_name_of_the_camera:assigned_password@camer_ip/"
```

An example stream is available at:

```console
    "rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa"
```

To be able to use YOLACT++, make sure you have the [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) ($\geq$ 10.x) installed. Further, you need to compile deformable convolutional layers (from [DCNv2](https://github.com/CharlesShang/DCNv2/tree/pytorch_1.0)). You can achieve this by running (in project root):

```console
    cd external/DCNv2
    python setup.py build develop
```

### Download pre-trained Models

The official [Yolact repository](https://github.com/dbolya/yolact) offers several pre-trained models:
|    Image Size            |Model File (-m)                       |Config (-c)                   |
|----------------|-------------------------------|-----------------------------|
|550|[yolact_resnet50_54_800000.pth](https://drive.google.com/file/d/1yp7ZbbDwvMiFJEq4ptVKTYTI2VeRDXl0/view?usp=sharing)            |yolact_resnet50            |
|550          |[yolact_darknet53_54_800000.pth](https://drive.google.com/file/d/1dukLrTzZQEuhzitGkHaGjphlmRJOjVnP/view?usp=sharing)           |yolact_darknet53            |
|550          |[yolact_base_54_800000.pth](https://drive.google.com/file/d/1UYy3dMapbH1BnmtZU4WH1zbYgOzzHHf_/view?usp=sharing)|yolact_base|
|700|[yolact_im700_54_800000.pth](https://drive.google.com/file/d/1lE4Lz5p25teiXV-6HdTiOJSnS7u7GBzg/view?usp=sharing)            |yolact_im700            |
|550         |[yolact_plus_resnet50_54_800000.pth](https://drive.google.com/file/d/1ZPu1YR2UzGHQD0o1rEqy-j5bmEm3lbyP/view?usp=sharing)            |yolact_plus_resnet50            |
|550          |[yolact_plus_base_54_800000.pth](https://drive.google.com/file/d/15id0Qq5eqRbkD-N3ZjDZXdCvRyIaHpFB/view?usp=sharing)|yolact_plus_base|

Download the pre-trained weights and save in the folder `./weights` (related to your project root). For instance, the yolact_plus_base is hardcoded in `webapp.py`.

### Running the webapp

Now you can run the webapp via:

```console
    python server.py
```

This starts the webserver and the webapp. With the standard configuration the webapp is locally reachable via [localhost:5000](http://localhost:5000).

### Running from CLI

Alternatively, you can run the inference from your terminal with the following command:

```console
    python inference.py -m=weights/yolact_base_54_800000.pth -c=yolact_base -i 0
```

Here `-i 0` defines the device id. Use `0` if you want to run the inference on your webcam feed. If you don't parse any argument it will run with the default values. You can tweak the following values according to your preferences.

|Input              |Standard Value |Description                  |
|-------------------|---------------|-----------------------------|
|width, height      |`1280 x 720`   | Resolution of the output video.
|display_lincomb    |`False`        | Display Lincomb masks (if the config uses them).
|crop               |`True`         | For better segmentation use this flag as `True`.
|score_threshold    |`0.15`         | The higher the value, the less objects are detected, the better the performance.
|top_k              |`30`           | At max how many objects will the model consider to detect in a given frame.
|display_masks      |`True`         | Draw segmentation masks.
|display_fps        |`True`         | Display FPS counter.
|display_text       |`True`         | Allow to display text.
|display_bboxes     |`True`         | Display bounding boxes around detected objects.
|display_scores     |`True`         | Display classification score.
|fast_nms           |`True`         | Use fast NMS (Non-Maximum-Supression).
|cross_class_nms    |`True`         | Use Cross-Class-NMS.

## Measuring the Distances

To measure distance between two vehicles Euclidean distance is used. **Euclidean distance** or **Euclidean metric** is the "ordinary" [straight-line](https://en.wikipedia.org/wiki/Straight_line "Straight line")  [distance](https://en.wikipedia.org/wiki/Distance "Distance") between two points in [Euclidean space](https://en.wikipedia.org/wiki/Euclidean_space "Euclidean space").

The **Euclidean distance** between two points **p** and **q** is the length of the [line segment](https://en.wikipedia.org/wiki/Line_segment "Line segment") connecting them ![\overline{\mathbf{p}\mathbf{q}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/6d397a90d8e00a9fbb6e7eb908cda31009fde6ee).
In the [Euclidean plane](https://en.wikipedia.org/wiki/Euclidean_plane "Euclidean plane"), if **p** = (p1, p2) and **q** = (q1, q2) then the distance is given by

![{\displaystyle d(\mathbf {p} ,\mathbf {q} )={\sqrt {(q_{1}-p_{1})^{2}+(q_{2}-p_{2})^{2}}}.}](https://wikimedia.org/api/rest_v1/media/math/render/svg/4febdae84cbc320c19dd13eac5060a984fd438d8)

This formula was applied in the **draw_distance(boxes)** function where we got all the bounding boxes of vehicle classes `car` and `truck` in a given frame from the model where each bounding is a regression value consisting `(x,y,w,h)` . Where `x` and `y` represent 2 coordinates of the vehicle. `w` and `h` represent width and height correspondingly. All combinations of boxes are used to calculate the distances between them.

## Acknowledgements

Thanks to **Pias Paul** for providing his [repository](https://github.com/paul-pias/Social-Distance-Monitoring) on github. It was a very good starting point with just very few caveats when running on Windows. I recommend, checking out his other repos as well.

Thanks to **Daniel Bolya** et. el for introducing Single Shot detection (SSD) implementation for segmentation in  [YOLACT](https://arxiv.org/abs/1904.02689) & [YOLACT++](https://arxiv.org/abs/1912.06218) as it becomes less memory hungry.
