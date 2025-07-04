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
component_description: "Supports multiplexed controllers, combining multiple sources of input."
toc_hide: true
# SMEs: James
---

Configuring a `mux` (multiplexed) input controller allows you to combine one or more controllers into a single virtual controller.

This lets you control a machine from different locations, such as the web and a locally connected gamepad, or use multiple controllers as one device.

For example, you could use a joystick alongside a numpad.

## Configuration

To combine multiple controllers into a `mux` controller, you must first configure each controller individually.

{{< tabs name="Configure a `mux` input controller" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `input_controller` type, then select the `mux` model.
Enter a name or use the suggested name for your input controller and click **Create**.

![An example configuration for a multiplexed input controller component](/components/input-controller/mux-input-controller-ui-config.png)

Enter the name of each source input controller in `sources`.

Also, select each of the source input controllers in the **Depends on** dropdown menu.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-mux-input-controller-name>",
      "model": "mux",
      "api": "rdk:component:input_controller",
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
      "api": "rdk:component:input_controller",
      "attributes": {
        "sources": ["myGamepad", "WebGamepad"]
      },
      "depends_on": ["myGamepad", "WebGamepad"]
    },
    {
      "name": "myGamepad",
      "model": "gamepad",
      "api": "rdk:component:input_controller",
      "attributes": {
        "auto_reconnect": true
      },
      "depends_on": []
    },
    {
      "name": "WebGamepad",
      "model": "webgamepad",
      "api": "rdk:component:input_controller",
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `sources` | array | **Required** | The `name` of every controller component you wish to combine input from. |

{{% alert title="Important" color="note" %}}
You must put each controller's `name` that you add in `sources` in `depends_on`.
This tells the program loading the config to fully load the source components first.
{{% /alert %}}

{{< readfile "/static/include/components/test-control/input-controller-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/input-controller.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/input-controller/" customTitle="Input controller API" noimage="true" %}}
{{% card link="/operate/get-started/supported-hardware/" noimage="true" %}}
{{% card link="/tutorials/control/gamepad/" noimage="true" %}}
{{< /cards >}}
