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
no_service: true
date: "2022-01-01"
updated: "2024-10-18"
# SMEs: Peter L, Gautham, Bijan
---

The frame system is the basis for some of Viam's other services, like [motion](/operate/reference/services/motion/) and [vision](/data-ai/reference/vision/).
It stores the required contextual information to use the position and orientation readings returned by some components.

It is a mostly static system for storing the "reference frame" of each component of a machine within a coordinate system configured by the user.

![Visualization of a wheeled base configured with motors and a mounted camera in the frame system tab of the Viam app UI](/services/frame-system/frame_system_wheeled_base.png)

## Used with

{{< cards >}}
{{< relatedcard link="/operate/reference/components/arm">}}
{{< relatedcard link="/operate/reference/components/base/">}}
{{< relatedcard link="/operate/reference/components/camera/">}}
{{< relatedcard link="/operate/reference/components/gantry/">}}
{{< /cards >}}

## Configuration

You can configure a reference frame within the frame system for each of your machine's components on the **Frame** subtab of the **CONFIGURE** tab or in the raw **JSON** configuration.

{{< tabs name="Frame Configuration Instructions" >}}
{{% tab name="Frame Editor" %}}

1. Navigate to the **CONFIGURE** tab of the machine's page in the [Viam app](https://app.viam.com) and select the **Frame** mode.
2. From the left-hand menu, select your component.
   If you haven't adjusted any parameters yet, the default reference frame will be shown for the component:

   {{<imgproc src="/services/frame-system/frame_card.png" resize="300x" style="width: 250px" alt="Frame card for a camera with the default reference frame settings">}}

3. To adjust the frame from its default configuration, change the parameters as needed for your machine before saving.
   Select a **Parent** frame and fill in the coordinates for **Translation** (m) and **Orientation** (deg, rad, or q), according to the position and orientation of your component in relation to the **Parent** frame.
   Optionally add a **Geometry**.

4. Select **Save** in the top right corner of the page to save your config.

{{% /tab %}}
{{% tab name="JSON Editor" %}}

1. Navigate to the **CONFIGURE** tab of the machine's page in the [Viam app](https://app.viam.com) and select the **JSON** mode.
2. Edit the JSON inside your component object to add a `"frame"` configuration.

{{< tabs >}}
{{% tab name="JSON Template" %}}

You can add a reference frame to your component with the following template:

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
      "namespace": "rdk",
      "type": "camera",
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

{{% /tab %}}
{{< /tabs >}}

Configure the reference frame as follows:

<!-- prettier-ignore -->
| Parameter | Required? | Required |
| --------- | ----------- | ----- |
| `parent`  | **Required** | Default: `world`. The name of the reference frame you want to act as the parent of this frame. |
| `translation` | **Required** | Default: `(0, 0, 0)`. The coordinates that the origin of this component's reference frame has within its parent reference frame. <br> Units: m in Frame Editor, mm in JSON. |
| `orientation`  | **Required** | Default: `(0, 0, 1), 0`. The [orientation vector](/operate/reference/orientation-vector/) that yields the axes of the component's reference frame when applied as a rotation to the axes of the parent reference frame. <br> Types: **Orientation Vector Degrees** (`ov_degrees`), **Orientation Vector Radians** (`ov_radians`), **Euler Angles** (`euler_angles`), and **Quaternion** (`quaternion`). |
| `geometry`  | Optional | Default: `none`. Collision geometries for defining bounds in the environment of the machine. <br> Units: m in Frame Editor, mm in JSON. <br> Types: **Sphere** (`sphere`), **Box** (`box`), and **Capsule** (`capsule`). |

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

### Visualize the frame system

