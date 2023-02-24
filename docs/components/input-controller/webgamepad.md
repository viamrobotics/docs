---
title: "Configure a webgamepad"
linkTitle: "webgamepad"
weight: 30
type: "docs"
description: "Configure a web-based gamepad as an input controller."
tags: ["input controller", "components"]
# SMEs: James
---

Configuring a `webgamepad` input controller allows you to use a web-based gamepad as a device to communicate with your robot.

This allows a gamepad to connect to your robot remotely through a browser and the `html5` Gamepad API.

{{% alert="Note" color="note" %}}
You **must** use "WebGamepad" as the `name` of the web gamepad controller. This restriction will be removed in the future.
{{% /alert %}}

## Configuration

Refer to the following example configuration for an input controller of model `webgamepad`:

{{< tabs name="Configure a `webgamepad` input controller" >}}
{{< tab name="Config Builder" >}}

<img src="../img/webgamepad-input-controller-ui-config.png" alt="What an example configuration for a web-based gamepad input controller component looks like in the Viam App config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "components": [
    {
      "name": "WebGamepad",
      "type": "input_controller",
      "model": "webgamepad",
      "attributes": {},
      "depends_on": []
    }
}
```

{{% /tab %}}
{{< /tabs >}}

## Use

After adding the above configuration, when viewing your robot in [the Viam app](https://app.viam.com) or at your robot's local address (like "myrobot.local:8080"), you'll see the WebGamepad component.

Connect any compatible web-based gamepad to your PC, and press any button or stick on the gamepad.
Then, you should see the name of your controller appear where you're viewing your robot, and the input displays respond to the controls.

When ready, click "Enable" in the upper right to "connect" the controller to the robot, and let it begin receiving inputs.

{{% alert="Note" color="note" %}}
For your security, the browser won't report a gamepad until an input has been sent.
{{% /alert %}}
<!-- TODO: testing, may need to add more info re. this tutorial (or at the least add it to next steps)

Using the gamepad requires a service.
To see how the service is configured, navigate to the **SERVICES** section under the **CONFIG** tab.
The **SERVICES** subtab contains the "Base Remote Control" service which uses three attributes:

- **base**: `viam_base`
- **control_mode**: `joystickControl`
- **input_controller**: `WebGamepad`

The names for **base** and **input_controller** correspond to the naming scheme from the **COMPONENTS** tab.

![Screenshot of the base remote control service named "base_rc" on the Services sub-tab of the CONFIG tab.](../img/try-viam/base-rc.png) -->

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
