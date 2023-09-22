---
title: "Add a CSI Camera as a Modular Resource"
linkTitle: "CSI Camera"
weight: 40
type: "docs"
description: "Use the viam:camera:csi model to add a CSI Camera to your robot."
tags:
  [
    "board",
    "csi",
    "jetson",
    "serial",
    "module",
    "modular resources",
    "Python",
    "python SDK",
    "nvidia",
    "jetson orin",
    "jetson orin nano",
    "nano",
    "camera",
  ]
# SMEs: Sean
---

Many boards, like the Jetson Orin Nano, come with the option to use Camera Serial Interface (CSI) cameras, like [these cameras from E-con Systems](https://www.e-consystems.com/nvidia-jetson-agx-orin-cameras.asp) or [this camera from Seed Technologies](https://www.digikey.com/en/products/detail/seeed-technology-co.,-ltd/114992263/12396924).
These cameras are excellent for utilizing embedded vision systems like Viam's [vision service](/services/vision/).
Not all CSI cameras are supported by the [webcam camera model](/components/camera/webcam/).
Instead, Viam supports CSI cameras by providing a [modular resource](/extend/modular-resources/) for your CSI camera: `viam:camera:csi`.

This module includes a simple wrapper around `GStreamer` and a control interface for the **control** tab of the [Viam app](https://app.viam.com) so you can utilize the hardware accelerated GST plugins and use the embedded CSI cameras on your `jetson` boards with Viam.

The module is open-sourced and available on [GitHub](https://github.com/seanavery/viam-csi).

To use the CSI camera module, follow the [installation](#installation) and [configuration](#configuration) steps.

## Installation

On your robot's computer, download [the `viam:camera:csi` appimage](https://github.com/seanavery/viam-csi) and make it executable:

```{class="command-line" data-prompt="$"}
sudo wget https://github.com/seanavery/viam-csi/releases/download/v0.0.2/viam-csi-0.0.2-aarch64.AppImage -O /usr/local/bin/viam-csi
sudo chmod 755 /usr/local/bin/viam-csi
```

## Configuration

{{< tabs name="Connect your CSI Module and Modular Resource">}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).

Click on the **Modules** subtab and navigate to the **Local** section.
Enter a name, for example `my_csi_cam_module_name`, then enter the executable path.
If you used the above install command, the executable path should be: `/usr/local/bin/viam-csi`.
Then click **Add module**.

Click on the **Components** subtab and click **Create component**.
Select the `local modular resource` type.
Then select `camera` as the type, enter the triplet `viam:camera:csi`, and give your resource a name, for example `my_test_csi_cam`.
Click **Create**.

On the new component panel, copy and paste the following JSON object into the attributes field:

```json
{
    "width_px": <int>,
    "height_px": <int>,
    "frame_rate": <int>,
    "debug": "<boolean>"
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.

Copy and paste the JSON object for the module into the modules array to add Viam's `csi-mr` module:

```json
{
  "executable_path": "</usr/local/bin/viam-csi>",
  "name": "<your-csi-cam-module-name>",
  "type": "local"
}
```

Next, add the following JSON object to your components array to configure a `csi` [camera](/components/camera/) component with the name `my_test_csi_cam`:

```json {class="line-numbers linkable-line-numbers"}
{
    "model": "viam:camera:csi",
    "attributes": {
      "width_px": <int>,
      "height_px": <int>,
      "frame_rate": <int>,
      "debug": "<boolean>"
    },
    "depends_on": [],
    "name": "<your-csi-cam-name>",
    "namespace": "rdk",
    "type": "camera"
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "executable_path": "/usr/bin/csi-mr",
      "name": "csi_cam_module",
      "type": "local"
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

{{% /tab %}}
{{< /tabs >}}

For more information, see [installing local modules](/extend/modular-resources/configure/#local-modules).

Edit and fill in the attributes to configure your component.

The following attributes are available for the `viam:camera:csi` model:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `width_px` | int | Optional | Width of the image this camera captures in pixels. <br> Default: `1920` |
| `height_px` | int | Optional | Height of the image this camera captures in pixels. <br> Default: `1080` |
| `frame_rate` | int | Optional | The image capture frame rate this camera should use. <br> Default: `30` |
| `video_path` | string | Optional | The filepath to the input sensor of this camera on your board. If none is given, your robot will attempt to detect the video path automatically. <br> Default: `"0"` </br>  |
| `debug` | boolean | Optional | Whether or not you want debug input from this camera in your robot's logs. <br> Default: `false` |

Then, save the config.

Check the [**Logs** tab](/program/debug/) of your robot in the Viam app to make sure your camera has connected and no errors are being raised.

For more information, see [installing local modules](/extend/modular-resources/configure/#local-modules).
