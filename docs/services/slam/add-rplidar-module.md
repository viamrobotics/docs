---
title: "Add a Rplidar as a Modular Component"
linkTitle: "Add a Rplidar as a Modular Component"
weight: 70
type: "docs"
description: "How to add a Rplidar as a modular component of your robot."
tags: ["slam", "services"]
# SMEs: Kat, Jeremy
---

{{% alert title="Note" color="note" %}}
The SLAM Service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

## Instructions

First, install the Rplidar Module:

{{< tabs >}}
{{% tab name="Linux aarch64" %}}

```bash
sudo curl -o /usr/local/bin/rplidar-module http://packages.viam.com/apps/rplidar/rplidar-module-latest-aarch64.AppImage
sudo chmod a+rx /usr/local/bin/rplidar-module
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

```bash
sudo curl -o /usr/local/bin/rplidar-module http://packages.viam.com/apps/rplidar/rplidar-module-latest-x86_64.AppImage
sudo chmod a+rx /usr/local/bin/rplidar-module
```

{{% /tab %}}
{{% tab name="MacOS" %}}

```bash
brew tap viamrobotics/brews && brew install rplidar-module
```

{{% /tab %}}
{{< /tabs >}}

Now, add the Rplidar as a modular component of your robot in the [Viam app](https://app.viam.com/):

1. Physically connect the Rplidar to your machine.
2. Go to your robot's page on the [Viam app](https://app.viam.com/).
3. In the **CONFIG** tab, select **Raw JSON** mode.
4. Copy the following configuration code for your Rplidar device.
  Paste it into the **Raw JSON** block:

  {{< tabs >}}
  {{% tab name="Linux" %}}

  ```json
  {
    "components": [
      {
        "namespace": "rdk",
        "type": "camera",
        "depends_on": [],
        "model": "viam:lidar:rplidar",
        "name": "rplidar"
      }
    ],
    "modules": [
      {
        "executable_path": "rplidar-module",
        "name": "rplidar-module"
      }
    ]
  }
  ```

  {{% /tab %}}
  {{% tab name="MacOS" %}}

  ```json
  {
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
    ],
    "modules": [
      {
        "executable_path": "rplidar-module",
        "name": "rplidar_module"
      }
    ]
  }
  ```

  {{% /tab %}}
  {{< /tabs >}}

5. Save the config.

Check the **LOGS** tab of your robot in the Viam app to make sure your Rplidar has connected and no errors are being raised.
