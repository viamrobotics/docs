---
title: "Add a CSI Camera as a Modular Resource"
linkTitle: "CSI Camera"
weight: 40
type: "docs"
description: "How to add a CSI Camera as a modular resource of your robot."
tags: ["board", "csi", "jetson", "serial", "module", "modular resources", "Python", "python SDK", "nvidia", "jetson orin", "jetson orin nano", "nano", "camera"]
# SMEs: Sean
---


Viam provides a modular resource [extending](/extend/modular-resources/) the [camera API](/components/camera/#api) as a new `viam:camera:csi` model of [camera](/components/camera/).

This module includes a simple wrapper around `GStreamer` and a control interface for the **control** tab of the [Viam app](https://app.viam.com) so you can utilize the hardware accelerated GST plugins and use the embedded CSI cameras on your `jetson` boards with Viam.

The module is open-sourced and available on [GitHub](https://github.com/seanavery/viam-csi).

[Install requirements](#requirements) and [configure](#configuration) the module to add an `viam:camera:csi` [camera](/components/camera/) {{< glossary_tooltip term_id="resource" text="resource" >}} to your robot.

## Requirements

On your robot's computer, download [the `viam:camera:csi` appimage](https://github.com/viamrobotics/odrive) and make it executable:

``` {class="command-line" data-prompt="$"}
sudo wget https://github.com/seanavery/viam-csi/releases/download/v0.0.2/viam-csi-0.0.2-aarch64.AppImage -O /usr/local/bin/viam-csi
sudo chmod 755 /usr/local/bin/viam-csi
```

## Configuration

### Module

{{< tabs name="Add the csi module">}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.
Copy and paste the following raw JSON to add a `csi` [camera](/components/camera) component with the name `my_test_csi_cam`:

```json {class="line-numbers linkable-line-numbers"}
{
    "modules": [
      {
        "executable_path": "/usr/bin/csi-mr",
        "name": "csi_cam_module"
      }
    ],
    "components": [
      {
        "model": "viam:camera:csi",
        "attributes": {
          "width_px": 1920,
          "height_px": 1080,
          "frame_rate": 30,
          "debug": true
        },
        "depends_on": [],
        "name": "my_test_csi_cam",
        "namespace": "rdk",
        "type": "camera"
      }
    ]
}
```

Save the config.
Edit and fill in the attributes as applicable.

Check the [**Logs** tab](/program/debug/) of your robot in the Viam app to make sure your camera has connected and no errors are being raised.

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for the `viam:camera:csi` model:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `width_px` | int | Optional | Width of the image this camera captures in pixels. <br> Default: `1920` |
| `height_px` | int | Optional | Height of the image this camera captures in pixels. <br> Default: `1080` |
| `frame_rate` | int | Optional | The image capture frame rate this camera should use. <br> Default: `30` |
| `video_path` | string | Optional | The filepath to the input sensor of this camera on your board. If none is given, your robot will attempt to detect the video path automatically. <br> Default: `"0"` |
| `debug` | boolean | Optional | Whether or not you want debug input from this camera in your robot's logs. <br> Example: `true` |
