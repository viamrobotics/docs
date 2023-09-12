---
title: "Add an RPlidar as a Modular Resource"
linkTitle: "RPlidar"
weight: 40
type: "docs"
description: "Configure a RPlidar camera as a modular resource of your robot."
image: "/program/modular-resources/rplidar-on-robot.png"
imageAlt: "An R-P-lidar mounted to a Viam rover."
images: ["/program/modular-resources/rplidar-on-robot.png"]
tags: ["slam", "services", "modular resources", "lidar", "rplidar"]
aliases:
  - "/program/extend/modular-resources/add-rplidar-module/"
  - "/program/extend/modular-resources/examples/add-rplidar-module/"
  - "/extend/modular-resources/examples/add-rplidar-module/"
# SMEs: Kat, Jeremy
---

## Requirements

Install the `rplidar-module` binary on your machine and make it executable by running the following commands according to your machine's architecture:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```{class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/rplidar-module https://storage.googleapis.com/packages.viam.com/apps/rplidar/rplidar-module-stable-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/rplidar-module
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

```{class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/rplidar-module https://storage.googleapis.com/packages.viam.com/apps/rplidar/rplidar-module-stable-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/rplidar-module
```

{{% /tab %}}
{{% tab name="macOS" %}}

```{class="command-line" data-prompt="$"}
brew tap viamrobotics/brews && brew install rplidar-module
```

{{% /tab %}}
{{< /tabs >}}

## Configuration

Physically connect the RPlidar to your robot.

Be sure to position the RPlidar so that it faces forward in the direction your robot travels.
For example, if you are using the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1) model, mount it to your robot so that the pointed end of the RPlidar mount housing points in the direction of the front of the robot.

Then, go to your robot's page on the [Viam app](https://app.viam.com/).

{{< tabs name="Add the RPlidar component">}}
{{% tab name="JSON Template" %}}

Navigate to the **Config** tab.
Select the **Raw JSON** mode, then copy/paste the following `"components"` and `"modules"` JSON:

  {{< tabs name="Add the RPlidar component - configs" >}}
  {{% tab name="Linux" %}}

  ```json
  {
    "modules": [
      {
        "executable_path": "/usr/local/bin/rplidar-module",
        "name": "rplidar-module"
      }
    ],
    "components": [
      {
        "namespace": "rdk",
        "type": "camera",
        "depends_on": [],
        "model": "viam:lidar:rplidar",
        "name": "rplidar"
      }
    ]
  }
  ```

  {{% /tab %}}
  {{% tab name="macOS x86_64" %}}

  ```json
  {
    "modules": [
      {
        "executable_path": "/usr/local/bin/rplidar-module",
        "name": "rplidar-module"
      }
    ],
    "components": [
      {
        "namespace": "rdk",
        "type": "camera",
        "depends_on": [],
        "model": "viam:lidar:rplidar",
        "attributes": {
          "device_path": "/dev/tty.SLAB_USBtoUART"
        },
        "name": "rplidar"
      }
    ]
  }
  ```

  {{% /tab %}}
  {{% tab name="macOS ARM64 (M1 & M2)" %}}

If you are on an M1 or M2 Macbook, determine the device path by running the following command:

```sh {class="command-line" data-prompt="$"}
ls /dev/ | grep tty.usbserial
```

For example, you may see `tty.usbserial-130`, in which case your device path would be `/dev/tty.usbserial-130`.
Use the device path in your configuration:

  ```json
  {
    "modules": [
      {
        "executable_path": "/opt/homebrew/bin/rplidar-module",
        "name": "rplidar-module"
      }
    ],
    "components": [
      {
        "namespace": "rdk",
        "type": "camera",
        "depends_on": [],
        "model": "viam:lidar:rplidar",
        "attributes": {
          "device_path": "/dev/tty.usbserial-XXX"
        },
        "name": "rplidar"
      }
    ]
  }
  ```

  {{% /tab %}}
  {{< /tabs >}}

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
