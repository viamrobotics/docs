---
linkTitle: "Define machine geometry"
title: "Define a machine’s geometry"
weight: 10
layout: "docs"
type: "docs"
description: "Specify your robot's dimensions and how it is positioned in space."
---

Before you can use the motion planning or navigation with your machine, you need to create a description of your machine's dimensions and how it is positioned relative to its surroundings.
The position and orientation readings returned by a component such as an accelerometer or a robot arm have no meaning without a reference frame.

Use Viam's frame system to define a coordinate system for your machine, and configure the geometries of your machine's components.
You can also [define static obstacles](/operate/mobility/define-obstacles/) for your machine to avoid.

{{% alert title="Note" color="note" %}}
For complex kinematic chain configuration, useful when creating a module to support an unsupported arm model, see [Configure Complex Kinematic Chains](/operate/reference/kinematic-chain-config/).
{{% /alert %}}

{{<imgproc src="/services/frame-system/frame_system_wheeled_base.png" resize="x1100" declaredimensions=true alt="Visualization of a wheeled base configured with motors and a mounted camera in the frame system tab of the Viam app UI" style="max-width:600px" class="imgzoom" >}}

## Configure a reference frame

Imagine you have a robotic [arm](/operate/reference/components/arm/) attached to a table.

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
- Select the **Frame** mode.
- From the left-hand menu, select your arm:
  {{<imgproc src="/services/frame-system/arm_default_frame.png" resize="500x" style="width: 300px" alt="Frame card for an arm with the default reference frame settings">}}
- Keep the **Parent** frame as `world` and fill in the coordinates for **Translation** (meters) and **Orientation** (degrees) according to the position and orientation of the arm in relation to the `world` frame's origin:
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

### Configure nested reference frames

Imagine you have a robotic arm attached to the actuator (moving part) of a [gantry](/operate/reference/components/gantry/).

Using a nested reference frame allows you to define the reference frame of the arm with respect to the end effector of the gantry.
This allows `viam-server` to correctly calculate the position of the end of the arm, taking into account the combined motion of the gantry and the arm.

1. Decide that the origin of the gantry and the origin of the `world` frame will be the same point.
   Pick a point on the stationary portion of the gantry and define it as `(0,0,0)`.
1. Pick a point on the gantry end effector where the arm is mounted, with the gantry end effector in what you consider to be the home position.
   This is the origin `(0,0,0)` of the arm reference frame.
1. Measure between these two points.
   For example, if the arm origin is 10 centimeters above the gantry/world origin, the translation is (0.00, 0.00, 0.10).
1. Configure the gantry reference frame and the arm reference frame according to the instructions in the section above, but set the `parent` of the arm as the gantry, and supply the translation you measured.

{{< tabs >}}
{{% tab name="Frame Editor" %}}

- Since the gantry and world have the same origin, don't configure a translation between them:

  {{<imgproc src="/services/frame-system/frame_card_dyn_gantry.png" resize="500x" style="width: 300px" alt="Gantry frame card example for this configuration">}}

- Next, select your arm from the left hand menu.
- Select the **Parent** frame as the gantry, and fill in the coordinates for **Translation** (m) of the arm in relation to the gantry's origin:

  {{<imgproc src="/services/frame-system/frame_card_dyn_arm.png" resize="500x" style="width: 300px" alt="Arm frame card example for this configuration">}}

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
