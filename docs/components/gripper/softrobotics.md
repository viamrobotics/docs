---
title: "Configure a Soft Robotics Gripper"
linkTitle: "softrobotics"
weight: 10
type: "docs"
description: "Configure a Soft Robotics gripper."
---

The `softrobotics` model supports the [Soft Robotics *m*Grip](https://www.softroboticsinc.com/products/mgrip-modular-gripping-solution-for-food-automation/) gripper.

{{< tabs name="Configure a softrobotics gripper" >}}
{{% tab name="Config Builder" %}}

On the **COMPONENTS** sub-tab of your robot's page in the [Viam app](https://app.viam.com/), navigate to the **Create Component** menu.
Enter a name for your gripper, select the type `gripper`, and select the `softrobotics` model.

![Creation of a softrobotics gripper component in the Viam app config builder.](../../img/gripper/softrobotics-builder.png)

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
                "open": <>,
                "close": <>,
                "power": <>
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
                        "pin": "0"
                    }
                ]
            }
        },
        {
            "name": "my_gripper",
            "type": "gripper",
            "model" : "softrobotics",
            "attributes": {
                "open": "40",
                "close": "38",
                "power": "36"
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
`open` | **Required** | string | The pin number of the [board](../../board/) pin wired to the open pin on the gripper controller.
`close` | **Required** | string | The pin number of the [board](../../board/) pin wired to the close pin on the gripper controller.
`power` | **Required** | string | The pin number of the [board](../../board/) pin wired to the enable pin on the gripper controller.

You'll also need to configure a [board component](../../board/) to control the pressure and to wire the controller pins to.
