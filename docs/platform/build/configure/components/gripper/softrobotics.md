---
title: "Configure a Soft Robotics Gripper"
linkTitle: "softrobotics"
weight: 30
type: "docs"
description: "Configure a Soft Robotics gripper."
images: ["/icons/components/gripper.svg"]
aliases:
  - "/components/gripper/softrobotics/"
---

The `softrobotics` model supports the [Soft Robotics *m*Grip](https://www.softroboticsinc.com/uploads/2021/03/Soft_Robotics_ModularGripping_800129_RevD_LR.pdf) gripper controlled by the [Soft Robotics *co*Drive Control Unit](https://www.softroboticsinc.com/uploads/2020/05/Tech_Sheet_coDrive_Control_Unit_-__TS-200210_Rev_B.pdf).

{{< tabs name="Configure a softrobotics gripper" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `gripper` type, then select the `softrobotics` model.
Enter a name for your gripper and click **Create**.

![Creation of a softrobotics gripper component in the Viam app config builder.](/platform/build/configure/components/gripper/softrobotics-ui-config.png)

Copy and paste the following attribute template into your gripper's **Attributes** box.
Then remove and fill in the attributes as applicable to your gripper, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "<your-board-name>",
  "open": "<pin-number-on-board>",
  "close": "<pin-number-on-board>",
  "power": "<pin-number-on-board>",
  "analog_reader": "psi"
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "local",
  "open": "11",
  "close": "13",
  "power": "15",
  "analog_reader": "psi"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-gripper-name>",
      "model": "softrobotics",
      "type": "gripper",
      "namespace": "rdk",
      "attributes": {
        "board": "<your-board-name>",
        "open": "<pin-number-on-board>",
        "close": "<pin-number-on-board>",
        "power": "<pin-number-on-board>",
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
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
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
      "model": "softrobotics",
      "type": "gripper",
      "namespace": "rdk",
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

<!-- prettier-ignore -->
| Name            | Inclusion    | Type   | Description                                                                                                                                                                                    |
| --------------- | ------------ | ------ | -------- |
| `board`         | **Required** | string | The `name` of the [board](/platform/build/configure/components/board/) to which your gripper [control unit](https://www.softroboticsinc.com/uploads/2020/05/Tech_Sheet_coDrive_Control_Unit_-__TS-200210_Rev_B.pdf) is wired. |
| `open`          | **Required** | string | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the board pin wired to the open pin (D1) on the gripper controller.                                                     |
| `close`         | **Required** | string | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the board pin wired to the close pin (D2) on the gripper controller.                                                    |
| `power`         | **Required** | string | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the board pin wired to the enable pin (D3) on the gripper controller.                                                   |
| `analog_reader` | **Required** | string | Must be called `"psi"`. You must [configure an analog](/platform/build/configure/components/board/#analogs) on your board and name it `"psi"`.                                                                                |

{{< readfile "/static/include/components/test-control/gripper-control.md" >}}
