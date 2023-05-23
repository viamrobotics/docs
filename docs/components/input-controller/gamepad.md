---
title: "Configure a linux-supported gamepad"
linkTitle: "gamepad"
weight: 30
type: "docs"
description: "Configure a linux-supported gamepad as an input controller."
images: ["/components/img/components/controller.svg"]
tags: ["input controller", "components"]
# SMEs: James
---

Configuring a `gamepad` input controller allows you to use a Linux-supported gamepad as a device to communicate with your robot.
Linux supports most standard gamepads, such as PlayStation or Xbox type game controllers, as well as many joysticks, racing wheels, and more.

## Configuration

Refer to the following example configuration for an input controller of model `gamepad`:

{{< tabs name="Configure a `gamepad` input controller" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your input controller, select the type `input_controller`, and select the `gamepad` model.

Click **Create component**.

![An example configuration for a linux-based gamepad input controller component in the Viam App config builder](../img/gamepad-input-controller-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name":  "<your-gamepad-input-controller>",
      "type": "input_controller",
      "model": "gamepad",
      "attributes": {
        "dev_file": "<string>",
        "auto_reconnect": <boolean>
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gamepad` input controllers:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `dev_file` | string | Optional | If `dev_file` is left blank or not included, `viam-server` will search and use the first gamepad it finds that's connected to the computer controlling your robot. If you want to specify a device, give the absolute path to the input device event file. For example: `/dev/input/event42`. |
| `auto_reconnect` | boolean | Optional | Applies to both remote (gRPC) and local (bluetooth or direct USB connected) devices. If set to `true`, `viam-server` tries to (re)connect the device automatically. It waits for a device to connect during a robot's start-up. If set to false (default) then start-up fails if a device is not already connected.

## Usage

Connect your controller to your computer.
Follow the instructions included with your gamepad to make this connection.

If you haven't done so already, create a robot in [the Viam app](https://app.viam.com), and follow the instructions in the **Setup** tab to start `viam-server` on your computer and connect to the robot.

Then, click on the robot's **Config** tab and configure an `input_controller` component of model `gamepad`, as shown above.
Save the config.

Next, navigate to the **Control** tab.
You should see a drop-down menu with the name of your gamepad.
Click on the drop-down menu to expand it.

Now, you should see the [Controls](../#control-field) on your input controller appear:

<img src="../img/gamepad-enabled-app.png" alt="The dropdown as a table of controls available and their inputs in the Control tab of the Viam app." style="width:100%"/>

You should now be able to see the row of [Controls](../#control-field) respond to your button presses and stick toggles.

For example, this is what the row of inputs above looks like after pressing the circle (west) button on the button pad of a PS4 controller connected as a `webgamepad` :

<img src="../img/gamepad-enabled-app-with-input.png" alt="The dropdown as a table of controls available for a web-based gamepad and their inputs in the Control tab of the Viam app. This is for a WebGamepad model." style="width:100%"/>

{{% alert title="Note" color="note" %}}
The **Enable** toggle shown in this example is only shown for the `webgamepad` and not shown when a linux-supported `gamepad` model is directly connected.
{{% /alert %}}

### Work in Progress Models

Mappings are currently available for a wired XBox 360 controller, and wireless XBox Series X|S, along with the 8bitdo Pro 2 bluetooth gamepad (which works great with the Raspberry Pi).

The XBox controllers emulate an XBox 360 gamepad when in wired mode, as does the 8bitdo.

Because of that, any unknown gamepad is mapped as an XBox 360.

If you have another controller that you want to use to control your robot, feel free to submit a PR on [Github](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) with new mappings.

## Troubleshooting

- If you are not able to see a drop-down menu with the name of your controller appear in the **Control** tab, try specifying the `dev_file` attribute to match the exact path to your device.
You can also try setting `auto_reconnect` to `True`.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
