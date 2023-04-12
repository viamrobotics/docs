---
title: "Configure a Webcam"
linkTitle: "Webcam"
weight: 33
type: "docs"
description: "Configure a standard camera that streams camera data."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

`webcam` is the general camera model.
If the camera drivers are among those in [this mediadevices repository](https://github.com/pion/mediadevices). the camera will work with the webcam model.

{{< tabs name="Configure a Webcam" >}}
{{% tab name="Config Builder" %}}

On the **COMPONENTS** subtab, navigate to the **Create Component** menu.
Enter a name for your camera, select the type `camera`, and select the `webcam` model.

<img src="../img/create-webcam.png" alt="Creation of webcam camera in the Viam app config builder." style="max-width:500px" />

Fill in the attributes for your webcam.
If you click on the **Video Path** field while your robot is live, a drop down autopopulates with identified camera paths.

<img src="../img/configure-webcam.png" alt="Configuration of a webcam camera in the Viam app config builder." />

Use the following configuration and fill in the attributes for your webcam:

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "webcam",
    "attributes": {
        "intrinsic_parameters": {
            "width_px": <integer>,
            "height_px": <integer>,
            "fx": <float64>,
            "fy": <float64>,
            "ppx": <float64>,
            "ppy": <float64>
        },
        "distortion_parameters": {
            "rk1": <float64>,
            "rk2": <float64>,
            "rk3": <float64>,
            "tp1": <float64>,
            "tp2": <float64>
        },
        "debug": <boolean>,
        "format": <string>,
        "video_path": <string>,
        "width_px": <integer>,
        "height_px": <integer>
    }
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "my_cam",
    "type": "camera",
    "model" : "webcam",
    "attributes": {
        "video_path": "video0"
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for webcams:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `intrinsic_parameters` | *Optional* | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> `width_px`: The expected width of the aligned image in pixels. </li> <li> `height_px`: The expected height of the aligned image in pixels. </li> <li> `fx`: The image center x point. </li> <li> `fy`: The image center y point. </li> <li> `ppx`: The image focal x. </li> <li> `ppy`: The image focal y. </li> </ul> |
| `distortion_parameters` | *Optional* | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> `rk1`: The radial distortion x. </li> <li> `rk2`: The radial distortion y. </li> <li> `rk3`: The radial distortion z. </li> <li> `tp1`: The tangential distortion x. </li> <li> `tp2`: The tangential distortion y. </li> </ul> |
| `debug` | *Optional* | Enables the debug outputs from the camera if `true`. Defaults to `false`. |
| `format` | *Optional* | The camera image format, used with video_path to find camera. |
| `video_path` | *Optional* | The id of or the path to the webcam. Often `video0`. If you don't provide a `video_path`, it defaults to the first valid video path it finds. Using the id of a webcam is more consistent than the path. |
| `width_px` | *Optional* | The camera image width in pixels, used with video_path to find camera with this resolution. Defaults to the closest possible value to closest to 480. |
| `height_px` | *Optional* | The camera image height in pixels, used with video_path to find camera with this resolution. Defaults to the closest possible value to closest to 640. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Troubleshooting

## Find the `video_path`

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

{{% /tab %}}
{{% tab name="Mac" %}}

```sh
system_profiler SPCameraDataType
```

The Unique ID displayed for each camera is the `video_path`.

{{% /tab %}}
{{< /tabs >}}

### No visible live video feed

If you're working on a Linux machine, `ssh` into it, then restart `viam-server` by running:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo systemctl restart viam-server
```

If this doesn't work, you can reboot your machine by running:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo reboot
```

### CSI Camera not working on a Raspberry Pi

If you are using a CSI camera on a Raspberry Pi, you need to [enable legacy mode](../../../installation/prepare/rpi-setup/#enable-communication-protocols).

### Timeout errors on a Raspberry Pi

If you are getting "timeout" errors from GRPC when adding a `webcam` model on a Raspberry Pi, make sure the webcam port is enabled on the Pi (common if you are using a fresh Pi right out of the box):

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo raspi-config
Interface Options -> Camera -> Enable Camera
Restart the Pi
```

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
