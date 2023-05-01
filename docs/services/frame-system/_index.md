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

To enable the default frame for a given [component](/components), click **Add Frame**, then click **Save Config**.

To adjust the frame from its default configuration, change the parameters as needed for your robot before saving.

{{< tabs name="Frame Configuration Instructions" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab on your robot's page in [the Viam app](https://app.viam.com), select the **Builder** mode, scroll to a component's card, and click **Add Frame**:

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
        "translation": {
          "y": <int>,
          "z": <int>,
          "x": <int>
        },
        "orientation": {
          "type": <"ov_degrees">,
          "value": {
            "x": <int>,
            "y": <int>,
            "z": <int>,
            "th": <int>
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

{{% alert title="Note" color="note" %}}

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

`viam-server` builds a tree of reference frames for your robot with the `world` as the root node and regenerates this tree following reconfiguration.

Access a [topologically-sorted list](https://en.wikipedia.org/wiki/Topological_sorting) of the generated reference frames in the robot's logs at `--debug` level:

![an example of a logged frame system](img/frame_sys_log_example.png)

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

*Supplemental Transforms* exist to help the Frame System determine the location of and relationships between objects not initially known to the robot.

For example:

- In our [example of dynamic attachment](/services/frame-system/component-on-dynamic), the arm can be managed by the Frame System without supplemental transforms because the base of the arm is fixed with respect to the gantry's platform, and the gantry's origin is fixed with respect to the `world` reference frame (centered at `(0, 0, 0)` in the robot's coordinate system).

    However, an arm with an attached [camera](/components/camera) might generate additional information about the poses of other objects with respect to references frames on the robot.

    With the [Vision Service](/services/vision/), the camera might detect objects that do not have a relationship to a `world` reference frame.

    If a [camera](/components/camera) is looking for an apple or an orange, the arm can be commanded to move to the detected fruit's location by providing a supplemental transform that contains the detected pose with respect to the camera that performed the detection.

    The detecting component (camera) would be fixed with respect to the `world` reference frame, and would supply the position and orientation of the detected object.

    With this information, the Frame System could perform the right calculations to express the pose of the object in the `world` reference frame.

Usage:

- You can pass a detected object's frame information to the `supplemental_transforms` parameter in your calls to Viam's Motion Service's [`GetPose`](/services/motion/#getpose) method.
- Functions of some services and components also take in a `WorldState` parameter, which includes a `transforms` property.
- Both [`TransformPose`](#accessing-the-frame-system) and [`FrameSystemConfig`](#accessing-the-frame-system) have the option to take in these supplemental transforms.
