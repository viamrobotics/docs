---
title: "Add a Rplidar as a Modular Component"
linkTitle: "Add a Rplidar as a Modular Component"
weight: 40
type: "docs"
description: "How to add a Rplidar as a modular component of your robot."
tags: ["slam", "services"]
# SMEs: Kat, Jeremy
---

{{% alert title="Note" color="note" %}}
The {{< glossary_tooltip term_id="slam" >}} Service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

First, install the Rplidar Module:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```{id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/rplidar-module http://packages.viam.com/apps/rplidar/rplidar-module-latest-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/rplidar-module
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

```{id="terminal-prompt" class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/rplidar-module http://packages.viam.com/apps/rplidar/rplidar-module-latest-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/rplidar-module
```

{{% /tab %}}
{{% tab name="MacOS" %}}

```{id="terminal-prompt" class="command-line" data-prompt="$"}
brew tap viamrobotics/brews && brew install rplidar-module
```

{{% /tab %}}
{{< /tabs >}}

Now, add the Rplidar as a modular component of your robot in the [Viam app](https://app.viam.com/):

1. Physically connect the Rplidar to your machine.
2. Go to your robot's page on the [Viam app](https://app.viam.com/).
3. In the **config** tab, select **Raw JSON** mode.
4. Copy the following configuration code for your Rplidar device.
  Paste it into the **Raw JSON** block:

  {{< tabs >}}
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

5. Save the config.

Check the **logs** tab of your robot in the Viam app to make sure your Rplidar has connected and no errors are being raised.

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
  {{% card link="/services/slam/cartographer" size="small" %}}
  {{% card link="/services/slam" size="small" %}}
{{< /cards >}}
