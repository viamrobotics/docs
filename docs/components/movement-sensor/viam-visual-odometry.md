---
title: "Configure Visual Odometry"
linkTitle: "viam-visual-odometry"
weight: 40
type: "docs"
description: "Configure viam-visual-odometry, a modular resource that derives movement data from a camera."
images: ["/icons/components/imu.svg"]
katex: true
# SMEs: Robin In
---

Viam provides a `monocular-visual-odometry` {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} which uses monocular [visual odometry](https://en.wikipedia.org/wiki/Visual_odometry) to enable any [calibrated camera](/components/camera/calibrate/) to function as a movement sensor.
In this way, you can add basic movement sensing to your camera-equipped robot without needing a dedicated hardware [movement sensor](/components/movement-sensor/).

<div class="aligncenter">
{{<video webm_src="/components/movement-sensor/visual-odometry.webm" poster="/components/movement-sensor/visual-odometry-poster.jpg" alt="Using a camera as a motion sensor to navigate a large office space">}}
</div>

The `monocular-visual-odometry` {{< glossary_tooltip term_id="module" text="module" >}} implements the following two methods of the [movement sensor API](/components/movement-sensor/#api):

- [`GetLinearVelocity()`](/components/movement-sensor/#getlinearvelocity)
- [`GetAngularVelocity()`](/components/movement-sensor/#getangularvelocity)

Note that `GetLinearVelocity()` returns an estimation of the instantaneous linear velocity **without scale factor**.
Therefore, you should not consider returned unit measurements trustworthy: instead, `GetLinearVelocity()` should serve as a direction estimation only.

While `monocular-visual-odometry` enables you to add movement sensing abilities to your robot without needing specialized hardware, a dedicated [movement sensor](/components/movement-sensor/) will generally provide more accurate readings.
If your robot requires precise awareness of its location and its movement, you should consider using a dedicated movement sensor in addition to the `monocular-visual-odometry` module.

The `monocular-visual-odometry` module is available [from the Viam registry](https://app.viam.com/module/viam/monocular-visual-odometry).
See [Modular resources](/registry/#the-viam-registry) for instructions on using a module from the Viam registry on your robot.

The source code for this module is available on the [`viam-visual-odometry` GitHub repository](https://github.com/viamrobotics/viam-visual-odometry).

## Requirements

If you haven't already, [install `viam-server`](/installation/) on your robot.

Your robot must have a [camera](/components/camera/) in order to use the `monocular-visual-odometry` module.
These instructions assume that you are using a [webcam](/components/camera/webcam/)) type camera, but you can use any type of camera with visual odometry.

## Configuration

Follow the instructions below to set up the `monocular-visual-odometry` module on your robot:

{{< tabs name="Configure visual odometry">}}
{{% tab name="Config Builder" %}}

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Components** subtab and click **Create component** in the lower-left corner.
1. Select the `camera` type, then select the `webcam` model.
1. Enter a name for your camera, then click **Create**.
1. In the resulting camera component configuration pane, select a **Video path** for your camera.
   If your robot is live, the drop-down menu auto-populates any identified camera stream paths.
1. Then, click **Create component** in the lower-left corner again.
1. Select **Movement Sensor**, then select `visual_odometry:opencv_orb`.
   You can also search for "visual_odometry".
1. Click **Add module**, give your component a name of your choice, then click **Create**.
1. In the resulting `movement_sensor` component configuration pane, paste the following configuration into the **Attributes** text window:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "camera_name": "<your-camera-name>",
     "time_between_frames_s": <time_seconds>,
     "lowe_ratio_threshold": <lowe_ratio_threshold>
   }
   ```

   Provide the camera name you used in step 4.
   See the [Attributes](#attributes) section for more information on the other attributes.

1. Click **Save config** at the bottom of the page.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "type": "registry",
      "name": "viam_monocular-visual-odometry",
      "module_id": "viam:monocular-visual-odometry",
      "version": "0.0.8"
    }
  ],
  "components": [
    {
      "name": "<your-camera-name>",
      "model": "webcam",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {
        "video_path": "<path-to-video-stream>",
        "height_px": <height>,
        "width_px": <width>,
        "intrinsic_parameters": {
          "ppx": <ppx>,
          "ppy": <ppy>,
          "fx": <fx>,
          "fy": <fy>
        },
        "distortion_parameters": {
          "rk3": <rk3>,
          "tp1": <tp1>,
          "tp2": <tp2>,
          "rk1": <rk1>,
          "rk2": <rk2>
        }
      },
      "depends_on": []
    },
    {
      "name": "<your_movement_sensor_name>",
      "type": "movement_sensor",
      "namespace": "rdk",
      "model": "viam:visual_odometry:opencv_orb",
      "attributes": {
        "camera_name": "<your-camera-name>",
        "time_between_frames_s": <time_seconds>,
        "lowe_ratio_threshold": <lowe_ratio_threshold>
      },
      "depends_on": []
    }
  ]
}
```

To save your changes, click **Save config** at the bottom of the page.

{{% /tab %}}
{{% tab name="JSON Example" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "type": "registry",
      "name": "viam_monocular-visual-odometry",
      "module_id": "viam:monocular-visual-odometry",
      "version": "0.0.8"
    }
  ],
  "components": [
    {
      "name": "my-camera",
      "model": "webcam",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {
        "video_path": "FDF90FEB-59E5-4FCF-AABD-DA03C4E19BFB",
        "height_px": 720,
        "width_px": 1280,
        "intrinsic_parameters": {
          "ppx": 446,
          "ppy": 585,
          "fx": 1055,
          "fy": 1209
        },
        "distortion_parameters": {
          "rk3": -0.03443,
          "tp1": 0.01364798,
          "tp2": -0.0107569,
          "rk1": -0.1621,
          "rk2": 0.13632
        }
      },
      "depends_on": []
    },
    {
      "name": "my_movement_sensor",
      "type": "movement_sensor",
      "namespace": "rdk",
      "model": "viam:visual_odometry:opencv_orb",
      "attributes": {
        "camera_name": "my-camera",
        "time_between_frames_s": 0.2,
        "lowe_ratio_threshold": 0.75
      },
      "depends_on": []
    }
  ]
}
```

To save your changes, click **Save config** at the bottom of the page.

{{% /tab %}}
{{< /tabs >}}

## Camera calibration

Once you have configured a `camera` component, you need to calibrate it.
Because the `monocular-visual-odometry` module performs visual odometry calculations, its visual data source (the camera) must be as well defined as possible.
These calibration steps ensure that the video stream data that reaches the module is as uniform as possible when calculating measurements.

1. Follow the [Calibrate a camera](/components/camera/calibrate/) procedure to generate the required intrinsic parameters specific to your camera.
1. Copy the resulting intrinsics data into your robot configuration, either in the **Config builder** or in the **Raw JSON**.
   See the JSON Example tab above for an example intrinsics configuration.

Camera calibration results should look similar to the following example, with readings specific to your camera:

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

{{% alert title="Copy calibration data" color="note" %}}
When you copy the calibration results into your `camera` component configuration, be sure to provide these values to the correct attributes in the target `camera` configuration.
Specifically, note that the `height_px` and `width_px` attributes are not contained within the `intrinsic_parameters` array in the `camera` configuration, but are located outside of it.
{{% /alert %}}

## Attributes

The following attributes are available to configure the `monocular-visual-odometry` module:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Default | Description |
| ---- | ---- | --------- | --------| ------------ |
| `camera_name` | string | **Required** | | Camera name to be used for inferring the motion. |
| `time_between_frames_s` | float | Optional | `0.1` | Target time between two successive frames, in seconds. Depending on the inference time and the time to get an image, the sleeping time after each inference will be auto-tuned to reach this target. Additionally, if the time between two successive frame is 5x larger than `time_between_frames_s`, another frame will be requested. This value depends on the speed of your system.|
|`orb_n_features`| int | Optional | `10000` | Maximum number of features to retain. |
|`orb_edge_threshold`| int | Optional | `31` | Size of the border where the features are not detected. It should roughly match the `orb_patch_size` attribute.  |
|`orb_patch_size`| int | Optional | `31` | Size of the patch used by the oriented BRIEF descriptor.|
|`orb_n_levels`| int | Optional | `8` |Number of pyramid levels.|
|`orb_first_level`| int | Optional | `0` |Level of pyramid to put source image into.|
|`orb_fast_threshold`| int | Optional | `20` | Fast threshold. |
|`orb_scale_factor`| float | Optional | `1.2` | Pyramid decimation ratio, greater than 1. |
|`orb_WTA_K`| int | Optional | `2` | Number of points that produce each element of the oriented BRIEF descriptor. |
|`matcher`| string | Optional | `"flann"` | Either `"flann"` for [FLANN based matcher](https://docs.opencv.org/3.4/d5/d6f/tutorial_feature_flann_matcher.html) or `"BF"` for brute force matcher. The FLANN matcher will look for the two best matches using the KNN method so Lowe's ratio test can be performed afterward. The [brute force matcher](https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html) uses Hamming norm. |
|`lowe_ratio_threshold`| float | Optional | `0.8` | Threshold value to check if the best match is significantly better than the second best match. This value will not be used if brute force matcher is chosen. |
| `ransac_prob` | float | Optional | `0.99` | Probability to find a subset without outliers in it. Defines the number of iterations to filter the outliers. The number of iterations is roughly given by `$k = \frac{\log(1-p)}{\log(1-w^n)}$`, where `$n$` is the number of points and `$w$` is the ratio of inliers to total points.|
| `ransac_threshold_px` | float | Optional | `0.5` | Maximum error to be classified as an inlier.|

See the [ORB openCV documentation](https://docs.opencv.org/3.4/db/d95/classcv_1_1ORB.html) for more details.

## Test the movement sensor

After you configure your movement sensor, navigate to the [Control tab](/manage/fleet/robots/#control) and select the dedicated movement sensor dropdown panel.
This panel presents the data collected by the movement sensor.