You can visualize how your machine is oriented in the frame system in the [Viam app](https://app.viam.com).
Navigate to the **CONFIGURE** tab on your machine's page and select the **Frame** mode.

The Viam app shows you a 3D visualization of the spatial configuration of the reference frames of components configured on your machine:

![Default frame system configuration grid visualization for a single component, shown in the Frame System Editor](/services/frame-system/frame_system_basic.png)

On this tab, you can simultaneously view and edit the position, orientation, and geometries of your machine's components in the frame system.

For example:

Consider a machine configured with a [board](/operate/reference/components/board/) wired to a [camera](/operate/reference/components/camera/webcam/) and a [`wheeled` base](/operate/reference/components/base/wheeled/).

You have not specified any reference frame configuration, so on the **Frame** subtab of the **CONFIGURE** tab, the components are shown to all be located on the default `world` origin point as follows:

![Example machine's default frame configuration shown in the Frame System Editor. All components are stuck on top of each other](/services/frame-system/demo_base_unedited.png)

The distance on the floor from the wheeled base to the board and camera setup is 0.2 meters.

Add this value to `"x"` in the base's reference frame `Translation` attribute, and the frame system readjusts to show the base's translation:

![Base translated 0.2 m forwards shown in the Frame System Editor](/services/frame-system/demo_base_edited.png)

The distance from the board to the camera mounted overhead is 0.05 meters.

Add this value to `"z"` in the camera's reference frame `Translation` attribute, and the frame system readjusts to show the camera's translation:

![Camera translated 0.05 m overhead shown in the Frame System Editor](/services/frame-system/demo_camera_edited_1.png)

Now the distance between these components is accurately reflected in the visualization.
However, the camera doesn't yet display as oriented towards the base.

Adjust the [orientation vector](/operate/reference/orientation-vector/) to 0.5 degrees in `"ox"` in the camera's reference frame `Orientation` attribute, and the frame system readjusts to show the camera's orientation:

![Camera oriented 0.5 degrees OX shown in the Frame System Editor](/services/frame-system/demo_camera_edited_2.png)

Now that you have configured the frame system with the machine's spatial orientation, you can use [motion service](/operate/reference/services/motion/) methods that take in reference frame information.

### Geometries

To visualize a component's spatial constraints, add `geometry` properties by selecting a component in the **Frame** editor and selecting a **Geometry**.

A **Geometry** is shown surrounding the origin point of a component.
You can adjust the parameters of a **Geometry** to change its size.
Parameters vary between **Geometry** types, but units are in meters in the editor.

{{< tabs name="Visualize Adding Geometry Bounds" >}}
{{% tab name="Box" %}}

![Demo robot with default box bounds added to the wheeled base, shown in the Frame System Editor](/services/frame-system/demo_bound_box.png)

{{< /tab >}}
{{% tab name="Sphere" %}}

![Demo robot with default sphere bounds added to the wheeled base, shown in the Frame System Editor](/services/frame-system/demo_bound_sphere.png)

{{% /tab %}}
{{% tab name="Capsule" %}}

![Demo robot with default capsule bounds added to the wheeled base, shown in the Frame System Editor](/services/frame-system/demo_bound_capsule.png)

{{% /tab %}}
{{< /tabs >}}

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

For example:

- In our [example of nested dynamic attachment](/operate/mobility/define-geometry/#configure-nested-reference-frames), the arm can be managed by the frame system without additional transforms because the base of the arm is fixed with respect to the gantry's platform, and the gantry's origin is fixed with respect to the `world` reference frame (centered at `(0, 0, 0)` in the machine's coordinate system).

  However, an arm with an attached [camera](/operate/reference/components/camera/) might generate additional information about the poses of other objects with respect to references frames on the machine.

  With the [vision service](/data-ai/reference/vision/), the camera might detect objects that do not have a relationship to a `world` reference frame.

  If a [camera](/operate/reference/components/camera/) is looking for an apple or an orange, the arm can be commanded to move to the detected fruit's location by providing an additional transform that contains the detected pose with respect to the camera that performed the detection.

  The detecting component (camera) would be fixed with respect to the `world` reference frame, and would supply the position and orientation of the detected object.

  With this information, the frame system could perform the right calculations to express the pose of the object in the `world` reference frame.

Usage:

- You can pass a detected object's frame information to the `supplemental_transforms` parameter in your calls to Viam's motion service's [`GetPose`](/dev/reference/apis/services/motion/#getpose) method.
- Functions of some services and components also take in a `WorldState` parameter, which includes a `transforms` property.
- [`TransformPose`](/dev/reference/apis/robot/#transformpose) has the option to take in these additional transforms.
