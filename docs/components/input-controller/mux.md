---
title: "Configure a Mux Input Controller"
linkTitle: "mux"
weight: 30
type: "docs"
description: "Configure a mux input controller to combine one or more input controllers."
images: ["/icons/components/controller.svg"]
tags: ["input controller", "components"]
aliases:
  - "/components/input-controller/mux/"
# SMEs: James
---

Configuring a `mux` (multiplexed) input controller allows you to combine one or more controllers into a single virtual controller.

This lets you control a robot from different locations, such as the web and a locally connected gamepad, or use multiple controllers as one device.

For example, you could use a joystick alongside a numpad.

## Configuration

To combine multiple controlers into a `mux` controller, you must first configure each controller individually.

{{< tabs name="Configure a `mux` input controller" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `input_controller` type, then select the `mux` model.
Enter a name for your input controller and click **Create**.

![An example configuration for a multiplexed input controller component in the Viam App config builder](/components/input-controller/mux-input-controller-ui-config.png)

Copy and paste the following attribute template into your input controller's **Attributes** box.
Then remove and fill in the attributes as applicable to your input controller, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "sources": [
    "<your-gamepad-input-controller-name",
    "<your-other-gamepad-input-controller-name>"
  ]
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "sources": ["myGamepad", "WebGamepad"]
}
```

{{% /tab %}}
{{< /tabs >}}

From the **Depends On** dropdown menu, select all of the source input controllers for your `mux` controller to combine.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-mux-input-controller-name>",
      "model": "mux",
      "type": "input_controller",
      "namespace": "rdk",
      "attributes": {
        "sources": [
          "<your-gamepad-input-controller-name",
          "<your-other-gamepad-input-controller-name>"
        ]
      },
      "depends_on": [
        "<your-gamepad-input-controller-name>",
        "<your-other-gamepad-input-controller-name>"
      ]
    }
    <...CONFIGS FOR THE INDIVIDUAL INPUT CONTROLLERS...>
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

The following example configuration combines a `gamepad` and a `webgamepad` controller:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "my-combined-controller",
      "model": "mux",
      "type": "input_controller",
      "namespace": "rdk",
      "attributes": {
        "sources": ["myGamepad", "WebGamepad"]
      },
      "depends_on": ["myGamepad", "WebGamepad"]
    },
    {
      "name": "myGamepad",
      "model": "gamepad",
      "type": "input_controller",
      "namespace": "rdk",
      "attributes": {
        "auto_reconnect": true
      },
      "depends_on": []
    },
    {
      "name": "WebGamepad",
      "model": "webgamepad",
      "type": "input_controller",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `mux` input controllers:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `sources` | array | **Required** | The `name` of every controller component you wish to combine input from. |

{{% alert title="Important" color="note" %}}
You must put each controller's `name` that you add in `sources` in `depends_on`.
This tells the program loading the config to fully load the source components first.
{{% /alert %}}

{{< readfile "/static/include/components/test-control/input-controller-control.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
