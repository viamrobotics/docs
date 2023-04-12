---
title: "The Robot Frame System"
linkTitle: "Frame System"
description: "The Frame System holds reference frame information for the relative position of components in space."
type: docs
weight: 45
no_list: true
tags: ["frame system", "services"]
# SMEs: Peter L, Gautham, Bijan
---

Any robot configured in Viam comes with the Frame System service: an internally managed and mostly static system for storing the "reference frame" of each component of a robot within a coordinate system configured by the user.

The Frame System is the basis for many of Viam's other services, like [Motion](/services/motion) and [Vision](/services/vision).
It stores the required contextual information to use the position and orientation readings returned by some components.

## Configuration

To adjust the Frame System from its default configuration for a particular [component](/components), add the following to its configuration:

{{< tabs name="Frame Configuration Instructions" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIG** tab on your robot's page in [the Viam app](https://app.viam.com), select the **Builder** mode, scroll to a component's card, and click **Add Frame**:

![add reference frame pane](img/frame_card.png)

Select a `parent` frame and fill in the coordinates for `translation` (*mm*) and `orientation` (*deg*, *rad*, or *q*), according to the position and orientation of your component in relation to the `parent` frame.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <"your_component_name_1">,
      "type": <"your_component_type_1">,
      "model": <"your_component_model_1">,
      "attributes": { ... },
      "depends_on": [],
      "frame": {
        "parent": <"world">,
        // default
        "translation": {
          "y": 0,
          "z": 0,
          "x": 0
        },
        // default
        "orientation": {
          "type": <"ov_degrees">,
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
      "name": <"your_component_name_2">,
      "type": <"your_component_type_2">,
      "model": <"your_component_model_2">,
      "attributes": { ... },
      "frame": {
        "parent": <"your_component_name_1">,
        // default
        "translation": {
          "x": 0,
          "y": 0,
          "z": 0
        },
        // default
        "orientation": {
          "type": <"ov_degrees">,
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

Configure the reference frame as follows:

| Parameter | Inclusion | Required |
| --------- | ----------- | ----- |
| `Parent`  | **Required** | Default: `world`. The name of the reference frame you want to act as the parent of this frame. |
| `Translation` | **Required** | Default: `(0, 0, 0)`. The coordinates that the origin of this component's reference frame has within its parent reference frame. <br> Units: *mm*. |
| `Orientation`  | **Required** | Default: `(0, 0, 1), 0`. The [orientation vector](/internals/orientation-vector/) that yields the axes of the component's reference frame when applied as a rotation to the axes of the parent reference frame. <br> Types: `Orientation Vector Degrees`, `Orientation Vector Radians`, and `Quaternion`. |
| `Geometry`  | Optional | Default: `none`. Collision geometries for defining bounds in the environment of the robot. <br> Types: `Sphere`, `Box`, and `Capsule`. |

{{% alert title="Caution" color="caution" %}}

The `Orientation` parameter offers `Types` for ease of configuration, but the Frame System always stores and returns [orientation vectors](/internals/orientation-vector/) in `"Orientation Vector Radians"`.
`"Degrees"` and `"Quaternion"` will be converted to `"Radians"`.

{{% /alert %}}

{{% alert title="Tip" color="tip" %}}

Viam's coordinate system considers `+X` to be forward, `+Y` to be left, and `+Z` to be up.
You can use [the right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule) to determine the orientation of these axes.

{{% /alert %}}

For more information about determining the appropriate values for these parameters, see these two examples:

- [A component attached to a static surface](/services/frame-system/component-on-static)
- [A component attached to another, dynamic, component](/services/frame-system/component-on-dynamic)

## Building the Frame System

Access a [topologically-sorted list](https://en.wikipedia.org/wiki/Topological_sorting) of the generated reference frames in the robot's logs at `--debug` level:

![an example of a logged frame system](img/frame_sys_log_example.png)

`viam-server` builds a tree of reference frames for your robot with the `world` as the root node and regenerates this tree following reconfiguration.

Consider the example of a [component attached to a dynamic component](/services/frame-system/component-on-dynamic): a robotic arm, `A`, attached to a gantry, `G`, which in turn is fixed in place at a point on the `World` of a table.

The resulting tree of reference frames looks like:

![reference frame tree](img/frame_tree.png)

`viam-server` builds the connections in this tree by looking at the `"frame"` portion of each component in the robot's configuration and defining *two* reference frames for each component:

1. One with the name of the component, representing the actuator or final link in the component's kinematic chain: like `"A"` as the end of an arm.
2. Another representing the origin of the component, defined with the component's name and the suffix *"_origin"*.

## Accessing the Frame System

The [Robot API](https://github.com/viamrobotics/api/blob/main/proto/viam/robot/v1/robot.proto) supplies two methods to interact with the Frame System through gRPC calls:

1. `TransformPose`: Transforms a pose measured in one reference frame to the same pose as it would have been measured in another.
2. `FrameSystemConfig`: Returns a topologically sorted list of all the reference frames monitored by the frame system.
Any [supplemental transforms](#supplemental-transforms) are also merged into the tree, topologically sorted, and returned.

## Supplemental Transforms

*Supplemental transforms* exist to compensate for the fact that the Frame System built for a robot only knows how to coordinate the location of components that are fixed to a point in space, allowing them to have a fixed origin in reference to a `world` reference frame with a fixed origin of `(0, 0, 0)`.

In our [example of dynamic attachment](/services/frame-system/component-on-dynamic), the arm can be managed by the Frame System without supplemental transforms because the base of the arm is fixed with respect to the gantry's platform, and the gantry's origin is fixed with respect to the `world` reference frame.

However, a dynamic arm attached to a [dynamic rover](/components/base/wheeled) could not be configured into the Frame System if the rover is unaware of its own position, because the rover can move freely with respect to the `world` reference frame.

To solve this problem:

- You can introduce a [movement sensor](/components/movement-sensor) or a [camera](/components/camera), in combination with our [Vision Service](/services/vision/), as a third component.
- This component would be fixed in respect to the `world` reference frame, and could supply the location and orientation of the rover in its own reference frame.

To add this component's reference frame into your robot's Frame System build, you can pass the `name` of this component's reference frame to various APIs.
These *supplemental transforms* then supply the missing link to transform a [pose](/internals/orientation-vector) in that dynamic arm's reference frame to the `world` reference frame.

- For example, you can pass this component's reference frame information to the `supplemental_transforms` parameter in your calls to Viam's motion service [`GetPose`](/services/motion/#getpose) method.
- Functions of some services and components also take in a `WorldState` parameter, which includes a `transforms` parameter.
- Both [`TransformPose`](#accessing-the-frame-system) and [`FrameSystemConfig`](#accessing-the-frame-system) have the option to take in these supplemental transforms.

{{% alert title="Tip" color="tip" %}}

Experienced users can code a [mobile base](/components/base/wheeled) that is able to report its own position without the need for supplemental transforms with an organic [SLAM](/services/slam) system.

{{% /alert %}}
