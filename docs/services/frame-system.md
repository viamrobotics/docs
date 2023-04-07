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

In this page, we will explain:

* How to configure a robot's components to make use of the Frame System in different contexts
* How `viam-server` builds the frame system
* How to access and use reference frame information from the Frame System

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

The information mathematically operates in the following way.
Let P be the parent's coordinate system and C be the component's coordinate system.
To get the coordinates in P of the vector (0,0,1) as measured in C, we apply the translation and orientation (as a rotation) to the vector (0,0,1) as measured in P.

* Viam recommends that you mark a sensible origin point in the physical space in which your robot will operate. For example, the corner of a table the robot is on.
  * This will be the origin point (`{0, 0, 0}`) of the `parent` reference frame.
* Measure from this point to a point on the component guaranteed to be fixed to some point in the `parent` reference frame.
  * This will be the origin point of this component in reference to its parent "world" or component frame.
* With those two origin points in mind, you can calculate the `Translation` and `Orientation` information for each component.

{{% alert title="Tip" color="tip" %}}

Viam's coordinate system considers `+X` to be forward, `+Y` to be left, and `+Z` to be up.

{{% /alert %}}

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

In our [example of a dynamic arm attached to a dynamic gantry](#component-attached-to-a-dynamic-component), the arm could managed by the Frame System without supplemental transforms because the base of the arm is fixed with respect to the gantry's platform, and the gantry's origin is fixed with respect to the `world` reference frame.

On the other hand, an arm attached to a [rover](/components/base/wheeled) that is unaware of its own position cannot be configured into the frame system because the rover can move freely with respect to the world frame.
A knowledgeable user could code a mobile base with an organic SLAM system able to report its own position without the need for supplementary transforms.

How do we deal with such components?
One solution would be to introduce a motion tracker or a camera in combination with our [Vision Service](/services/vision/) as a third component.
This component is fixed in space (making it configurable in the Frame System) and can supply the location and orientation of the rover in its own reference frame.
This *supplemental transform* is the missing link to be able to transform a pose in the arm's reference frame to the world reference frame (or others that may exist in the frame system).

Both TransformPose and FrameSystemConfig optionally take in these supplemental transforms.

Functions of some services and components take in a WorldState parameter (like `ArmMoveToPosition`).
This data structure includes an entry for supplying supplemental transforms for use by internal calls to the Frame System.

## Reference

### Model Configuration

Many components are non-trivial kinematic chains and require an additional set of intermediate reference frames.
For example, a traditional arm may have a reference frame whose origin is at its base, but it also has an alternating sequence of links and joints whose frames of reference matter when attempting to move the arm to a certain pose.
Each driver of such a component in the Viam system requires a JSON file named **Model JSON** that details the attachment of reference frames.
However, that is a requirement for Viam's drivers.
If you implement your own drivers, the decision whether to require Model JSON files will depend on your code.
These reference frames are ingested by the Frame System, but not exposed through gRPC calls. You cannot access them directly with SDK code.

{{% alert title="Note" color="note" %}}
If you are using a component driver provided by Viam, the **Model JSON** should come pre-packaged.
Otherwise, please refer to the [**Model JSON** section](#model-json).
{{% /alert %}}

Viam uses model files written in JSON, similar to the URDF files used in ROS.
JSON files are better suited for use in Python environments.

### Model JSON

As explained in the [Model Configuration](#model-configuration) section, some components use an additional **Model JSON** file to specify reference frame information about the kinematic chain of the component to the Frame System.

When writing a driver for a particular piece of hardware that implements one of these components, you must create its accompanying **Model JSON** file.

{{% alert title="Note" color="note" %}}
There is currently (15 Sept 2022) no user interface in the Viam app (<a href="https://app.viam.com">app.viam.com</a>) by which to create these files.
{{% /alert %}}

Furthermore, only our Go implementation supports creation of custom **Model JSON** files (15 Sept 2022) as a way if ingesting kinematic parameters is provided in our Go repository.
Native support for specifying kinematic parameters of arms is not yet supported in the Python SDK."

This means that a user will fork our [repository](https://github.com/viamrobotics/rdk), create one of these files in that fork, and then use it to build the package for running the server.

We currently support two methods of supplying reference frame parameters for a kinematic chain:

1. [Spatial Vector Algebra (SVA)](https://drake.mit.edu/doxygen_cxx/group__multibody__spatial__vectors.html) - supplying reference frame information for each link and each joint.
2. [Denavit-Hartenberg (DH)](https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters) parameters.

Of the two methods, Viam prefers Spacial Vector Algebra over Denavit-Hartenberg.

Viam wants roboticists to be able to specify link frames arbitrarily, which DH parameters are unable to guarantee.
We also want roboticists to make their own (messy) robots; accurate identification of DH parameters for a mass-produced robot can be exceedingly difficult.
Furthermore, incorrect SVA parameters are much easier to troubleshoot than incorrect DH parameters.

Below are JSON examples for each parameter type used by our [Universal Robots](https://www.universal-robots.com/) arms driver:

#### Example: kinematic_param_type=SVA

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "UR5e",
    "kinematic_param_type": "SVA",
    "links": [
        {
            "id": "base_link",
            "parent": "world",
            "translation": {
                "x": 0,
                "y": 0,
                "z": 162.5
            },
            "geometry": {
                "x": 120,
                "y": 120,
                "z": 260,
                "translation": {
                  "x": 0,
                  "y": 0,
                  "z": 130
                }
            }
        },
        {
            "id": "shoulder_link",
            "parent": "shoulder_pan_joint",
            "translation": {
                "x": 0,
                "y": 0,
                "z": 0
            }
        },
        {
            "id": "upper_arm_link",
            "parent": "shoulder_lift_joint",
            "translation": {
                "x": -425,
                "y": 0,
                "z": 0
            },
            "geometry": {
                "x": 550,
                "y": 150,
                "z": 120,
                "translation": {
                    "x": -215,
                    "y": -130,
                    "z": 0
                }
            }
        },
        {
            "id": "forearm_link",
            "parent": "elbow_joint",
            "translation": {
                "x": -392.2,
                "y": 0,
                "z": 0
            },
            "geometry": {
                "x": 480,
                "y": 120,
                "z": 100,
                "translation": {
                    "x": -190,
                    "y": 0,
                    "z": 0
                }
            }
        },
        {
            "id": "wrist_1_link",
            "parent": "wrist_1_joint",
            "translation": {
                "x": 0,
                "y": -133.3,
                "z": 0
            },
            "geometry": {
                "x": 90,
                "y": 130,
                "z": 130,
                "translation": {
                    "x": 0,
                    "y": -110,
                    "z": 0
                }
            }
        },
        {
            "id": "wrist_2_link",
            "parent": "wrist_2_joint",
            "translation": {
                "x": 0,
                "y": 0,
                "z": -99.7
            },
            "geometry": {
                "x": 80,
                "y": 150,
                "z": 100,
                "translation": {
                    "x": 0,
                    "y": 0,
                    "z": -100
                }
            }
        },
        {
            "id": "ee_link",
            "parent": "wrist_3_joint",
            "translation": {
                "x": 0,
                "y": -99.6,
                "z": 0
            },
            "orientation": {
                "type" : "ov_degrees",
                "value" : {
                    "x": 0,
                    "y": -1,
                    "z": 0,
                    "th": 90
                }
            }
        }
    ],
    "joints": [
        {
            "id": "shoulder_pan_joint",
            "type": "revolute",
            "parent": "base_link",
            "axis": {
                "x": 0,
                "y": 0,
                "z": 1
            },
            "max": 360,
            "min": -360
        },
        {
            "id": "shoulder_lift_joint",
            "type": "revolute",
            "parent": "shoulder_link",
            "axis": {
                "x": 0,
                "y": -1,
                "z": 0
            },
            "max": 360,
            "min": -360
        },
        {
            "id": "elbow_joint",
            "type": "revolute",
            "parent": "upper_arm_link",
            "axis": {
                "x": 0,
                "y": -1,
                "z": 0
            },
            "max": 180,
            "min": -180
        },
        {
            "id": "wrist_1_joint",
            "type": "revolute",
            "parent": "forearm_link",
            "axis": {
                "x": 0,
                "y": -1,
                "z": 0
            },
            "max": 360,
            "min": -360
        },
        {
            "id": "wrist_2_joint",
            "type": "revolute",
            "parent": "wrist_1_link",
            "axis": {
                "x": 0,
                "y": 0,
                "z": -1
            },
            "max": 360,
            "min": -360
        },
        {
            "id": "wrist_3_joint",
            "type": "revolute",
            "parent": "wrist_2_link",
            "axis": {
                "x": 0,
                "y": -1,
                "z": 0
            },
            "max": 360,
            "min": -360
        }
    ]
}
```

#### Example: kinematic_param_type=DH

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "UR5e",
    "kinematic_param_type": "DH",
    "dhParams": [
        {
            "id": "base",
            "parent": "world",
            "a": 0,
            "d": 162.5,
            "alpha": 1.57079632679,
            "max": 360,
            "min": -360
        },
        {
            "id": "shoulder",
            "parent": "base",
            "a": -425,
            "d": 0,
            "alpha": 0,
            "max": 360,
            "min": -360
        },
        {
            "id": "elbow",
            "parent": "shoulder",
            "a": -392.2,
            "d": 0,
            "alpha": 0,
            "max": 180,
            "min": -180
        },
        {
            "id": "wrist_1",
            "parent": "elbow",
            "a": 0,
            "d": 133.3,
            "alpha": 1.57079632679,
            "max": 360,
            "min": -360
        },
        {
            "id": "wrist_2",
            "parent": "wrist_1",
            "a": 0,
            "d": 99.7,
            "alpha": -1.57079632679,
            "max": 360,
            "min": -360
        },
        {
            "id": "wrist_3",
            "parent": "wrist_2",
            "a": 0,
            "d": 99.6,
            "alpha": 0,
            "max": 360,
            "min": -360
        }
    ]
}
```
