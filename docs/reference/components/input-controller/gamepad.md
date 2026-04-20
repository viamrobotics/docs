---
title: "gamepad"
linkTitle: "gamepad"
weight: 30
type: "docs"
description: "Reference for the gamepad input-controller model. Linux-supported gamepad as an input controller."
images: ["/icons/components/controller.svg"]
tags: ["input controller", "components"]
aliases:
  - "/components/input-controller/gamepad/"
  - "/reference/components/input-controller/gamepad/"
component_description: "Supports X-box, Playstation, and similar controllers with Linux support."
# SMEs: James
---

Configuring a `gamepad` input controller allows you to use a Linux-supported gamepad as a device to communicate with your machine.
Linux supports most standard gamepads, such as PlayStation or Xbox type game controllers, as well as many joysticks, racing wheels, and more.

To be able to test your gamepad as you configure it, physically connect your gamepad to your machine's computer and turn both on.

{{< tabs name="Configure a `gamepad` input controller" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name":  "<your-gamepad-input-controller>",
      "model": "gamepad",
      "api": "rdk:component:input_controller",
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `dev_file` | string | Optional | If `dev_file` is left blank or not included, `viam-server` will search and use the first gamepad it finds that's connected to the computer controlling your machine. If you want to specify a device, give the absolute path to the input device event file. For example: `/dev/input/event42`. |
| `auto_reconnect` | boolean | Optional | Applies to both remote (gRPC) and local (Bluetooth or direct USB connected) devices. If set to `true`, `viam-server` tries to (re)connect the device automatically. It waits for a device to connect during a machine's start-up. If set to false (default) then start-up fails if a device is not already connected. |

{{< readfile "/static/include/components/test-control/input-controller-control.md" >}}

## Work in progress models

Mappings are currently available for a wired XBox 360 controller, and wireless XBox Series X|S, along with the 8bitdo Pro 2 Bluetooth gamepad (which works great with the Raspberry Pi).

The XBox controllers emulate an XBox 360 gamepad when in wired mode, as does the 8bitdo.

Because of that, any unknown gamepad is mapped as an XBox 360.

If you have another controller that you want to use to control your machine, feel free to submit a PR on [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/input/input.go) with new mappings.

## Troubleshooting

{{% expand "Not able to see a dropdown menu?" %}}
If you are not able to see a dropdown menu with the name of your controller appear in the **CONTROL** tab, try specifying the `dev_file` attribute to match the exact path to your device.
You can also try setting `auto_reconnect` to `True`.
{{% /expand%}}
