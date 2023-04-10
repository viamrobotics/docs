---
title: "Frame System Configuration for a Component attached to a Dynamic Component"
linkTitle: "Dynamic Attachment"
description: "How to configure the Frame System in an scenario where a component is attached to a dynamic surface."
type: docs
weight: 50
tags: ["frame system", "services"]
# SMEs: Peter L, Gautham, Bijan
---

### Component Attached to a Dynamic Component

Imagine a robotic [arm](/components/arm) is attached to the actuator (moving part) of a [gantry](components/gantry).

Here, the point that the gantry itself is fixed to can be considered to be the center of the `"world"`.
That means the gantry's origin is the same as the `"world"` origin: `{0, 0, 0}`.

After configuring the gantry's `"frame"` with `"parent": "world"` and the default `"translation"` and `"orientation"`, you can configure the arm to use the gantry's frame as its parent.

The base of the arm is mounted to the gantry 100 mm above the gantry's origin of `{0, 0, 0}`.

Knowing this, all you need to do to configure the frames of the components together is specify the arm's parent as the name of the gantry and translate the arm's `"frame"` `100` on the `"z"` axis. After adjusting the arm's `"translation"`, you can leave all other frames' `"orientation"` and `"translation"` at their default values.

Now, as the gantry moves its actuator, the Frame System will translate both the gantry and the arm's location according to that motion.

{{< tabs name="Example Frame Configuration of Component attached to Dynamic Component" >}}
{{< tab name="Config Builder" >}}

{{< /tab >}}
{{% tab name="Raw JSON" %}}

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

Note: `"myGantry"` uses the default translation, `{0, 0, 0}` from the `"world"` origin.

You do not have to explicitly configure this on your robot, as it is the default.
It is included as part of this example for illustrative purposes.

{{% /alert %}}
