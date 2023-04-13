---
title: "The Robot Frame System"
linkTitle: "Frame System"
description: "The Frame System holds reference frame information for the relative position of components in space."
type: docs
weight: 45
tags: ["frame system", "services"]
# SMEs: Peter L, Gautham, Bijan
---

Any robot configured in Viam comes with a service we call the Frame System: an internally managed and mostly static system for storing the "reference frame" of each component of a robot within a coordinate system configured by the user.

The Frame System is the basis for many of Viam's other services, like [motion](/services/motion) and [vision](/services/vision).
It stores the required contextual information to use the position and orientation readings returned by some components.

## Configuration

To adjust the Frame System from its default configuration for a particular [component](/components), add the following to its configuration:

{{< tabs name="Frame Configuration Instructions" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIG** tab on your robot's page in [the Viam app](https://app.viam.com), select the **Builder** mode, scroll to a component's card, and click **Add Frame**:

![add reference frame pane](../img/frame-card.png)

{{< /tab >}}
{{% tab name="Raw JSON" %}}

{{% /tab %}}
{{< /tabs >}}

Configure the reference frame as follows:

| Parameter | Inclusion | Required |
| --------- | ----------- | ----- |
| `Parent`  | **Required** | Default: `world`. The name of the reference frame you want to act as the parent of this frame. |
| `Translation` | **Required** | Default: `{0, 0, 0}`. The coordinates that the origin of this component's reference frame has within its parent reference frame. |
| `Orientation`  | **Required** | Default: `{0, 0, 1, 0}`. The [orientation vector](/internals/orientation-vector/) that yields the axes of the component's reference frame when applied as a rotation to the axes of the parent reference frame. <br> Types: `Orientation Vector Degrees`, `Orientation Vector Radians`, and `Quaternion`. |
| `Geometry`  | **Required** | Default: `none`. Collision geometries for defining bounds in the environment of the robot. <br> Types: `Sphere` and `Box`. |

{{% alert title="Caution" color="caution" %}}

`Types` are offered in `Orientation` for ease of configuration, but the [orientation vector](/internals/orientation-vector/) type that is always stored and returned by the Frame System is `"Orientation Vector Radians"`.
`"Degrees"` and `"Quaternion"` will be converted to `"Radians"`.

{{% /alert %}}

<!-- The information mathematically operates in the following way.
Let P be the parent's coordinate system and C be the component's coordinate system.
To get the coordinates in P of the vector (0,0,1) as measured in C, we apply the translation and orientation (as a rotation) to the vector (0,0,1) as measured in P.

* Viam recommends that you mark a sensible origin point in the physical space in which your robot will operate. For example, the corner of a table the robot is on.
  * This will be the origin point (`{0, 0, 0}`) of the `parent` reference frame.
* Measure from this point to a point on the component guaranteed to be fixed to some point in the `parent` reference frame.
  * This will be the origin point of this component in reference to its parent "world" or component frame.
* With those two origin points in mind, you can calculate the `Translation` and `Orientation` information for each component. -->

{{% alert title="Tip" color="tip" %}}

Many components are non-trivial kinematic chains and require an additional set of intermediate reference frames.
For example, a traditional arm may have a reference frame whose origin is at its base, but it also has an alternating sequence of links and joints whose frames of reference matter when attempting to move the arm to a certain pose.
Each driver of such a component in the Viam system requires a JSON file named **Model JSON** that details the attachment of reference frames.
However, that is a requirement for Viam's drivers.
If you implement your own drivers, the decision whether to require Model JSON files will depend on your code.
These reference frames are ingested by the Frame System *but not exposed through {{< glossary_tooltip term_id="grpc" text="gRPC" >}} call* (meaning they are unavailable for inspection by any of the SDKs).

{{% /alert %}}

### Component Attached to a Static Surface

Imagine a robotic [arm](/components/arm) is attached to a table.
Consider one corner of the table the arm is attached to to be the origin of the `"world"`.
Measure from that point to the *base* of the arm to get the `"translation"` coordinates.

Once the configuration is completed and the server is started, the robot builds a tree of reference frames with the world as the root node.

A [topologically-sorted list](https://en.wikipedia.org/wiki/Topological_sorting) of the generated reference frames is printed by the server and can be seen in the server logs.
Viam regenerates this tree in the process of [reconfiguration](/manage/fleet/#configuration):

![an example of a logged frame system](../img/frame_sys_log_example.png)

Viam builds this tree by looking at the frame portion of each component in the robot's configuration (including those defined on any remotes) and creating two reference frames.

* One reference frame is given the name of the component and represents the actuator or final link in the component's kinematic chain (for example, the end of an arm, the platform of a gantry, and so on).
* Viam creates an additional static reference frame whose translation and orientation relative to its parent is provided by the user in configuration.
  Viam names this reference frame with the component name and the suffix *"_origin"*.
  For example, "right-arm_<em>origin</em>".

As an example, let's consider an arm on a gantry.

Let our gantry be named "G" and our arm be named "A".
We might decide that the static origin of our gantry is its zero position and specify a translation and orientation with respect to the world frame.
The Frame System considers the reference frame with this static origin to be "G_origin" and the reference frame with its origin being the location of the platform to be "G".
This choice is made so that when we specify the parent frame of the arm, we can simply use "G" and the Frame System will understand that the arm's parent frame is the platform of the gantry and not it's zero position used as a point of reference to the world.
The resulting tree of reference frames could be visualized like so:

![reference frame tree](../img/frame_tree.png)

## Configuration Examples

### Example 1: A robot arm attached to a table (a component fixed to the world frame)

We can consider one corner of the table the origin of the world and measure from that point to the *base* of the arm to get the translation.
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

### Component Attached to a Dynamic Component

* Let the point the gantry is fixed on the table be the origin of the `"world"` frame, with coordinates of `{0, 0, 0}`.
* By calculating the translation and orientation (`G_offset`) of the gantry in respect to its `"World"` Frame, we can define a new reference frame for the gantry itself, `"G"`.
`"G"` has the `"World"` frame as its `"parent"`.
* Then, when we specify the `"parent"` frame of the reference frame of the arm, `"A"`, we can use `"G"`, instead of `"World"`.

Imagine a robotic [arm](/components/arm) is attached to the actuator (moving part) of a [gantry](components/gantry).

Here, the point that the gantry itself is fixed to can be considered to be the center of the `"world"`.
That means the gantry's origin is the same as the `"world"` origin: `{0, 0, 0}`.

After configuring the gantry's `"frame"` with `"parent": "world"` and the default `"translation"` and `"orientation"`, you can configure the arm to use the gantry's frame as its parent.

The base of the arm is mounted to the gantry 100 mm above the gantry's origin of `{0, 0, 0}`.
Knowing this, all you need to do to configure the frames of the components together is specify the arm's parent as the name of the gantry and translate the arm's `"frame"` `100` on the `"z"` axis.

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

## Reference Frame Trees: Building the Frame System

Once you configure your robot and run `viam-server`, your robot will builds a tree of reference frames with the `world` as the root node.

A [topologically-sorted list](https://en.wikipedia.org/wiki/Topological_sorting) of the generated reference frames is printed by the server and can be seen in the server logs:

![an example of a logged frame system](../img/frame_sys_log_example.png)

Viam regenerates this tree in the process of [reconfiguration](/manage/fleet-management/#configurationlogging).

Let's consider the example of a [component attached to a dynamic component](#component-attached-to-a-dynamic-component): a robotic arm, `A`, attached to a gantry, `G`, which in turn is fixed in place at a point on the `World` of a table.

Let's use `G_offset` to refer to the configuration for the translation and orientation of the gantry from its world parent, and `A_offset` to refer to the configuration for the translation and orientation of the arm from its gantry parent.

The resulting tree of reference frames:

![reference frame tree](../img/frame_tree.png)

Viam builds the connections in this tree by looking at the `"frame"` portion of each component in the robot's configuration and defining *two* reference frames for each component:

1. One with the name of the component, representing the actuator or final link in the component's kinematic chain: like `"A"` as the end of an arm.
2. Another representing the origin of the component, defined with the component's name and the suffix *"_origin"*.

For example, in the robot's `viam-server` behind the reference frame tree shown above, the arm would have two reference frames: `"a_origin"` and `"A"`. `"a_origin"` would be the same as `"G"`.

## Accessing the Frame System

The [Robot API](https://github.com/viamrobotics/api/blob/main/proto/viam/robot/v1/robot.proto) supplies two methods to interact with the Frame System through gRPC calls:

1. `TransformPose`: Transforms a pose measured in one reference frame to the same pose as it would have been measured in another.
2. `FrameSystemConfig`: Returns a topologically sorted list of all the reference frames monitored by the frame system.
Any [supplemental transforms](#handling-motion-with-supplemental-transforms) are also merged into the tree, topologically sorted, and returned.

### Handling Motion with Supplemental Transforms

*Supplemental Transforms* exist to compensate for the fact that the Frame System built by a robot only knows how to coordinate the location of components in reference to a `"world"` frame with a fixed origin of `{0, 0, 0}`.

In our [example of a dynamic arm attached to a dynamic gantry](#component-attached-to-a-dynamic-component), the arm could be managed by the Frame System without supplemental transforms because the base of the arm is fixed with respect to the gantry's platform, and the gantry's origin is fixed with respect to the `world` reference frame.

On the other hand, an arm attached to a [rover](/components/base/wheeled) that is unaware of its own position cannot be configured into the frame system because the rover can move freely with respect to the world frame.
A knowledgeable user could code a mobile base with an organic SLAM system able to report its own position without the need for supplementary transforms.

How do we deal with such components?
One solution would be to introduce a motion tracker or a camera in combination with our [Vision Service](/services/vision/) as a third component.
This component is fixed in space (making it configurable in the Frame System) and can supply the location and orientation of the rover in its own reference frame.
This *supplemental transform* is the missing link to be able to transform a pose in the arm's reference frame to the world reference frame (or others that may exist in the frame system).

Both `TransformPose` and `FrameSystemConfig` optionally take in these supplemental transforms.

Functions of some services take in a WorldState parameter (like `motion_service.move(component_name, destination, world_state)`).
This data structure includes an entry for supplying supplemental transforms for use by internal calls to the Frame System.
