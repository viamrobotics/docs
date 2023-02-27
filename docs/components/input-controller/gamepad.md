---
title: "Configure a linux-based gamepad"
linkTitle: "gamepad"
weight: 30
type: "docs"
description: "Configure a linux-based gamepad as an input controller."
tags: ["input controller", "components"]
# SMEs: James
---

Configuring a `gamepad` input controller allows you to use a Linux-supported gamepad as a device to communicate with your robot.
Linux supports most standard gamepads, such as PlayStation or Xbox type game controllers, as well as many joysticks, racing wheels, and more.

## Configuration

Refer to the following example configuration for an input controller of model `gamepad`:

{{< tabs name="Configure a `gamepad` input controller" >}}
{{< tab name="Config Builder" >}}

<img src="../img/gamepad-input-controller-ui-config.png" alt="What an example configuration for a linux-based gamepad input controller component looks like in the Viam App config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name":  <your-gamepad-input-controller>,
      "type": "input_controller",
      "model": "gamepad",
      "attributes": {
        "dev_file": "",
        "auto_reconnect": false
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gamepad` input controllers:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `dev_file` | *Optional* | If `dev_file` is left blank or not included, `viam-server` will search and use the first gamepad it finds that's connected to the computer controlling your robot. If you want to specify a device, give the absolute path to the input device event file. For example: `/dev/input/event42` |
| `auto_reconnect` | *Optional* | If set to `true`, `viam-server` tries to connect the device automatically. It waits for a device to connect during a robot's start-up, and start-up fails if a device is not connected. Defaults to `false` if not included. |

{{% alert="Note" color="note" %}}
`auto_reconnect` applies to both remote (gRPC) and local (bluetooth or direct USB connected) devices.
{{% /alert %}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
