---
title: "Calibrate a Camera"
linkTitle: "Calibrate a Camera"
weight: 46
type: "docs"
description: "Instructions for calibrating a camera."
tags: ["camera", "components"]
---
## Camera Calibration

To calibrate a camera, follow the instructions in the [camera calibration repository](https://github.com/viam-labs/camera-calibration)[^cc] to obtain the `intrinsic_parameters` and `distortion_parameters`.
[^cc]: Camera calibration repository: <a href="https://github.com/viam-labs/camera-calibration" target="_blank">ht<span></span>tps://github.com/viam-labs/camera-calibration</a>

You will need to print out the checkerboard and take images of the checkerboard from various angles by clicking **Export Screenshot** on the camera component control.  

After running the calibration script from the [camera calibration repository](https://github.com/viam-labs/camera-calibration), you'll get a print out of the `intrinsic_parameters` and `distortion_parameters`. We will use the values we've obtained from our camera as an example moving forward:

```json-viam
"intrinsic_parameters": {
    "fy": 940.2928257873841,
    "height_px": 480,
    "ppx": 320.6075282958033,
    "ppy": 239.14408757087756,
    "width_px": 640,
    "fx": 939.2693584627577
},
"distortion_parameters": {
    "rk2": 0.8002516496932317,
    "rk3": -5.408034254951954,
    "tp1": -0.000008996658362365533,
    "tp2": -0.002828504714921335,
    "rk1": 0.046535971648456166
}
```

Copy/paste the parameters you obtained into your camera config by going into the **CONFIG** tab and clicking "Raw JSON".

<img src="../img/configure-a-camera/04_camera_tutorial_copy_paste.png" width="800px"><br>

For us, the finished config now looks like this:

```json-viam
{
  "components": [
    {
      "name": "color",
      "type": "camera",
      "model": "webcam",
      "attributes": {
        "intrinsic_parameters": {
          "fy": 940.2928257873841,
          "height_px": 480,
          "ppx": 320.6075282958033,
          "ppy": 239.14408757087756,
          "width_px": 640,
          "fx": 939.2693584627577
        },
        "distortion_parameters": {
          "rk2": 0.8002516496932317,
          "rk3": -5.408034254951954,
          "tp1": -0.000008996658362365533,
          "tp2": -0.002828504714921335,
          "rk1": 0.046535971648456166
        },
        "stream": "",
        "debug": false,
        "format": "",
        "video_path": "video0",
        "width_px": 0,
        "height_px": 0
      },
      "depends_on": []
    }
  ]
}
```
