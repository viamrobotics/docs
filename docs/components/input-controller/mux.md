---
title: "Configure a mux input controller"
linkTitle: "mux"
weight: 30
type: "docs"
description: "Configure a mux input controller to combine one or more input controllers."
tags: ["input controller", "components"]
# SMEs: James
---

Configuring a `mux` (multiplexed) input controller allows you to combine one or more controllers into a single virtual controller.

This lets you control a robot from different locations, such as the web and a locally connected gamepad, or use multiple controllers as one device.

For example, a joystick could be added to a numpad.

## Configuration

{{% alert="Note" color="note" %}}
You must give the other input controllers their own component configuration, as shown below with a `gamepad` and `webgamepad`, to combine them in the `mux` model.
{{% /alert %}}

Refer to the following example configuration for an input controller of model `mux`:

{{< tabs name="Configure a `mux` input controller" >}}
{{< tab name="Config Builder" >}}

<img src="../img/mux-input-controller-ui-config.png" alt="Example of what configuration for a multiplexed input controller component looks like in the Viam App config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="Raw Json" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <your-mux-input-controller>,
      "type": "input_controller",
      "model": "mux",
      "attributes": {
        "sources": [
          <your-gamepad-input-controller,
          "WebGamepad"
        ]
      },
      "depends_on": [
        <your-gamepad-input-controller>,
        "WebGamepad"
      ]
    },
    {
      "name": <your-gamepad-input-controller>,
      "type": "input_controller",
      "model": "gamepad",
      "attributes": {
        "dev_file": "",
        "auto_reconnect": false
      },
      "depends_on": []
    },
    {
      "name": "WebGamepad",
      "type": "input_controller",
      "model": "webgamepad",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `mux` input controllers:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `sources` | *Required* | The `name` of each input controller component that should be combined in the `mux` model. |

{{% alert="Note" color="note" %}}
You must also put each name in `sources` in `depends_on`, as shown above.
This tells the program loading the config to fully load the source components first.
{{% /alert %}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
