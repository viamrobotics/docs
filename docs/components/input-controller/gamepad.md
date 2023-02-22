---
title: "Configure a linux-based gamepad"
linkTitle: "gamepad"
weight: 30
type: "docs"
description: "Configure a linux-based gamepad as an input controller."
tags: ["input controller", "components"]
# SMEs: James
---

Configuring a `gamepad` input controller allows you to use a Linux-based gamepad as a device to communicate with your robot.
Most standard gamepads, such as xbox or playstation type game controllers, are Linux-based.

## Configuration

Refer to the following example configuration for an input controller of model `gamepad`:

{{< tabs name="Configure a `gamepad` input controller" >}}
{{< tab name="Config Builder" >}}

<img src="../img/gamepad-input-controller-ui-config.png" alt="What an example configuration for a linux-based gamepad input controller component looks like in the Viam App config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="Raw Json" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name":  <your-gamepad-input-controller-name>,
      "type": "input_controller",
      "model": "gamepad",
      "attributes": {
        "dev_file": "",
        "auto_reconnect": false
      },
      "depends_on": [
        <your-board-name>
      ]
    }, ...
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gamepad` input controllers:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `dev_file` | *Optional* | If `dev_file` is left blank or not included, `viam-server` will search and use the first gamepad it finds that's connected to the computer controlling your robot. If you want to specify a device, give the absolute path to the input device event file. For example: "<file>/dev/input/event42</file>" |
| `auto_reconnect` | *Optional* | If set to `true`, `viam-server` will set the device to be automatically connected, waiting for a device to connect during a robot's start-up, and start-up will fail if a device is not connected. Defaults to `false` if not included. |

Note that `auto_reconnect` applies to both remote (gRPC) and local (bluetooth or direct USB connected) devices.

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
