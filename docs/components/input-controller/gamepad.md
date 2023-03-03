---
title: "Configure a linux-supported gamepad"
linkTitle: "gamepad"
weight: 30
type: "docs"
description: "Configure a linux-supported gamepad as an input controller."
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
        "dev_file": <string>,
        "auto_reconnect": <boolean>
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gamepad` input controllers:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `dev_file` | *Optional* | If `dev_file` is left blank or not included, `viam-server` will search and use the first gamepad it finds that's connected to the computer controlling your robot. If you want to specify a device, give the absolute path to the input device event file. For example: `/dev/input/event42`. |
| `auto_reconnect` | *Optional* | Applies to both remote (gRPC) and local (bluetooth or direct USB connected) devices. If set to `true`, `viam-server` tries to (re)connect the device automatically. It waits for a device to connect during a robot's start-up. If set to false (default) then start-up fails if a device is not already connected. 

## Usage with Base Remote Control Service

Connect your controller to your computer.
If you haven't done so already, create a robot in [the Viam app](https://app.viam.com), and follow the instructions in the **SETUP** tab to start `viam-server` on your computer and connect to the robot.

Then, click on the robot's **CONFIG** tab and configure an `input_controller` component of model `gamepad`, as shown above.

Next, click on the **SERVICES** sub tab of **CONFIG** and add a service of type `base_remote_control`.

<img src="../img/base-rc-service-config.png" alt="What an example configuration for the Base Remote Control service of a web-based gamepad input controller component looks like in the Viam App." style="width:100%"/>

{{% alert title="Note" color="note" title%}}
You do not need to configure a base component and control it with the input controls to use the "Base Remote Control" service to connect to your controller.

For now, `"control_mode": "joystickControl"` does not affect the controls that are available to use on your gamepad.
Buttons are still available with this configuration.

Support for this component is still experimental, and this page will be updated as the interface develops.
{{% /alert %}}

After both the service and component are configured, navigate to the **CONTROL** tab.
There, you should be able to see a drop-down menu appear with the name of your gamepad.
Click **Enable**, and click buttons on your controller.
Then, you should see the controls of your robot and the current input for each control displayed.

<img src="../img/gamepad-enabled-app.png" alt="The dropdown as a table of controls available and their inputs in the Control tab of the Viam app." style="width:100%"/>

Press any button or toggle any stick on the gamepad.
You should now be able to see the row of control inputs respond to your button presses and stick toggles.
For example, this is what the row of inputs above looks like *after* pressing the left button on the diamond button pad of the connected PS4 controller.

<img src="../img/gamepad-enabled-app-with-input.png" alt="The dropdown as a table of controls available and their inputs in the Control tab of the Viam app." style="width:100%"/>

{{% alert title="Note" color="note" %}}
You have to press a button or move a stick on your gamepad for the browser to report the gamepad.
For your security, the browser won't report a gamepad until an input has been sent.
{{% /alert %}}

### Work in Progress Models

Mappings are currently available for a wired XBox 360 controller, and wireless XBox Series X|S, along with the 8bitdo Pro 2 bluetooth gamepad (which works great with the Raspberry Pi).

The XBox controllers emulate an XBox 360 gamepad when in wired mode, as does the 8bitdo.

Because of that, any unknown gamepad will be be mapped that way.
If you have another controller that you want to use to control your robot, feel free to submit a PR on [Github](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) with new mappings.

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
