---
title: "Configure a webgamepad"
linkTitle: "webgamepad"
weight: 30
type: "docs"
description: "Configure a web-based gamepad as an input controller."
images: ["/icons/components/controller.svg"]
tags: ["input controller", "components"]
# SMEs: James
---

Configuring a `webgamepad` input controller allows you to use a web-based gamepad as a device to communicate with your robot.

{{% alert title="Important" color="note" %}}
You **must** use "WebGamepad" as the `name` of the web gamepad controller.
This restriction will be removed in the future.
{{% /alert %}}

## Configuration

Use the following configuration for an input controller of model `webgamepad`:

{{< tabs name="Configure a `webgamepad` input controller" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `input_controller` type, then select the `webgamepad` model.
Enter the name `WebGamepad` and click **Create**.

![An example configuration for a web-based gamepad input controller component in the Viam App config builder](/components/input-controller/webgamepad-input-controller-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
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

## Usage

Connect your controller to your computer.
Follow the instructions included with your gamepad to make this connection.

If you haven't done so already, create a robot in [the Viam app](https://app.viam.com), and follow the instructions in the **Setup** tab to start `viam-server` on your computer and connect to the robot.

Then, click on the robot's **Config** tab and configure an `input_controller` component of model `webgamepad` and name `WebGamepad`, as shown above.
Save the config.

Next, navigate to the **Control** tab.
You should see a `WebGamepad` drop-down menu.
Click on the drop-down menu to expand it.
Click **Enable**, and press a button on your controller.
Then, you should see the [Controls](../#control-field) on your input controller appear:

![The dropdown as a table of controls available and their inputs in the Control tab of the Viam app. This is for a WebGamepad model.](/components/input-controller/gamepad-enabled-app.png)

You should now be able to see the row of control inputs respond to your button presses and stick toggles.

For example, this is how the row of [Controls](../#control-field) appears after pressing the circle (west) button on the button pad of the connected PS4 controller:

![The dropdown as a table of controls available for a web-based gamepad and their inputs in the Control tab of the Viam app.](/components/input-controller/gamepad-enabled-app-with-input.png)

{{% alert title="Important" color="note" %}}
You have to press a button or move a stick on your gamepad for the browser to report the gamepad.
For your security, the browser won't report a gamepad until an input has been sent.
{{% /alert %}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
