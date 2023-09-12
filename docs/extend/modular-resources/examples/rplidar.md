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
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).

  {{< tabs name="Add the RPlidar component - configs" >}}
  {{% tab name="Linux" %}}

Click on the **Modules** subtab and navigate to the **Local** section.
Enter a name, for example `my_rplidar_module_name`, and the executable path `/usr/bin/csi-mr`.
Then click **Add module**.

Click on the **Components** subtab and click **Create component**.
Select the `local modular resources` type.
Then select the `camera` as the type, enter the triplet `viam:lidar:rplidar` and give your resource a name, for example `rplidar`.
Click **Create**.

  {{% /tab %}}
  {{% tab name="macOS x86_64" %}}

Click on the **Modules** subtab and navigate to the **Local** section.
Enter a name, for example `my_rplidar_module_name`, and the executable path `/usr/bin/csi-mr`.
Then click **Add module**.

Click on the **Components** subtab and click **Create component**.
Select the `local modular resources` type.
Then select the `camera` as the type, enter the triplet `viam:lidar:rplidar` and give your resource a name, for example `rplidar`.
Click **Create**.

On the new component panel, copy and paste the following JSON object into the attributes field:

```json
{
    "device_path": "/dev/tty.SLAB_USBtoUART"
}
```

  {{% /tab %}}
  {{% tab name="macOS ARM64 (M1 & M2)" %}}

Click on the **Modules** subtab and navigate to the **Local** section.
Enter a name, for example `my_rplidar_module_name`, and the executable path `/opt/homebrew/bin/rplidar-module`.
Then click **Add module**.

Click on the **Components** subtab and click **Create component**.
Select the `local modular resources` type.
Then select the `camera` as the type, enter the triplet `viam:lidar:rplidar` and give your resource a name, for example `rplidar`.
Click **Create**.

On the new component panel, copy and paste the following JSON object into the attributes field:

```json
{
    "device_path": "/dev/tty.usbserial-XXX"
}
```

If you are on an M1 or M2 Macbook, determine the device path by running the following command:

```sh {class="command-line" data-prompt="$"}
ls /dev/ | grep tty.usbserial
```

For example, you may see `tty.usbserial-130`, in which case your device path would be `/dev/tty.usbserial-130`.
Replace the `XXX` at the end of the `device_path` value in the attributes configuration with the number at the end of your device path.

  {{% /tab %}}
  {{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

Navigate to the **Config** tab.

Select the **Raw JSON** mode.

  {{< tabs name="Add the RPlidar component - configs" >}}
  {{% tab name="Linux" %}}

  Copy and paste the JSON object for the module into the modules array to add the module:

  ```json
  {
      "executable_path": "/usr/local/bin/rplidar-module",
      "name": "my_rplidar_module_name"
  }
  ```

  Next, add the following JSON object to your components array to configure a `rplidar` [camera](/components/camera/) component with the name `rplidar`:

  ```json
  {
      "namespace": "rdk",
      "type": "camera",
      "depends_on": [],
      "model": "viam:lidar:rplidar",
      "name": "rplidar"
  }
  ```

  {{% /tab %}}
  {{% tab name="macOS x86_64" %}}

  Copy and paste the JSON object for the module into the modules array to add the module:

  ```json
  {
      "executable_path": "/usr/local/bin/rplidar-module",
      "name": "my_rplidar_module_name"
  }
  ```

  Next, add the following JSON object to your components array to configure a `rplidar` [camera](/components/camera/) component with the name `rplidar`:

  ```json
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
  ```

  {{% /tab %}}
  {{% tab name="macOS ARM64 (M1 & M2)" %}}

  Copy and paste the JSON object for the module into the modules array to add the module:

  ```json
  {
      "executable_path": "/usr/local/bin/rplidar-module",
      "name": "my_rplidar_module_name"
  }
  ```

  Next, add the following JSON object to your components array to configure a `rplidar` [camera](/components/camera/) component with the name `rplidar`:

  ```json
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
  ```

  If you are on an M1 or M2 Macbook, determine the device path by running the following command:

  ```sh {class="command-line" data-prompt="$"}
  ls /dev/ | grep tty.usbserial
  ```

  For example, you may see `tty.usbserial-130`, in which case your device path would be `/dev/tty.usbserial-130`.
  Replace the `XXX` at the end of the `device_path` value in the attributes configuration with the number at the end of your device path.

  {{% /tab %}}
  {{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

Then, save the config.

Check the **Logs** tab of your robot in the Viam app to make sure your RPlidar has connected and no errors are being raised.

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
  {{% card link="/services/slam/cartographer" %}}
  {{% card link="/services/slam" %}}
{{< /cards >}}
