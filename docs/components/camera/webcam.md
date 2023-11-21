---
title: "Configure a Webcam"
linkTitle: "webcam"
weight: 33
type: "docs"
description: "Configure a standard camera that streams camera data."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

`webcam` is the general camera model.
If the camera drivers are among those in [this mediadevices repository](https://github.com/pion/mediadevices). the camera will work with the webcam model.

{{< tabs name="Configure a Webcam" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `webcam` model.
Enter a name for your camera and click **Create**.

{{< imgproc src="/components/camera/configure-webcam.png" alt="Configuration of a webcam camera in the Viam app config builder." resize="600x" >}}

Edit and fill in the attributes as applicable.
If you click on the **Video Path** field while your robot is live, a dropdown autopopulates with identified camera paths.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "webcam",
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

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my_cam",
  "model": "webcam",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "video_path": "video0"
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `webcam` cameras:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `video_path` | string | Optional | The ID of or the path to the webcam. If you don't provide a `video_path`, it defaults to the first valid video path it finds. Using the ID of a webcam is more consistent than the path. See [Using `video_path`](#using-video_path). |
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

The `id` listed by `ls /dev/v4l/by-id/` is a more consistent way to refer to the webcam.

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
- MJPEG
- NV12
- NV21
- RGBA
- UYVY
- YUY2
- Z16

If your machine is connected to the Viam app, the available pixel formats supported by your camera automatically appear in the **Format** dropdown menu, which is visible when you click the **Show more** button.

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

If you are using a CSI camera v1.3 or v2.0 on a Raspberry Pi, you need to [enable legacy mode](../../../installation/prepare/rpi-setup/#enable-communication-protocols).
If you are using a CSI camera v3.0, you need to use the [`viam:camera:csi` module](https://github.com/viamrobotics/csi-camera/) instead.

### High CPU usage

Each camera stream you add uses CPU on the device it is connected to and there is therefore a practical limit to the numbeof camera streams your device can simultaneously support.
You can limit the CPU usage by reducing the image resolution.

### Timeout errors on a Raspberry Pi

If you are getting "timeout" errors from GRPC when adding a `webcam` model on a Raspberry Pi, make sure the webcam port is enabled on the Pi (common if you are using a fresh Pi right out of the box).

To enable the webcam port on a Raspberry Pi, run the following command:

```sh {class="command-line" data-prompt="$"}
sudo raspi-config
```

Then, select: **Interface Options -> Camera -> Enable Camera**.

Restart the Pi to complete the configuration.

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
