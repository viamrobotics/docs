---
title: "Reference Frame Configuration"
linkTitle: "Configure a Reference Frame"
description: "How to configure the frame system in an scenario where a component is fixed to a static object."
type: docs
weight: 45
tags: ["frame system", "services"]
aliases:
  - /services/frame-system/frame-config/
# SMEs: Peter L, Gautham, Bijan
---

Imagine a robotic [arm](/components/arm/) is attached to a table.

Consider one corner of the table the arm is attached to to be the origin of the `world`, `(0, 0, 0)`.
Measure from that point to the base of the arm to get the `translation` coordinates.

- Suppose the arm is offset from the corner by 100mm in the positive X direction, and 250mm in the negative Y direction.
- Supply this `translation` when configuring the arm component's `frame` information.
- Leave `parent` and `orientation` at their default values.

{{< tabs name="Example Frame Configuration of Component attached to Static Surface" >}}
{{% tab name="Config Builder" %}}

To complete the frame configuration for your robot following this example, navigate to the **Config** tab on your robot's page in [the Viam app](https://app.viam.com), select the **Builder** mode, scroll to `myArm`'s card, and click **Add Frame**:

![frame card example for this configuration](/mobility/frame-system/frame_card_static.png)

Select the `parent` frame as `world` and fill in the coordinates for `translation` (_mm_) and `orientation` (_deg_) according to the position and orientation of the arm in relation to the `world` frame's origin.

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
| Parameter | Inclusion | Required |
| --------- | ----------- | ----- |
| `Parent`  | **Required** | Default: `world`. The name of the reference frame you want to act as the parent of this frame. |
| `Translation` | **Required** | Default: `(0, 0, 0)`. The coordinates that the origin of this component's reference frame has within its parent reference frame. <br> Units: _mm_. |
| `Orientation`  | **Required** | Default: `(0, 0, 1), 0`. The [orientation vector](/internals/orientation-vector/) that yields the axes of the component's reference frame when applied as a rotation to the axes of the parent reference frame. <br> Types: `Orientation Vector Degrees`, `Orientation Vector Radians`, and `Quaternion`. |
| `Geometry`  | Optional | Default: `none`. Collision geometries for defining bounds in the environment of the robot. <br> Types: `Sphere`, `Box`, and `Capsule`. |

{{% alert title="Tip" color="tip" %}}

Note: `myArm` uses the default `orientation` from the `world` origin.

You do not have to explicitly configure this on your robot, as it is the default.
It is included as part of this example for illustrative purposes.

{{% /alert %}}
