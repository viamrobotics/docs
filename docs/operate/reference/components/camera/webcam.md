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

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `camera` type, then select the `webcam` model.
Enter a name or use the suggested name for your camera and click **Create**.

{{< imgproc src="/components/camera/configure-webcam.png" alt="Configuration of a webcam camera." resize="1200x" style="width=600x" class="shadow"  >}}

Edit and fill in the attributes as applicable.
Leave the **video_path** blank and the camera will use the default video path for your machine.
If this doesn't work when you test your camera later, you can try [configuring a video path](#using-video_path).

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "webcam",
  "api": "rdk:component:camera",
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
  "api": "rdk:component:camera",
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

### Find a video path using a discovery service

The [`rand:find-webcams:webcam-discovery`](https://app.viam.com/module/rand/find-webcams) service helps you identify path options.
To add and use the service:

1. Navigate to the **CONFIGURE** tab of your machine's page.
1. Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
1. Search for `find-webcams` and select the `discovery / find-webcams:webcam-discovery` service.
1. Click **Add module**.
1. Enter a name or use the suggested name for your camera and click **Create**.
1. Save your configuration, and wait a moment for the service to start.
1. Click **Test** to see the available `video_path`s.

   {{<imgproc src="/components/camera/webcam-discovery-test.png" alt="The test panel for the find-webcams service." resize="1100x" style="max-width:600px" class="shadow imgzoom" >}}

1. Click the **Copy attributes** button for the camera you want to use.
1. Click the **{}** icon in the upper right corner of the camera component configuration.

   {{<imgproc src="/components/camera/advanced-config.png" resize="x1100" declaredimensions=true alt="The switch to advanced button." style="width:200px" class="shadow" >}}

1. Paste the copied attributes.
1. Click **Save**.
1. You can now delete the discovery service and the module that provides it from your machine.

### Find a video path using the command line

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

If you are using macOS version 15.x.x Sequoia or later, you need to give `viam-server` permissions to access webcams.
When you run `viam-server` for the first time, a pop-up message will ask for camera access.
Click **Allow**.
To confirm settings, you can go to **System Settings** > **Privacy & Security** > **Camera** and check that the toggle next to `viam-server` is set to enable access.

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

If your machine is connected to Viam, the available pixel formats supported by your camera automatically appear in the **Format** dropdown menu, which is visible when you click the **Show more** button.

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

Restart `viam-server`:

1. Navigate to your machine's page.
1. Select the part status dropdown to the right of your machine's name on the top of the page.
   {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="machine cloud credentials button on the machine part info dropdown" class="shadow" >}}
1. If you installed `viam-server` with `viam-agent` you will see a **Restart** button. Click it.
   Both `viam-server` and `viam-agent` will restart.

   If you do not see the **Restart** button, click the **...** menu on the right side of the machine part's card, and select **Restart part**.
   If restarting the machine part does not resolve the issue, ssh into the machine and [stop and restart viam-server manually](/operate/reference/viam-server/manage-viam-server/#run-viam-server).

If this doesn't work, you can reboot your machine by running the following command on the machine:

```sh {class="command-line" data-prompt="$"}
sudo reboot
```

{{% /expand%}}

{{% expand "Images are dim on start up" %}}
If you are capturing camera data, it can happen that the camera captures and syncs discolored or dark images upon start up.
{{% /expand%}}

{{% expand "CSI Camera not working on a Raspberry Pi" %}}

If you are using a CSI camera v1.3 or v2.0, or v3.0 with a Raspberry Pi, use the `viam:camera:csi-pi` model provided by the [Viam CSI camera module](https://github.com/viamrobotics/csi-camera/) instead.
For CSI cameras used with Jetsons, use the `viam:camera:csi` model provided by the same module.

For Raspberry Pi AI cameras like the IMX500 AI camera, use a module such as [this `viam-pi-ai-camera` vision service](https://github.com/HipsterBrown/viam-pi-ai-camera).
For more information about the vision service, see [run inference](https://docs.viam.com/data-ai/ai/run-inference/).
{{% /expand%}}

{{% expand "High CPU usage" %}}
Camera streams use a significant amount of CPU resources.
The more CPU resources a device has, the more camera streams you can run simultaneously.
If your device doesn't have enough CPU resources to support your use case, try lowering the image resolution to decrease the CPU load of the camera streams.
{{% /expand%}}

{{% expand "macOS camera permissions issues" %}}
On macOS, if you're having trouble accessing your webcam, you may need to grant camera permissions for the application that you use to run `viam-server`.

**Resetting camera permissions:**

If `viam-server` is not prompting for camera permissions or you need to re-grant permissions, you can reset the camera permissions for all applications using the following command:

```sh {class="command-line" data-prompt="$"}
tccutil reset Camera
```

If you know the macOS bundle ID of the application that you use to run `viam-server`, you can pass the bundle ID to limit the camera permissions reset to only that application.
For instance, you can reset camera permissions for the built-in Terminal app with `tccutil reset Camera com.apple.Terminal`.
If the command was successful, you should see output similar to the following:

```sh {class="command-line" data-prompt="$"}
Successfully reset Camera approval status for com.apple.Terminal
```

After running this command, restart `viam-server` and it should prompt for camera permissions again.

**Checking camera permissions:**

To verify camera permissions, go to **System Settings** > **Privacy & Security** > **Camera**.
Find the application `viam-server` is running in (such as Terminal or VS Code).
Ensure that your terminal application has camera access enabled.
{{% /expand%}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/camera/" customTitle="Camera API" noimage="true" %}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{< /cards >}}
