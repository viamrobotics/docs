---
title: "Calibrate a Camera"
linkTitle: "Calibrate a Camera"
weight: 80
type: "docs"
description: "Calibrate a camera and extract the intrinsic and distortion parameters."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/machine/components/camera/calibrate/"
---

To calibrate a camera, you can use the classical example of a [chessboard](https://en.wikipedia.org/wiki/Chessboard_detection).
The chessboard is often used because the geometry makes it a good test case for detection and processing.

### Prerequisites

The calibration code uses the `numpy` and `opencv-python` packages.
To follow along, install the libraries:

```sh {class="command-line" data-prompt="$"}
pip3 install numpy
pip3 install opencv-python
```

### Instructions

1. Print out the [checkerboard](https://github.com/viam-labs/camera-calibration/blob/main/Checkerboard-A4-25mm-8x6.pdf) and attach it to a flat surface that doesn't distort the checkerboard.
   Good surfaces are completely flat like a table, an non-textured wall or an acrylic plate.
   Do not hold the image in the air with your hands or tape it to a textured surface such as a textured wall, cardboard, or folder.
2. Take images of the checkerboard with your camera from various angles and distances that show the entire image, including the edges.
   Ensure the image is well and thoroughly lit to avoid distortions affecting the vision algorithms.
   You can use the **Export screenshot** button on the camera panel of your machine's **CONTROL** tab in the [Viam app](https://app.viam.com).
   Save between 10 - 15 images (see [examples](https://github.com/viam-labs/camera-calibration#example-images)).

   {{< alert title="Important" color="note" >}}
   In order for the calibration to be compatible with the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, take the images by running the camera using the RDK.
   {{< /alert >}}

   Example of good images:
   ![Example of good images](/machine/components/camera/calibrate/example-images.png)

3. Save [`cameraCalib.py`](https://github.com/viam-labs/camera-calibration/blob/main/cameraCalib.py)
4. Run `python3 cameraCalib.py YOUR_PICTURES_DIRECTORY`.

   Example output:

   ```json {class="line-numbers linkable-line-numbers"}
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

5. Copy the output which contains the `intrinsic_parameters` and `distortion_parameters` into the JSON config on your machine's **CONFIGURE** tab.

{{<imgproc src="/machine/components/camera/camera_tutorial_copy_paste.png" resize="800x" declaredimensions=true alt="Config tab with configuration snippet highlighted">}}

The following is a full example config:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "color",
      "model": "webcam",
      "type": "camera",
      "namespace": "rdk",
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

## Next steps

{{< cards >}}
{{% card link="/machine/components/camera/transform/" %}}
{{% card link="/app/ml/" %}}
{{% card link="/tutorials/services/try-viam-color-detection" %}}
{{< /cards >}}
