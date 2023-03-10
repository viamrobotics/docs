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

For example, you could use a joystick alongside a numpad.

## Configuration

To combine multiple controlers into a `mux` controller, you must first configure each controller individually.

The following example configuration combines a `gamepad` and a `webgamepad` controller:

{{< tabs name="Configure a `mux` input controller" >}}
{{< tab name="Config Builder" >}}

<img src="../img/mux-input-controller-ui-config.png" alt="What configuration for a multiplexed input controller component looks like in the Viam App config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="JSON Template" %}}

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
| `sources` | *Required* | An array of `name`s of each input controller component that should be combined in the `mux` model. |

{{% alert title="Note" color="note" %}}
You must put each controller's `name` that you add in `sources` in `depends_on`.
This tells the program loading the config to fully load the source components first.
{{% /alert %}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< readfile "/static/include/social.md" >}}
