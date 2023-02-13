---
title: "Configure a Webcam"
linkTitle: "Webcam"
weight: 33
type: "docs"
description: "Configure a standard USB camera that streams camera data."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `webcam` camera is generally a standard USB camera that streams camera data.

{{% alert title="Tip" color="tip"%}}

Viam recommends using a standard webcam rather than a ribbon cam (typically a bare camera with a ribbon and connector for mating to a Pi) as ribbon cams can be unreliable.

{{% /alert %}}

{{< tabs name="Configure a Webcam" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> tab, navigate to the <b>Create Component</b> menu.
Enter a name for your camera, select the type <code>camera</code>, and select the <code>webcam</code> model.
<br>
<img src="../img/create-webcam.png" alt="Creation of webcam camera in the Viam App config builder." />
<br>
Fill in the attributes for your webcam view:
<br>
<img src="../img/configure-webcam.png" alt="Configuration of a webcam camera in the Viam App config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "webcam",
    "attributes": {
        "intrinsic_parameters": {
            "width_px": <integer>,
            "height_px": <integer>,
            "fx": <number>,
            "fy": <number>,
            "ppx": <number>,
            "ppy": <number>
        },
        "distortion_parameters": {
            "rk1": <number>,
            "rk2": <number>,
            "rk3": <number>,
            "tp1": <number>,
            "tp2": <number>
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
{{< /tabs >}}

The following attributes are available for webcams:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `intrinsic_parameters` | *Optional* | The intrinsic parameters of the camera used to do 2D <-> 3D projections: <ul> <li> <code>width_px</code>: The expected width of the aligned image in pixels. </li> <li> <code>height_px</code>: The expected height of the aligned image in pixels. </li> <li> <code>fx</code>: The image center x point. </li> <li> <code>fy</code>: The image center y point. </li> <li> <code>ppx</code>: The image focal x. </li> <li> <code>ppy</code>: The image focal y. </li> </ul> |
| `distortion_parameters` | *Optional* | Modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens: <ul> <li> <code>rk1</code>: The radial distortion x. </li> <li> <code>rk2</code>: The radial distortion y. </li> <li> <code>rk3</code>: The radial distortion z. </li> <li> <code>tp1</code>: The tangential distortion x. </li> <li> <code>tp2</code>: The tangential distortion y. </li> </ul> |
| `debug` | *Optional* | Enables the debug outputs from the camera if `true`. Defaults to `false`. |
| `format` | *Optional* | The camera image format, used with video_path to find camera. |
| `video_path` | *Optional* | The path to the webcam. Often `video0`. To find potential video paths run `v4l2-ctl --list-devices` in your terminal. |
| `width_px` | *Optional* | The camera image width, used with video_path to find camera with this resolution. |
| `height_px` | *Optional* | The camera image height, used with video_path to find camera with this resolution. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Troubleshooting

### `video0` does not work

### No visible live video feed

If you're working on a linux machine, `ssh` into it, then restart `viam-server` by running:

```bash
sudo systemctl restart viam-server
```

If this doesn't work, you can reboot your machine by running:

```bash
sudo reboot
```

If `video0` does not work for you, you can find another potential `video_path` by typing the following in your terminal:

```bash
v4l2-ctl --list-devices
```

The output for a webcam looks like this, in which case `video1` might be the correct path to use for `video_path`:

```bash
C270 HD WEBCAM (usb-0000:01:00.0-1.2):
 /dev/video0
 /dev/video1
 /dev/media4
```

### Timeout errors on a Raspberry Pi

If you are getting "timeout" errors from GRPC when adding a `webcam` model on a Raspberry Pi, make sure the webcam port is enabled on the Pi (common if you are using a fresh Pi right out of the box):

```bash
sudo raspi-config
Interface Options -> Camera -> Enable Camera
Restart the Pi
```

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
