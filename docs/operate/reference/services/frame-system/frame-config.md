---
title: "Reference Frame Configuration"
linkTitle: "Configure a Reference Frame"
description: "How to configure the frame system in an scenario where a component is fixed to a static object."
type: docs
weight: 45
tags: ["frame system", "services"]
aliases:
  - /services/frame-system/frame-config/
  - /mobility/frame-system/frame-config/
no_service: true
date: "2024-10-18"
updated: "2024-10-18"
# SMEs: Peter L, Gautham, Bijan
---

Imagine a robotic [arm](/operate/reference/components/arm/) is attached to a table.

Consider one corner of the table the arm is attached to be the origin of the `world`, `(0, 0, 0)`.
Measure from that point to the base of the arm to get the `translation` coordinates.

- Suppose the arm is offset from the corner by 0.1 m in the positive X direction, and 0.25 m in the negative Y direction.
- Supply this `translation` when configuring the arm component's `frame` information.
- Leave `parent` and `orientation` at their default values.

{{< tabs name="Example Frame Configuration of Component attached to Static Surface" >}}
{{% tab name="Frame Editor" %}}

To configure your machine following this example:

- Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
- Select **Builder** mode and [configure your arm](/operate/reference/components/arm/#configuration).
  If you don't have a physical arm, you can use a `fake` model.
- Select the **Frame** mode.
- From the left-hand menu, select your arm:
  {{<imgproc src="/services/frame-system/arm_default_frame.png" resize="500x" style="width: 300px" alt="Frame card for an arm with the default reference frame settings">}}
- Keep the **Parent** frame as `world` and fill in the coordinates for **Translation** (m) and **Orientation** (deg) according to the position and orientation of the arm in relation to the `world` frame's origin:
  {{<imgproc src="/services/frame-system/arm_frame.png" resize="500x" style="width: 300px" alt="Frame card for an arm with a translation of 0.1 meters and -0.25 meters configured">}}

{{< /tab >}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "depends_on": [],
      "name": "myArm",
      "model": "ur5e",
      "type": "arm",
      "namespace": "rdk",
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

<!-- prettier-ignore -->
| Parameter | Required? | Required |
| --------- | ----------- | ----- |
| `parent`  | **Required** | Default: `world`. The name of the reference frame you want to act as the parent of this frame. |
| `translation` | **Required** | Default: `(0, 0, 0)`. The coordinates that the origin of this component's reference frame has within its parent reference frame. <br> Units: m in Frame Editor, mm in JSON. |
| `orientation`  | **Required** | Default: `(0, 0, 1), 0`. The [orientation vector](/operate/reference/orientation-vector/) that yields the axes of the component's reference frame when applied as a rotation to the axes of the parent reference frame. <br> **Types**: **Orientation Vector Degrees** (`ov_degrees`), **Orientation Vector Radians** (`ov_radians`), **Euler Angles** (`euler_angles`), and **Quaternion** (`quaternion`). |
| `geometry`  | Optional | Default: `none`. Collision geometries for defining bounds in the environment of the machine. <br> Units: m in Frame Editor, mm in JSON. <br> **Types**: **Sphere** (`sphere`), **Box** (`box`), and **Capsule** (`capsule`). |
