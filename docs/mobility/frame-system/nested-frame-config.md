---
title: "Nested Reference Frame Configuration"
linkTitle: "Configure Nested Reference Frames"
description: "How to configure the Frame System in an scenario where a component is attached to another component."
type: docs
weight: 50
tags: ["frame system", "services"]
aliases:
  - /services/frame-system/nested-frame-config/
# SMEs: Peter L, Gautham, Bijan
---

Imagine a robotic [arm](/build/configure/components/arm/) is attached to the actuator (moving part) of a [gantry](/build/configure/components/gantry/).

Consider the point that the gantry itself is fixed to as the center of the `world`, making the gantry's origin the same as the `world` origin: `(0, 0, 0)`.

Measure from that point to the base of the arm to get the `translation` of the arm.

- Suppose the base of the arm is mounted to the gantry 100mm above the gantry's origin.
- Supply this `translation` and specify the arm's `parent` reference frame as `myGantry`.
- Leave all other frames' `orientation` and `translation` at their default values.

Now, as the gantry moves its actuator, the Frame System will translate both the gantry and the arm's location according to that motion.

{{< tabs name="Example Frame Configuration of Component attached to Dynamic Component" >}}
{{% tab name="Config Builder" %}}

To complete the frame configuration for your robot following this example, navigate to the **Config** tab on your robot's page in [the Viam app](https://app.viam.com), select the **Builder** mode, scroll to `myGantry`'s card, and click **Add Frame**:

![gantry frame card example for this configuration](/mobility/frame-system/frame_card_dyn_gantry.png)

Select the `parent` frame as `world` and fill in the coordinates for `translation` (_mm_) and `orientation` (_deg_) according to the position and orientation of the gantry in relation to the `world` frame's origin.

Navigate to `myArm`'s card and click **Add Frame**:

![arm frame card example for this configuration](/mobility/frame-system/frame_card_dyn_arm.png)

Select the `parent` frame as `myGantry` and fill in the coordinates for `translation` (_mm_) and `orientation` (_deg_) according to the position and orientation of the arm in relation to the `myGantry` frame's origin.

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
| Parameter | Inclusion | Required |
| --------- | ----------- | ----- |
| `Parent`  | **Required** | Default: `world`. The name of the reference frame you want to act as the parent of this frame. |
| `Translation` | **Required** | Default: `(0, 0, 0)`. The coordinates that the origin of this component's reference frame has within its parent reference frame. <br> Units: _mm_. |
| `Orientation`  | **Required** | Default: `(0, 0, 1), 0`. The [orientation vector](/internals/orientation-vector/) that yields the axes of the component's reference frame when applied as a rotation to the axes of the parent reference frame. <br> Types: `Orientation Vector Degrees`, `Orientation Vector Radians`, and `Quaternion`. |
| `Geometry`  | Optional | Default: `none`. Collision geometries for defining bounds in the environment of the robot. <br> Types: `Sphere`, `Box`, and `Capsule`. |

{{% alert title="Tip" color="tip" %}}

Note: `myGantry` uses the default translation and orientation from the `world` origin, and `myArm` uses the default orientation.

You do not have to explicitly configure this on your robot, as it is the default.
It is included as part of this example for illustrative purposes.

{{% /alert %}}
