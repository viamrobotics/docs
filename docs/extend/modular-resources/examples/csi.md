---
title: "Add an ODrive motor as a Modular Resource"
linkTitle: "ODrive"
weight: 40
type: "docs"
description: "How to add an ODrive motor with serial or CANbus communication as a modular resource of your robot."
tags: ["motor", "odrive", "canbus", "serial", "module", "modular resources", "Python", "python SDK", "CAN"]
# SMEs: Kim, Martha, Rand
---

The [Viam GitHub](https://github.com/viamrobotics/odrive) provides an implementation of ODrive Robotics' [ODrive S1](https://odriverobotics.com/shop/odrive-s1) motor driver as module defining two modular resources [extending](/extend/modular-resources/) the [motor API](/components/motor/#api) as new motor types.

[Install requirements](#requirements) and [configure](#configuration) the module to configure an `serial` or `canbus` [motor](/components/motor/) {{< glossary_tooltip term_id="resource" text="resource" >}} on your robot.

## Requirements

On your robot's computer, download [the Viam `csi` appimage](https://github.com/viamrobotics/odrive) and make it executable:

``` {class="command-line" data-prompt="$"}
sudo wget https://github.com/seanavery/viam-csi/releases/download/v0.0.2/viam-csi-0.0.2-aarch64.AppImage -O /usr/local/bin/viam-csi
sudo chmod 755 /usr/local/bin/viam-csi
```

## Configuration

### Module

{{< tabs name="Add the ODrive module">}}
{{% tab name="Config Builder" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page, and click on the **Modules** subtab.

Copy and  the csi module with a name of your choice.

![The ODrive module with the name 'odrive' and executable path '~/desktop/odrive/odrive-motor/run.sh' added to a robot in the Viam app config builder](/extend/modular-resources/add-odrive/add-odrive-module-ui.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.
Copy and paste the following raw JSON to add a `csi` [camera](/components/camera) component with the name `my_test_csicam`:

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
        "name": "my_test_csicam",
        "namespace": "rdk",
        "type": "camera"
      }
    ]
}
```

Save the config.

{{% /tab %}}
{{< /tabs >}}

Edit and fill in the attributes as applicable to your `csi` camera.

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for the `csi` camera resource made programmatically available in the `viam:camera:csi` module:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `width_px` | int | Optional | . <br> Example: `0` |
| `height_px` | string | Optional | . |
| `frame__rate` | string | Optional | . |
| `debug` | string | Optional | . <br> Example: `"250k"` |

Save the config.
Check the [**Logs** tab](/program/debug/) of your robot in the Viam app to make sure your `csi` camera has connected and no errors are being raised.
