---
title: "Frame System Configuration for a Component attached to a Dynamic Component"
linkTitle: "Configure a Component on a Dynamic Component"
description: "How to configure the Frame System in an scenario where a component is attached to another component."
type: docs
weight: 50
tags: ["frame system", "services"]
# SMEs: Peter L, Gautham, Bijan
---

Imagine a robotic [arm](/components/arm) is attached to the actuator (moving part) of a [gantry](/components/gantry).

Consider the point that the gantry itself is fixed to as the center of the `"world"`, making the gantry's origin the same as the `"world"` origin: `(0, 0, 0)`.

Measure from that point to the base of the arm to get the `"translation"` of the arm.

- Suppose the base of the arm is mounted to the gantry 100mm above the gantry's origin.
- Supply this `"translation"` and specify the arm's `"parent"` reference frame as `"myGantry"`.
- Leave all other frames' `"orientation"` and `"translation"` at their default values.

Now, as the gantry moves its actuator, the Frame System will translate both the gantry and the arm's location according to that motion.

{{< tabs name="Example Frame Configuration of Component attached to Dynamic Component" >}}
{{% tab name="Config Builder" %}}

To complete the frame configuration for your robot following this example, navigate to the **CONFIG** tab on your robot's page in [the Viam app](https://app.viam.com), select the **Builder** mode, scroll to `"myGantry"`'s card, and click **Add Frame**:

![gantry frame card example for this configuration](../img/frame_card_dyn_gantry.png)

Navigate to `"myArm"`'s card and click **Add Frame**:

![arm frame card example for this configuration](../img/frame_card_dyn_arm.png)

{{< /tab >}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "myGantry",
      "type": "gantry",
      "model": "oneaxis",
      "attributes": {},
      "depends_on": [],
      "frame": {
        "parent": "world",
        "translation": {
          "y": 0,
          "z": 0,
          "x": 0
        },
        "orientation": {
          "type": "ov_degrees",
          "value": {
            "x": 0,
            "y": 0,
            "z": 1,
            "th": 0
          }
        }
      }
    },
    {
      "depends_on": [],
      "name": "myArm",
      "type": "arm",
      "model": "ur5e",
      "attributes": {
        "host": "127.0.0.1"
      },
      "frame": {
        "parent": "myGantry",
        "translation": {
          "x": 0,
          "y": 0,
          "z": 100
        },
        "orientation": {
          "type": "ov_degrees",
          "value": {
            "x": 0,
            "y": 0,
            "z": 1,
            "th": 0
          }
        }
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Tip" color="tip" %}}

Note: `"myGantry"` uses the default translation and orientation from the `"world"` origin, and `"myArm"` uses the default orientation.

You do not have to explicitly configure this on your robot, as it is the default.
It is included as part of this example for illustrative purposes.

{{% /alert %}}
