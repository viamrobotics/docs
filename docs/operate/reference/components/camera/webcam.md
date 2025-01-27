---
title: "Configure a Webcam"
linkTitle: "webcam"
weight: 33
type: "docs"
description: "Configure a standard camera that streams camera data."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/webcam/"
component_description: "A standard USB camera or other webcam that streams camera data."
usage: 999999
toc_hide: true
# SMEs: Bijan, vision team
---

`webcam` is the general camera model.
If the camera drivers are among those in [this mediadevices repository](https://github.com/pion/mediadevices), the camera will work with the webcam model.

First, connect your camera to your machine's computer (unless it is built-in like a webcam on a laptop) and power both on.
Then, configure your camera:

{{< tabs name="Configure a Webcam" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `webcam` model.
Enter a name or use the suggested name for your camera and click **Create**.

{{< imgproc src="/components/camera/configure-webcam.png" alt="Configuration of a webcam camera in the Viam app config builder." resize="1200x" style="width=600x" >}}

Edit and fill in the attributes as applicable.
If you click on **Show more**, then the **video_path** field while your machine is live, a dropdown autopopulates with identified camera paths.

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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `video_path` | string | Optional | The ID of or the path to the webcam. If you don't provide a `video_path`, it defaults to the first valid video path it finds. Using the ID of a webcam is more consistent than the path. See [Using `video_path`](#using-video_path). |
| `format` | string | Optional | The camera image format, used with `video_path` to find the camera. See [Using `format`](#using-format). |
| `width_px` | int | Optional | The camera image width in pixels, used with `video_path` to find a camera with this resolution. Negative values are silently ignored and result in the default being used. <br> Default: Closest possible value to `480` |
| `height_px` | int | Optional | The camera image height in pixels, used with `video_path` to find a camera with this resolution. Negative values are silently ignored and result in the default being used. <br> Default: Closest possible value to `640` |
| `frame_rate` | float | Optional | The camera capture frequency as frames per second, used with `video_path` to find a camera with this throughput. <br> Default: Closest possible value to `30.0` |
| `intrinsic_parameters` | object | Optional | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> `width_px`: The expected width of the aligned image in pixels. </li> <li> `height_px`: The expected height of the aligned image in pixels. </li> <li> `fx`: The image center x point. </li> <li> `fy`: The image center y point. </li> <li> `ppx`: The image focal x. </li> <li> `ppy`: The image focal y. </li> </ul> |
| `distortion_parameters` | object | Optional | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> `rk1`: The radial distortion x. </li> <li> `rk2`: The radial distortion y. </li> <li> `rk3`: The radial distortion z. </li> <li> `tp1`: The tangential distortion x. </li> <li> `tp2`: The tangential distortion y. </li> </ul> |

## Using `video_path`

To list available `video_path`s use the following command:

{{< tabs name="Find video devices" >}}
{{% tab name="Linux" %}}

```sh {class="command-line" data-prompt="$"}
ls /dev/v4l/by-id/
```

To find the `path`s of all connected video devices, run the following command:

```sh {class="command-line" data-prompt="$"}
v4l2-ctl --list-devices
```

The `id` listed by `ls /dev/v4l/by-id/` is a more consistent way to refer to the webcam.

{{% /tab %}}
{{% tab name="Mac" %}}

```sh {class="command-line" data-prompt="$"}
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

{{< readfile "/static/include/components/troubleshoot/camera.md" >}}

{{% expand "Cannot open webcam or found no webcams" %}}
When working with a [camera](/operate/reference/components/camera/) component on the Linux platform, your Linux OS must be able to access the camera properly, and the camera must be configured to use a pixel format that Viam supports.

On your Linux system, verify each of the following:

- Ensure that your Linux OS is able to access your camera:

  1.  Run the following command to list compatible camera devices on your system:

      ```sh {class="command-line" data-prompt="$"}
      v4l2-ctl --list-devices
      ```

      In the list of camera devices returned, find the entry for your camera.
      For example, the webcam on a rover may appear as follows:

      ```sh {class="command-line" data-prompt="$"}
      GENERAL WEBCAM: GENERAL WEBCAM (usb-0000:01:00.0-1.4):
              /dev/video0
              /dev/video1
              /dev/media4
      ```

      The video path for your camera device is the first path listed under that camera, in this case `/dev/video0`.

  1.  Then, [stop `viam-server`](/operate/reference/viam-server/manage-viam-server/#run-viam-server), and verify that your Linux OS is able to access that video device properly:

      ```sh {class="command-line" data-prompt="$"}
      v4l2-ctl --stream-count 1 --device /dev/video0
      ```

      Replace `/dev/video0` in the above command with the video path you determined for your video device above, if different.

      The command returns successfully (with no output) if Linux is able to successfully communicate with the camera, or errors with `Cannot open device` if there was a problem communicating.
      If this command errors, you should consult the documentation for your camera and Linux distribution to troubleshoot.
      If you receive the error `Device or resource busy` instead, be sure you have [stopped `viam-server`](/operate/reference/viam-server/manage-viam-server/#run-viam-server) first, then re-run the command above.

- Ensure that your camera uses a supported pixel format:

  1.  First, determine your video path, like `/dev/video0`, following the instructions above.
  1.  Then, run the following command:

      ```sh {class="command-line" data-prompt="$"}
      v4l2-ctl --list-formats-ext --device /dev/video0
      ```

      Replace `/dev/video0` in the above command with the video path you determined for your video device above, if different.

      The command will return a list of pixel formats your camera supports, such as `MJPG` (also notated as `MJPEG`) or `YUYV` (also notated as `YUY2`).
      In order to use a camera device with Viam, it must support at least one of the [pixel formats supported by Viam](/operate/reference/components/camera/webcam/#using-format).
      If your camera does not support any of these formats, it cannot be used with Viam.

If you are still having issues with your camera component on the Linux platform, and would like to [file an issue](https://github.com/viamrobotics/rdk), include your machine's camera debug file contained in the <file>/root/.viam/debug/components/camera</file> directory.
If you are running `viam-server` as a different user, find the <file>.viam/debug/components/camera</file> directory in that user's home directory instead.
This file contains basic diagnostic and configuration information about your camera that helps to quickly troubleshoot issues.
{{% /expand%}}

{{% expand "No visible live video feed" %}}
If you're working on a Linux machine, `ssh` into it, then restart `viam-server` by running:

```sh {class="command-line" data-prompt="$"}
sudo systemctl restart viam-server
```

If this doesn't work, you can reboot your machine by running:

```sh {class="command-line" data-prompt="$"}
sudo reboot
```

{{% /expand%}}

{{% expand "Images are dim on start up" %}}
If you are capturing camera data, it can happen that the camera captures and syncs miscolored or dark images upon start up.
{{% /expand%}}

{{% expand "CSI Camera not working on a Raspberry Pi" %}}
If you are using a CSI camera v1.3 or v2.0 on a Raspberry Pi, you need to [enable legacy mode](/operate/reference/prepare/rpi-setup/#enable-communication-protocols).
If you are using a CSI camera v3.0, you need to use the [`viam:camera:csi` module](https://github.com/viamrobotics/csi-camera/) instead.
IMX500 AI cameras are not officially supported.
{{% /expand%}}

{{% expand "High CPU usage" %}}
Each camera stream you add uses CPU on the device it is connected to and there is therefore a practical limit to the numbeof camera streams your device can simultaneously support.
You can limit the CPU usage by reducing the image resolution.
{{% /expand%}}

{{% expand "Timeout errors on a Raspberry Pi" %}}

If you are getting "timeout" errors from GRPC when adding a `webcam` model on a Raspberry Pi, make sure the webcam port is enabled on the Pi (common if you are using a fresh Pi right out of the box).

To enable the webcam port on a Raspberry Pi, run the following command:

```sh {class="command-line" data-prompt="$"}
sudo raspi-config
```

Then, select: **Interface Options -> Camera -> Enable Camera**.

Restart the Pi to complete the configuration.

{{% /expand%}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/camera/" customTitle="Camera API" noimage="true" %}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{< /cards >}}
