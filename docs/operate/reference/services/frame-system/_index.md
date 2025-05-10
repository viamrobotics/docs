---
title: "The Robot Frame System"
linkTitle: "Frame System"
description: "The frame system holds reference frame information for the relative position of components in space."
type: docs
weight: 50
no_list: true
icon: true
images: ["/services/icons/frame-system.svg"]
tags: ["frame system", "services"]
aliases:
  - /services/frame-system/
  - /mobility/frame-system/
  - /services/frame-system/frame-config/
  - /mobility/frame-system/frame-config/
  - /operate/reference/services/frame-system/frame-config/
no_service: true
date: "2022-01-01"
updated: "2024-10-18"
# SMEs: Peter L, Gautham, Bijan
---

The frame system is the basis for some of Viam's other services, like [motion](/operate/reference/services/motion/) and [vision](/operate/reference/services/vision/).
It stores the required contextual information to use the position and orientation readings returned by some components.

It is a mostly static system for storing the "reference frame" of each component of a machine within a coordinate system configured by the user.

## Used with

{{< cards >}}
{{< relatedcard link="/operate/reference/components/arm">}}
{{< relatedcard link="/operate/reference/components/base/">}}
{{< relatedcard link="/operate/reference/components/camera/">}}
{{< relatedcard link="/operate/reference/components/gantry/">}}
{{< relatedcard link="/operate/reference/components/gripper/">}}
{{< /cards >}}

## Configuration

You can configure a reference frame within the frame system for each of your machine's components on the **Frame** subtab of the **CONFIGURE** tab or in the raw **JSON** configuration.

1. Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).

