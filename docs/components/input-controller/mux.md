---
title: "Configure a mux input controller"
linkTitle: "mux"
weight: 30
type: "docs"
description: "Configure a mux input controller to combine one or more input controllers."
images: ["/icons/components/controller.svg"]
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
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your input controller, select the type `input_controller`, and select the `mux` model.

Click **Create component**.

![An example configuration for a multiplexed input controller component in the Viam App config builder](/components/input-controller/mux-input-controller-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-mux-input-controller-name>",
      "type": "input_controller",
      "model": "mux",
      "attributes": {
        "sources": [
          "<your-gamepad-input-controller-name",
          "WebGamepad"
        ]
      },
      "depends_on": [
        "<your-gamepad-input-controller-name>",
        "WebGamepad"
      ]
    },
    {
      "name": "<your-gamepad-input-controller-name>",
      "type": "input_controller",
      "model": "gamepad",
      "attributes": {
        "dev_file": "<your-filepath>",
        "auto_reconnect": <boolean>
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

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `sources` | array | **Required** | The `name` of every controller component you wish to combine input from. |

{{% alert title="Important" color="note" %}}
You must put each controller's `name` that you add in `sources` in `depends_on`.
This tells the program loading the config to fully load the source components first.
{{% /alert %}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
