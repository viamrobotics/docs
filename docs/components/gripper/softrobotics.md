---
title: "Configure a Soft Robotics Gripper"
linkTitle: "softrobotics"
weight: 10
type: "docs"
description: "Configure a Soft Robotics gripper."
images: ["/components/img/components/gripper.svg"]
---

The `softrobotics` model supports the [Soft Robotics *m*Grip](https://www.softroboticsinc.com/products/mgrip-modular-gripping-solution-for-food-automation/) gripper controlled by the [Soft Robotics *co*Drive Control Unit](https://www.softroboticsinc.com/uploads/2020/05/Tech_Sheet_coDrive_Control_Unit_-__TS-200210_Rev_B.pdf).

{{< tabs name="Configure a softrobotics gripper" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** sub-tab and navigate to the **Create component** menu.

Enter a name for your gripper, select the type `gripper`, and select the `softrobotics` model.

![Creation of a softrobotics gripper component in the Viam app config builder.](../../img/gripper/softrobotics-builder.png)

Click **Create component** and then fill in the attributes for your model.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "components": [
        {
            "name": <gripper_name>,
            "type": "gripper",
            "model" : "softrobotics",
            "attributes": {
                "board": <board_name>,
                "open": <pin_number>,
                "close": <pin_number>,
                "power": <pin_number>,
                "analog_reader": "psi"
            }
        }
    ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "components": [
        {
            "name": "local",
            "type": "board",
            "model": "pi",
            "attributes": {
                "analogs": [
                    {
                        "name": "psi",
                        "pin": "32"
                    }
                ]
            }
        },
        {
            "name": "my_gripper",
            "type": "gripper",
            "model" : "softrobotics",
            "attributes": {
                "board": "local",
                "open": "11",
                "close": "13",
                "power": "15",
                "analog_reader": "psi"
            }
        }
    ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `softrobotics` grippers:

Name | Inclusion | Type | Description
---- | --------- | ---- | -----------
`board` | **Required** | string | The name of the [board](../../board/) to which your gripper [control unit](https://www.softroboticsinc.com/uploads/2020/05/Tech_Sheet_coDrive_Control_Unit_-__TS-200210_Rev_B.pdf) is wired.
`open` | **Required** | string | The pin number of the board pin wired to the open pin (D1) on the gripper controller.
`close` | **Required** | string | The pin number of the board pin wired to the close pin (D2) on the gripper controller.
`power` | **Required** | string | The pin number of the board pin wired to the enable pin (D3) on the gripper controller.
`analog_reader` | **Required** | string | Needs to be called `"psi"`, and you need to configure an [analog](../../board/#analogs) named `"psi"` on your board.
