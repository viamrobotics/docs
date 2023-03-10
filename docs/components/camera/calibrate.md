---
title: "Calibrate a Camera"
linkTitle: "Calibrate a Camera"
weight: 50
type: "docs"
description: "Calibrate a camera and extract the intrinsic and distortion parameters."
tags: ["camera", "components"]
---

### Prerequisites

The calibration code uses the `numpy` and `opencv-python` packages.
To follow along, install the libraries:

```bash
pip3 install numpy
pip3 install opencv-python
```

### Instructions

1. Print out the [checkerboard](https://github.com/viam-labs/camera-calibration/blob/main/Checkerboard-A4-25mm-8x6.pdf) and attach it to a flat surface that doesn't distort the checkerboard.
2. Take images of the checkerboard with your camera from various angles and distances.
   You can use the **Export Screenshot** button on the camera panel of your robot's **CONTROL** tab in the [Viam app](https://app.viam.com).
   Save between 10 - 15 images (see [examples](https://github.com/viam-labs/camera-calibration#example-images)).

   {{< alert title="Note" color="note" >}}
   In order for the calibration to be compatible with the rdk, take the images by running the camera using the rdk.
   {{< /alert >}}
3. Save [`cameraCalib.py`](https://github.com/viam-labs/camera-calibration/blob/main/cameraCalib.py)
4. Run `python3 cameraCalib.py YOUR_PICTURES_DIRECTORY`.

   Example output:

   ```json-viam {class="line-numbers linkable-line-numbers"}
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

5. Copy the output which contains the `intrinsic_parameters` and `distortion_parameters` into the Raw JSON config on your robot's **CONFIG** tab.

<img src="../img/camera_tutorial_copy_paste.png" width="800px"><br>

The following is a full example config:

```json-viam {class="line-numbers linkable-line-numbers"}
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

## Next Steps

<div class="container text-center">
  <div class="row">
    <div class="col hover-card">
        <a href="../transform/">
        <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">
            Transform a Camera
        </h4>
        </a>
        <p style="text-align: left;"> Calibrate a camera and extract the intrinsic and distortion parameters. </p>
    </div>
    <div class="col hover-card">
        <a href="control-a-component">
        <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">Vision Service</h4>
        <p style="text-align: left;">The vision service enables your robot to use its on-board cameras to intelligently see and interpret the world around it.</p>
        <a>
    </div>
    <div class="col hover-card">
        <a href="/tutorials/viam-rover/try-viam-color-detection/">
            <h4 style="text-align: left; margin-left: 0px;">Detect color with a Viam Rover</h4>
            <p style="text-align: left;">Use the vision service in the Viam app to detect a color.</p>
        </a>
    </div>
  </div>
</div>
