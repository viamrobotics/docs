---
title: "Add a Rplidar as a Modular Component"
linkTitle: "Add a Rplidar as a Modular Component"
weight: 40
type: "docs"
description: "How to add a Rplidar as a modular component of your robot."
image: "/program/img/modular-resources/rplidar-on-robot.png"
tags: ["slam", "services"]
# SMEs: Kat, Jeremy
---

{{% alert title="Note" color="note" %}}
The {{< glossary_tooltip term_id="slam" >}} Service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

## Requirements

Install the `rplidar-module` binary on your machine and make it executable by running the following commands according to your machine's architecture:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```{id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/rplidar-module https://storage.googleapis.com/packages.viam.com/apps/rplidar/rplidar-module-latest-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/rplidar-module
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

```{id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/rplidar-module https://storage.googleapis.com/packages.viam.com/apps/rplidar/rplidar-module-latest-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/rplidar-module
```

{{% /tab %}}
{{% tab name="MacOS" %}}

```{id="terminal-prompt" class="command-line" data-prompt="$"}
brew tap viamrobotics/brews && brew install rplidar-module
```

{{% /tab %}}
{{< /tabs >}}

## Configuration

Physically connect the Rplidar to your machine. Go to your robot's page on the [Viam app](https://app.viam.com/).

{{< tabs name="Add the Rplidar component">}}
{{% tab name="Config Builder" %}}
Navigate to the **config** tab on your robot's page, and click on the **Components** subtab.

Add a component with type `camera`, model `viam:lidar:rplidar`, and a name of your choice:

![adding rplidar component](../img/add-rplidar/add-rplidar-component-ui.png)

Paste the following into the **Attributes** field of your new component according to your machine's architecture:

{{< tabs name="Add Rplidar Configs">}}
{{% tab name="MacOS x86_64" %}}

```json
{
  "device_path": "/dev/tty.SLAB_USBtoUART"
}
```

{{% /tab %}}

{{% tab name="MacOS ARM64 (M1 & M2)" %}}

```json
{
  "device_path": "/dev/tty.usbserial-0001"
}
```

{{% /tab %}}
{{< /tabs >}}

Click on the **Modules** subtab. Add the rplidar module with a name of your choice and an executable path that points to the location of your installed `rplidar-module` binary:

{{< tabs name="Add Rplidar Component Module">}}
{{% tab name="Linux/MacOS x86_64" %}}

![adding rplidar module linux](../img/add-rplidar/add-rplidar-module-ui-linux.png)

{{% /tab %}}

{{% tab name="MacOS ARM64 (M1 & M2)" %}}

![adding rplidar module M1 M2](../img/add-rplidar/add-rplidar-module-ui-M1-M2.png)

{{% /tab %}}
{{< /tabs >}}
{{% /tab %}}
{{% tab name="JSON Template" %}}

Navigate to the **config** tab.
Select the **Raw JSON** mode, then copy/paste the following `"components"` and `"modules"` JSON:

  {{< tabs name="Add the Rplidar component - configs" >}}
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
  {{% tab name="MacOS x86_64" %}}

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
  {{% tab name="MacOS ARM64 (M1 & M2)" %}}

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
          "device_path": "/dev/tty.usbserial-0001"
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

Check the **logs** tab of your robot in the Viam app to make sure your Rplidar has connected and no errors are being raised.

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
  {{% card link="/services/slam/cartographer" size="small" %}}
  {{% card link="/services/slam" size="small" %}}
{{< /cards >}}
