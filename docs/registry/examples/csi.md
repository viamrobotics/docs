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
aliases:
  - "/extend/modular-resources/examples/csi/"
  - "/modular-resources/examples/csi/"
# SMEs: Sean
---

Many boards, like the Jetson Orin Nano, come with the option to use Camera Serial Interface (CSI) cameras, like [these cameras from E-con Systems](https://www.e-consystems.com/nvidia-jetson-agx-orin-cameras.asp) or [this camera from Seed Technologies](https://www.digikey.com/en/products/detail/seeed-technology-co.,-ltd/114992263/12396924).
These cameras are excellent for utilizing embedded vision systems like Viam's [vision service](/ml/vision/).
Not all CSI cameras are supported by the built-in [webcam camera model](/components/camera/webcam/).
Instead, Viam supports CSI cameras by providing a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} for your CSI camera, `viam:camera:csi`, which you can use to add support for your CSI camera to your robot.

This {{< glossary_tooltip term_id="module" text="module" >}} includes a simple wrapper around `GStreamer` and a control interface for the **Control** tab of the [Viam app](https://app.viam.com) so you can utilize the hardware accelerated GST plugins and use the embedded CSI cameras on your `jetson` boards with Viam.

The `csi-cam` module is available [from the Viam registry](https://app.viam.com/module/viam/csi-cam).
See [Modular resources](/registry/#the-viam-registry) for instructions on using a module from the Viam registry on your robot.

The source code for this module is available on the [`viam-csi` GitHub repository](https://github.com/seanavery/viam-csi).

## Requirements

If you haven't already, [install `viam-server`](/get-started/installation/) on your robot.

The `csi-cam` module is distributed as an AppImage.
AppImages require FUSE version 2 to run.
See [FUSE troubleshooting](/appendix/troubleshooting/#appimages-require-fuse-to-run) for instructions on installing FUSE 2 on your system if it is not already installed.

Currently, the `csi-cam` module supports the Linux platform only.

## Configuration

{{< tabs name="Configure your CSI camera">}}
{{% tab name="Config Builder" %}}

Follow the instructions below to set up the `csi-cam` module on your robot:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Components** subtab and click **Create component** in the lower-left corner.
1. Select **Camera**, then select `csi`.
   You can also search for "csi".
1. Click **Add module**, give your component a name of your choice, then click **Create**.
1. In the resulting `camera` component configuration pane, paste the following configuration into the **Attributes** text window:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "width_px": <int>,
     "height_px": <int>,
     "frame_rate": <int>,
     "debug": <boolean>
   }
   ```

   See the [Attributes](#attributes) section for more information on the other attributes.

1. Click **Save config** at the bottom of the page.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.

```json
{
  "components": [
    {
      "name": "<your-csi-cam-name>",
      "model": "viam:camera:csi",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {
        "width_px": <int>,
        "height_px": <int>,
        "frame_rate": <int>,
        "debug": <boolean>
      },
      "depends_on": []
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_csi-cam",
      "module_id": "viam:csi-cam",
      "version": "0.2.0"
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
  "components": [
    {
      "name": "my-csi-camera",
      "model": "viam:camera:csi",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {
        "width_px": 1920,
        "height_px": 1080,
        "frame_rate": 60,
        "debug": false
      },
      "depends_on": []
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_csi-cam",
      "module_id": "viam:csi-cam",
      "version": "0.2.0"
    }
  ]
}
```

To save your changes, click **Save config** at the bottom of the page.

{{% /tab %}}
{{< /tabs >}}

## Attributes

The following attributes are available for the `viam:camera:csi` model:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `width_px` | int | Optional | Width of the image this camera captures in pixels. <br> Default: `1920` |
| `height_px` | int | Optional | Height of the image this camera captures in pixels. <br> Default: `1080` |
| `frame_rate` | int | Optional | The image capture frame rate this camera should use. <br> Default: `30` |
| `video_path` | string | Optional | The filepath to the input sensor of this camera on your board. If none is given, your robot will attempt to detect the video path automatically. <br> Default: `"0"` </br>  |
| `debug` | boolean | Optional | Whether or not you want debug input from this camera in your robot's logs. <br> Default: `false` |

Check the [**Logs** tab](/build/program/debug/) of your robot in the Viam app to make sure your camera has connected and no errors are being raised.
