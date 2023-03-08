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

{{% alert title="Note" color="note" %}}
You **must** use "WebGamepad" as the `name` of the web gamepad controller. This restriction will be removed in the future.
{{% /alert %}}

## Configuration

Use the following configuration for an input controller of model `webgamepad`:

{{< tabs name="Configure a `webgamepad` input controller" >}}
{{< tab name="Config Builder" >}}

<img src="../img/webgamepad-input-controller-ui-config.png" alt="What an example configuration for a web-based gamepad input controller component looks like in the Viam App config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="JSON Template" %}}

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
  ],
    "services": [
      {
        "name": "base-rc",
        "type": "base_remote_control",
        "attributes": {
          "control_mode": "joystickControl",
          "base": "base", // You do not need to have configured a base.
          "input_controller": "WebGamepad"
        }
      }
    ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Usage with Base Remote Control Service

Connect your controller to your computer.
If you haven't done so already, create a robot in [the Viam app](https://app.viam.com), and follow the instructions in the **SETUP** tab to start `viam-server` on your computer and connect to the robot.

Then, click on the robot's **CONFIG** tab and configure an `input_controller` component of model `webgamepad`, as shown above.

Configure a base component with name `base` and model `fake` as well.
This component does not need to have any attributes added to its configuration, but will keep the service from having errors as it starts.

Next, click on the **SERVICES** sub tab of **CONFIG** and add a service of type `base_remote_control`.

<img src="../img/base-rc-service-config.png" alt="What an example configuration for the Base Remote Control service of a web-based gamepad input controller component looks like in the Viam App." style="width:100%"/>

{{% alert="Note" title="Note" color="note" %}}
You do not have to possess base hardware to use the "Base Remote Control" service to connect to your controller.

For now, `"control_mode": "joystickControl"` does not affect the controls that are available to use on your gamepad.
Buttons are still available with this configuration.

Support for this component is still experimental, and this page will be updated as the interface develops.
{{% /alert %}}

After both the service and component are configured, navigate to the **CONTROL** tab.
There, you should be able to see a `WebGamepad` drop-down appear.
Click **Enable**, and click buttons on your controller.
Then, you should see the controls of your robot and the current input for each control displayed.

<img src="../img/gamepad-enabled-app.png" alt="The dropdown as a table of controls available and their inputs in the Control tab of the Viam app." style="width:100%"/>

Press any button or toggle any stick on the gamepad.
You should now be able to see the row of control inputs respond to your button presses and stick toggles.
For example, this is what the row of inputs above looks like *after* pressing the left button on the diamond button pad of the connected PS4 controller.

<img src="../img/gamepad-enabled-app-with-input.png" alt="The dropdown as a table of controls available for a web-based gamepad and their inputs in the Control tab of the Viam app." style="width:100%"/>

{{% alert title="Note" color="note" %}}
You have to press a button or move a stick on your gamepad for the browser to report the gamepad.
For your security, the browser won't report a gamepad until an input has been sent.
{{% /alert %}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
