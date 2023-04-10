---
title: "Frame System Configuration for a Component attached to a Static Surface"
linkTitle: "Static Attachment"
description: "How to configure the Frame System in an scenario where a component is attached to a static surface."
type: docs
weight: 45
tags: ["frame system", "services"]
# SMEs: Peter L, Gautham, Bijan
---

### Component Attached to a Static Surface

Imagine a robotic [arm](/components/arm) is attached to a table.
Consider one corner of the table the arm is attached to to be the origin of the `"world"`.
Measure from that point to the *base* of the arm to get the `"translation"` coordinates.

In this case, let's pretend the arm is offset from the corner by 100mm in the positive X direction, and 250mm in the negative Y direction.

We will use the default orientation for the arm, which is the vector (0,0,1) with theta being 0.
Note: because we are using the default orientation, it is optional in the JSON configuration (we are including it for illustrative purposes).

We supply this frame information when configuring the arm component, making sure that the parent is "world".

{{< tabs name="Example Frame Configuration of Component attached to Static Surface" >}}
{{< tab name="Config Builder" >}}

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "depends_on": [],
      "name": "myArm",
      "type": "arm",
      "model": "ur5e",
      "attributes": {
        "host": "127.0.0.1"
      },
      "frame": {
        "parent": "world",
        "translation": {
          "x": 100,
          "y": -250,
          "z": 0
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