1. Select **Builder** mode and [configure your arm](/operate/reference/components/arm/#configuration).
   If you don't have a physical arm, you can use a `fake` model.

1. Click **+ Add Frame**.

1. Edit the frame configuration.
   The frame configuration is a JSON object with the following parameters:

<!-- prettier-ignore -->
| Parameter | Required? | Required |
| --------- | ----------- | ----- |
| `parent`  | **Required** | Default: `world`. The name of the reference frame you want to act as the parent of this frame. |
| `translation` | **Required** | Default: `(0, 0, 0)`. The coordinates that the origin of this component's reference frame has within its parent reference frame. <br> Units: m in Frame Editor, mm in JSON. |
| `orientation`  | **Required** | Default: `(0, 0, 1), 0`. The [orientation vector](/operate/reference/orientation-vector/) that yields the axes of the component's reference frame when applied as a rotation to the axes of the parent reference frame. <br> Types: **Orientation Vector Degrees** (`ov_degrees`), **Orientation Vector Radians** (`ov_radians`), **Euler Angles** (`euler_angles`), and **Quaternion** (`quaternion`). |
| `geometry`  | Optional | Default: `none`. Collision geometries for defining bounds in the environment of the machine. <br> Units: m in Frame Editor, mm in JSON. <br> Types: **Sphere** (`sphere`), **Box** (`box`), and **Capsule** (`capsule`). |

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your_component_name_1>",
      "type": "<your_component_type_1>",
      "model": "<your_component_model_1>",
      "attributes": { ... },
      "depends_on": [],
      "frame": {
        "parent": "<world_or_parent_component_name>",
        "translation": {
          "y": <int>,
          "z": <int>,
          "x": <int>
        },
        "orientation": {
          "type": "<type>",
          "value": {
            "x": <int>,
            "y": <int>,
            "z": <int>,
            "th": <int> // "w": <int> if "type": "quaternion"
          }
        },
        "geometry": {
          "type": "<type>",
          "x": <int>,
          "y": <int>,
          "z": <int>
        }
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "cam",
      "api": "rdk:component:camera",
      "model": "webcam",
      "attributes": {
        "video_path": "FDF90FEC-59E5-4FCF-AABD-DA03C4E19BFB"
      },
      "frame": {
        "parent": "world",
        "translation": {
          "x": 0,
          "y": 0,
          "z": 0
        },
        "orientation": {
          "type": "quaternion",
          "value": {
            "x": 0,
            "y": 0,
            "z": 0,
            "w": 1
          }
        },
        "geometry": {
          "type": "box",
          "x": 100,
          "y": 100,
          "z": 100
        }
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Info" color="info" %}}

The `orientation` parameter offers types for ease of configuration, but the frame system always stores and returns [orientation vectors](/operate/reference/orientation-vector/) in `Orientation Vector Radians`.
Other types will be converted to `ov_radian`.

{{% /alert %}}

{{% alert title="Tip" color="tip" %}}

For [base components](/operate/reference/components/base/), Viam considers `+X` to be to the right, `+Y` to be forwards, and `+Z` to be up.
You can use [the right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule) to understand rotation about any of these axes.

For non base components, there is no inherent concept of "forward," so it is up to the user to define frames that make sense in their application.

{{% /alert %}}

For more information about determining the appropriate values for these parameters, see these two examples:

- [A Reference Frame:](/operate/mobility/define-geometry/#configure-a-reference-frame) A component attached to a static surface
- [Nested Reference Frames:](/operate/mobility/define-geometry/#configure-nested-reference-frames) A component attached to another, dynamic, component

## How the frame system works

`viam-server` builds a tree of reference frames for your machine with the `world` as the root node and regenerates this tree following reconfiguration.

Access a [topologically-sorted list](https://en.wikipedia.org/wiki/Topological_sorting) of the generated reference frames in the machine's logs at `--debug` level:

![an example of a logged frame system](/services/frame-system/frame_sys_log_example.png)

Consider the example of nested reference frame configuration where [two dynamic components are attached](/operate/mobility/define-geometry/#configure-nested-reference-frames): a robotic arm, `A`, attaches to a gantry, `G`, which in turn is fixed in place at a point on the `World` of a table.

The resulting tree of reference frames looks like:

![reference frame tree](/services/frame-system/frame_tree.png)

`viam-server` builds the connections in this tree by looking at the `"frame"` portion of each component in the machine's configuration and defining _two_ reference frames for each component:

1. One with the name of the component, representing the actuator or final link in the component's kinematic chain: like `"A"` as the end of an arm.
2. Another representing the origin of the component, defined with the component's name and the suffix _"\_origin"_.

## Access the frame system

The [Machine Management API](/dev/reference/apis/robot/) supplies the following methods to interact with the frame system:

<!-- prettier-ignore -->
| Method Name | Description |
| ----- | ----------- |
| [`FrameSystemConfig`](/dev/reference/apis/robot/#framesystemconfig) | Return a topologically sorted list of all the reference frames monitored by the frame system. |
| [`TransformPose`](/dev/reference/apis/robot/#transformpose) | Transform a given source Pose from the original reference frame to a new destination reference frame. |

## Additional transforms

_Additional transforms_ exist to help the frame system determine the location of and relationships between objects not initially known to the machine.

### Example of additional transforms

Imagine you are using a wall-mounted [camera](/operate/reference/components/camera/) to find objects near your arm.
You can use the [vision service](/operate/reference/services/vision/) with the camera to detect objects and provide the poses of the objects with respect to the camera's reference frame.
The camera is fixed with respect to the `world` reference frame.

If the camera finds an apple or an orange, you can command the arm to move to the detected fruit's location by providing an additional transform that contains the detected pose of the fruit with respect to the camera that performed the detection.

The frame system uses the supplemental transform to determine where the arm should move to pick up the fruit.

### Transform usage

- You can pass a detected object's frame information to the `supplemental_transforms` parameter in your calls to Viam's motion service's [`GetPose`](/dev/reference/apis/services/motion/#getpose) method.
- Functions of some services and components also take in a `WorldState` parameter, which includes a `transforms` property.
- [`TransformPose`](/dev/reference/apis/robot/#transformpose) has the option to take in these additional transforms.
