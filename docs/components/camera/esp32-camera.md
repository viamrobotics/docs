---
title: "Configure an esp32-camera (Micro-RDK)"
linkTitle: "esp32-camera"
weight: 33
type: "docs"
description: "Configure a camera connected to an esp32 board, initialized and configured using esp-idf."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components", "micro-RDK"]
component_description: "An `OV2640` or `OV3660` camera connected to an esp32 board."
usage: 10
toc_hide: true
# SMEs: Matt Perez, micro-RDK team
---

`esp32-camera` is the camera model for cameras connected to an `esp32` board, which are initialized and configured using the [Micro-RDK Development Setup](/installation/micro-rdk-dev/) (ESP-IDF).
If the camera drivers are one of the following two, the camera will work with the `esp32-camera` model:

- `OV2640`
  - [Datasheet](https://www.uctronics.com/download/OV2640_DS.pdf)
  - 1600 x 1200, Color, ¼” lens
  - You can use a cam ribbon adapter to connect to your `esp32` board

- `OV3660`: an [m5 camera timer module](https://docs.m5stack.com/en/unit/timercam_f)
  - [Datasheet](https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/unit/OV3660_CSP3_DS_1.3_sida.pdf)
  - 2048 x 1536, Color, ⅕” lens

## Software requirements

To use this module, you must follow the [Micro-RDK Development Setup](/installation/micro-rdk-dev/), which enables you to install and activate the ESP-IDF.
At the step [Generate a new project from the micro-RDK template](/installation/micro-rdk-dev/#generate-a-new-project-from-the-micro-RDK-template) where you create a new project with `cargo generate`, select the option to include camera module traits when prompted.
Finish the [Micro-RDK Development Setup](/installation/micro-rdk-dev/) and return to this guide.

{{< alert title="Info" color="info" >}}

The`esp32-camera` camera model is not currently available as a built-in option in [the Viam app](https://app.viam.com), so you cannot use **Builder** mode to configure this board.

{{< /alert >}}

{{< tabs name="Configure a esp32-camera" >}}
{{% tab name="JSON Template" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Select **Builder** mode.
Copy and paste the following JSON into your existing machine configuration in the `"components"` level:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "esp32-camera",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "intrinsic_parameters": {
      "width_px": <int>,
      "height_px": <int>,
      "fx": <float>,
      "fy": <float>,
      "ppx": <float>,
      "ppy": <float>
    },
    "distortion_parameters": {
      "rk1": <float>,
      "rk2": <float>,
      "rk3": <float>,
      "tp1": <float>,
      "tp2": <float>
    },
    "debug": <boolean>,
    "format": <string>,
    "video_path": "<your-video-path>",
    "width_px": <int>,
    "height_px": <int>,
    "frame_rate": <float>
  }
}
```

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my_cam",
  "model": "esp32-camera",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "video_path": "video0"
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `esp32-camera` cameras:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `video_path` | string | Optional | The ID of or the path to the esp32-camera. If you don't provide a `video_path`, it defaults to the first valid video path it finds. Using the ID of a esp32-camera is more consistent than the path. See [Using `video_path`](#using-video_path). |
| `format` | string | Optional | The camera image format, used with `video_path` to find the camera. See [Using `format`](#using-format). |
| `width_px` | int | Optional | The camera image width in pixels, used with `video_path` to find a camera with this resolution. <br> Default: Closest possible value to `480` |
| `height_px` | int | Optional | The camera image height in pixels, used with `video_path` to find a camera with this resolution. <br> Default: Closest possible value to `640` |
| `frame_rate` | float | Optional | The camera capture frequency as frames per second, used with `video_path` to find a camera with this throughput. <br> Default: Closest possible value to `30.0` |
| `intrinsic_parameters` | object | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> `width_px`: The expected width of the aligned image in pixels. </li> <li> `height_px`: The expected height of the aligned image in pixels. </li> <li> `fx`: The image center x point. </li> <li> `fy`: The image center y point. </li> <li> `ppx`: The image focal x. </li> <li> `ppy`: The image focal y. </li> </ul> |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> `rk1`: The radial distortion x. </li> <li> `rk2`: The radial distortion y. </li> <li> `rk3`: The radial distortion z. </li> <li> `tp1`: The tangential distortion x. </li> <li> `tp2`: The tangential distortion y. </li> </ul> |
| `debug` | boolean | Optional | Enables the debug outputs from the camera if `true`. <br> Default: `false` |

## Using `video_path`

To list available `video_path`s use the following command:

{{< tabs name="Find video devices" >}}
{{% tab name="Linux" %}}

```sh
ls /dev/v4l/by-id/
```

To find the `path`s of all connected video devices, run the following command:

```sh
v4l2-ctl --list-devices
```

The `id` listed by `ls /dev/v4l/by-id/` is a more consistent way to refer to the esp32-camera.

See [Camera troubleshooting](/appendix/troubleshooting/#error-failed-to-find-camera) for Linux-specific camera troubleshooting steps.

{{% /tab %}}
{{% tab name="Mac" %}}

```sh
system_profiler SPCameraDataType
```

The Unique ID displayed for each camera is the `video_path`.

{{% /tab %}}
{{< /tabs >}}

## Using `format`

Viam supports the following pixel formats:

- I420
- I444
- MJPEG / MJPG
- NV12
- NV21
- RGBA
- UYVY / Y422
- YUY2 / YUYV / V422
- Z16

If your machine is connected to the Viam app, the available pixel formats supported by your camera automatically appear in the **Format** dropdown menu, which is visible when you click the **Show more** button.

On Linux, you can also manually determine which pixel formats your camera supports by running the following command on the machine your camera is connected to.
Replace `/dev/video0` with the video path you [determined for your video device above](#using-video_path), if different:

```sh {class="command-line" data-prompt="$"}
v4l2-ctl --list-formats-ext --device /dev/video0
```

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Troubleshooting

### No visible live video feed

If you're working on a Linux machine, `ssh` into it, then restart `viam-server` by running:

```sh {class="command-line" data-prompt="$"}
sudo systemctl restart viam-server
```

If this doesn't work, you can reboot your machine by running:

```sh {class="command-line" data-prompt="$"}
sudo reboot
```

### Images are dim on start up

If you are capturing camera data, it can happen that the camera captures and syncs miscolored or dark images upon start up.

### CSI Camera not working on a Raspberry Pi

If you are using a CSI camera v1.3 or v2.0 on a Raspberry Pi, you need to [enable legacy mode](/installation/prepare/rpi-setup/#enable-communication-protocols).
If you are using a CSI camera v3.0, you need to use the [`viam:camera:csi` module](https://github.com/viamrobotics/csi-camera/) instead.

### High CPU usage

Each camera stream you add uses CPU on the device it is connected to and there is therefore a practical limit to the numbeof camera streams your device can simultaneously support.
You can limit the CPU usage by reducing the image resolution.

### Timeout errors on a Raspberry Pi

If you are getting "timeout" errors from GRPC when adding a `esp32-camera` model on a Raspberry Pi, make sure the esp32-camera port is enabled on the Pi (common if you are using a fresh Pi right out of the box).

To enable the esp32-camera port on a Raspberry Pi, run the following command:

```sh {class="command-line" data-prompt="$"}
sudo raspi-config
```

Then, select: **Interface Options -> Camera -> Enable Camera**.

Restart the Pi to complete the configuration.

## Next steps

Complete a quick mini-project using your esp32-camera with computer vision:

{{< cards >}}
{{< card link="/get-started/detect-people/" >}}
{{< card link="/tutorials/services/basic-color-detection/" >}}
{{< /cards >}}
