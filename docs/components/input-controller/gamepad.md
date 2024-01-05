---
title: "Configure a Linux-supported Gamepad"
linkTitle: "gamepad"
weight: 30
type: "docs"
description: "Configure a linux-supported gamepad as an input controller."
images: ["/icons/components/controller.svg"]
tags: ["input controller", "components"]
aliases:
  - "/components/input-controller/gamepad/"
# SMEs: James
---

Configuring a `gamepad` input controller allows you to use a Linux-supported gamepad as a device to communicate with your machine.
Linux supports most standard gamepads, such as PlayStation or Xbox type game controllers, as well as many joysticks, racing wheels, and more.

{{< tabs name="Configure a `gamepad` input controller" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `input_controller` type, then select the `gamepad` model.
Enter a name for your input controller and click **Create**.

![An example configuration for a linux-based gamepad input controller component in the Viam App config builder](/components/input-controller/gamepad-input-controller-ui-config.png)

Copy and paste the following attribute template into your input controller's **Attributes** box.
Then remove and fill in the attributes as applicable to your input controller, according to the table below.

```json {class="line-numbers linkable-line-numbers"}
{
  "dev_file": "<string>",
  "auto_reconnect": <boolean>
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name":  "<your-gamepad-input-controller>",
      "model": "gamepad",
      "type": "input_controller",
      "namespace": "rdk",
      "attributes": {
        "dev_file": "<string>",
        "auto_reconnect": <boolean>
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gamepad` input controllers:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `dev_file` | string | Optional | If `dev_file` is left blank or not included, `viam-server` will search and use the first gamepad it finds that's connected to the computer controlling your machine. If you want to specify a device, give the absolute path to the input device event file. For example: `/dev/input/event42`. |
| `auto_reconnect` | boolean | Optional | Applies to both remote (gRPC) and local (bluetooth or direct USB connected) devices. If set to `true`, `viam-server` tries to (re)connect the device automatically. It waits for a device to connect during a machine's start-up. If set to false (default) then start-up fails if a device is not already connected.

{{< readfile "/static/include/components/test-control/input-controller-control.md" >}}

### Work in Progress Models

Mappings are currently available for a wired XBox 360 controller, and wireless XBox Series X|S, along with the 8bitdo Pro 2 bluetooth gamepad (which works great with the Raspberry Pi).

The XBox controllers emulate an XBox 360 gamepad when in wired mode, as does the 8bitdo.

Because of that, any unknown gamepad is mapped as an XBox 360.

If you have another controller that you want to use to control your robot, feel free to submit a PR on [Github](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) with new mappings.

## Troubleshooting

- If you are not able to see a dropdown menu with the name of your controller appear in the **Control** tab, try specifying the `dev_file` attribute to match the exact path to your device.
  You can also try setting `auto_reconnect` to `True`.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
