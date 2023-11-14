---
title: "Add an RPlidar as a Modular Resource"
linkTitle: "RPlidar"
weight: 40
type: "docs"
description: "Configure an RPlidar camera as a modular resource of your robot."
image: "/program/modular-resources/rplidar-on-robot.png"
imageAlt: "An R-P-lidar mounted to a Viam rover."
images: ["/program/modular-resources/rplidar-on-robot.png"]
tags: ["slam", "services", "modular resources", "lidar", "rplidar"]
no_list: true
aliases:
  - "/program/extend/modular-resources/add-rplidar-module/"
  - "/program/extend/modular-resources/examples/add-rplidar-module/"
  - "/extend/modular-resources/examples/add-rplidar-module/"
  - "/extend/modular-resources/examples/rplidar/"
  - "/modular-resources/examples/rplidar/"
# SMEs: Kat, Jeremy
---

Viam provides an `rplidar` {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} which adds support for SLAMTECH's RPlidar family of lidar scanners, extending the Viam [camera API](/components/camera/#api).
Currently, the `rplidar` {{< glossary_tooltip term_id="module" text="module" >}} has been tested with the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1), [RPlidar A3](https://www.slamtec.com/en/Lidar/A3), and [RPlidar S1](http://bucket.download.slamtec.com/f19ea8efcc2bb55dbfd5839f1d307e34aa4a6ca0/LD601_SLAMTEC_rplidar_datasheet_S1_v1.4_en.pdf).

The `rplidar` module is available [from the Viam registry](https://app.viam.com/module/viam/rplidar).
See [Modular resources](/registry/#the-viam-registry) for instructions on using a module from the Viam registry on your robot.

The source code for this module is available on the [`rplidar` GitHub repository](https://github.com/viamrobotics/rplidar).

## Requirements

If you haven't already, [install `viam-server`](/installation/) on your robot.

The `rplidar` module is distributed as an AppImage.
AppImages require FUSE version 2 to run.
See [FUSE troubleshooting](/appendix/troubleshooting/#appimages-require-fuse-to-run) for instructions on installing FUSE 2 on your system if it is not already installed.

Currently, the `rplidar` module supports the Linux platform only.

Your robot must have an RPlidar installed to be able to use the `rplidar` module, such as the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) or [RPlidar A3](https://www.slamtec.com/en/Lidar/A3).

Physically connect the RPlidar to your robot.
Be sure to position the RPlidar so that it faces forward in the direction your robot travels.
For example, if you are using the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) model, mount it to your robot so that the pointed end of the RPlidar mount housing points in the direction of the front of the robot.

## Configuration

{{< tabs name="Add the RPlidar component">}}
{{% tab name="Config Builder" %}}

Follow the instructions below to set up the `rplidar` module on your robot:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Components** subtab and click **Create component** in the lower-left corner.
1. Select **Camera**, then select `rplidar`.
   You can also search for "rplidar".
1. Click **Add module**, give your component a name of your choice, then click **Create**.
1. Click **Save config** at the bottom of the page.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.

```json
{
  "components": [
    {
      "name": "<your-rplidar-name>",
      "model": "viam:lidar:rplidar",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_rplidar",
      "module_id": "viam:rplidar",
      "version": "0.1.14"
    }
  ]
}
```

To save your changes, click **Save config** at the bottom of the page.

{{% /tab %}}
{{% tab name="JSON Example" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.

```json
{
  "components": [
    {
      "name": "my-rplidar",
      "model": "viam:lidar:rplidar",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_rplidar",
      "module_id": "viam:rplidar",
      "version": "0.1.14"
    }
  ]
}
```

To save your changes, click **Save config** at the bottom of the page.

{{% /tab %}}
{{< /tabs >}}

Check the **Logs** tab of your robot in the Viam app to make sure your RPlidar has connected and no errors are being raised.

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
{{% card link="/services/slam/cartographer" %}}
{{% card link="/services/slam" %}}
{{< /cards >}}
