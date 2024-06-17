---
title: "Nested Reference Frame Configuration"
linkTitle: "Configure Nested Reference Frames"
description: "How to configure the Frame System in an scenario where a component is attached to another component."
type: docs
weight: 50
tags: ["frame system", "services"]
aliases:
  - /services/frame-system/nested-frame-config/
  - /mobility/frame-system/nested-frame-config/
# SMEs: Peter L, Gautham, Bijan
---

Imagine a robotic [arm](/components/arm/) is attached to the actuator (moving part) of a [gantry](/components/gantry/).

Consider the point that the gantry itself is fixed to as the center of the `world`, making the gantry's origin the same as the `world` origin: `(0, 0, 0)`.

Measure from that point to the base of the arm to get the `translation` of the arm.

- Suppose the base of the arm is mounted to the gantry 100mm above the gantry's origin.
- Supply this `translation` and specify the arm's `parent` reference frame as `myGantry`.
- Leave all other frames' `orientation` and `translation` at their default values.

Now, as the gantry moves its actuator, the Frame System will translate both the gantry and the arm's location according to that motion.

{{< tabs name="Example Frame Configuration of Component attached to Dynamic Component" >}}
{{% tab name="Frame Editor" %}}

To configure your machine following this example:

- Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
- Select **Builder** mode and [configure your gantry](/components/gantry/#supported-models), then [configure your arm](/components/arm/#supported-models).
  If you don't have a physical gantry or arm, you can use their `fake` models.
- Select the **Frame** mode.
- From the left-hand menu, select your gantry.
- Keep the **Parent** frame as `world` and fill in the coordinates for **Translation** (_mm_) and **Orientation** (_deg_) according to the position and orientation of the gantry in relation to the `world` frame's origin.
  For example, considering the point that the gantry itself is fixed to as the center of the `world` you would leave the gantry's frame at the default configuration:
  {{<imgproc src="/services/frame-system/frame_card_dyn_gantry.png" resize="300x" style="max-width: 500px" alt="Gantry frame card example for this configuration">}}

- Next, select your arm from the left hand menu.
- Select the **Parent** frame as the gantry, and fill in the coordinates for **Translation** (_mm_) and **Orientation** (_deg_) of the arm in relation to the gantry's origin:

  {{<imgproc src="/services/frame-system/frame_card_dyn_arm.png" resize="300x" style="max-width: 500px" alt="Arm frame card example for this configuration">}}

{{< /tab >}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "myGantry",
      "model": "single-axis",
      "type": "gantry",
      "namespace": "rdk",
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
      "model": "ur5e",
      "type": "arm",
      "namespace": "rdk",
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

<!-- prettier-ignore -->
| Parameter | Required? | Required |
| --------- | ----------- | ----- |
| `parent`  | **Required** | Default: `world`. The name of the reference frame you want to act as the parent of this frame. |
| `translation` | **Required** | Default: `(0, 0, 0)`. The coordinates that the origin of this component's reference frame has within its parent reference frame. <br> Units: _mm_. |
| `orientation`  | **Required** | Default: `(0, 0, 1), 0`. The [orientation vector](/internals/orientation-vector/) that yields the axes of the component's reference frame when applied as a rotation to the axes of the parent reference frame. <br> Types: **Orientation Vector Degrees** (`ov_degrees`), **Orientation Vector Radians** (`ov_radians`), **Euler Angles** (`euler_angles`), and **Quaternion** (`quaternion`). |
| `geometry`  | Optional | Default: `none`. Collision geometries for defining bounds in the environment of the machine. <br> Units: _mm_ <br> Types: **Sphere** (`sphere`), **Box** (`box`), and **Capsule** (`capsule`). |
