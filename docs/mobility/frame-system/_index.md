---
title: "The Robot Frame System"
linkTitle: "Frame System"
description: "The frame system holds reference frame information for the relative position of components in space."
type: docs
weight: 10
no_list: true
icon: true
images: ["/services/icons/frame-system.svg"]
tags: ["frame system", "services"]
aliases:
  - /services/frame-system/
# SMEs: Peter L, Gautham, Bijan
---

Any machine configured in Viam comes with the frame system service: an internally managed and mostly static system for storing the "reference frame" of each component of a machine within a coordinate system configured by the user.

![Visualization of a wheeled base configured with motors and a mounted camera in the frame system tab of the Viam app UI](/mobility/frame-system/frame_system_wheeled_base.png)

The frame system is the basis for some of Viam's other services, like [motion](/mobility/motion/) and [vision](/ml/vision/).
It stores the required contextual information to use the position and orientation readings returned by some components.

## Used with

{{< cards >}}
{{< relatedcard link="/components/arm/">}}
{{< relatedcard link="/components/base/">}}
{{< relatedcard link="/components/board/">}}
{{< relatedcard link="/components/camera/">}}
{{< relatedcard link="/components/gantry/">}}
{{< relatedcard link="/components/motor/">}}
{{< /cards >}}

## Configuration

You can configure a reference frame within the frame system for each of your machine's components on the **Frame** subtab of the **CONFIGURE** tab or in the raw **JSON** configuration.

{{< tabs name="Frame Configuration Instructions" >}}
{{% tab name="Frame Editor" %}}

1. Navigate to the **CONFIGURE** tab of the machine's page in [the Viam app](https://app.viam.com) and select the **Frame** mode.
2. From the left-hand menu, select your component.
   If you haven't adjusted any parameters yet, the default reference frame will be shown for the component:

   {{<imgproc src="/mobility/frame-system/frame_card.png" resize="300x" style="max-width: 500px" alt="Frame card for a camera with the default reference frame settings">}}

3. To adjust the frame from its default configuration, change the parameters as needed for your machine before saving.
   Select a **Parent** frame and fill in the coordinates for **Translation** (_mm_) and **Orientation** (_deg_, _rad_, or _q_), according to the position and orientation of your component in relation to the **Parent** frame.

4. Select **Save** in the top right corner of the page to save your config.

{{% /tab %}}
{{% tab name="JSON Editor" %}}

1. Navigate to the **CONFIGURE** tab of the machine's page in [the Viam app](https://app.viam.com) and select the **JSON** mode.
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
| Parameter | Inclusion | Required |
| --------- | ----------- | ----- |
| `parent`  | **Required** | Default: `world`. The name of the reference frame you want to act as the parent of this frame. |
| `translation` | **Required** | Default: `(0, 0, 0)`. The coordinates that the origin of this component's reference frame has within its parent reference frame. <br> Units: _mm_. |
| `orientation`  | **Required** | Default: `(0, 0, 1), 0`. The [orientation vector](/internals/orientation-vector/) that yields the axes of the component's reference frame when applied as a rotation to the axes of the parent reference frame. <br> Types: **Orientation Vector Degrees** (`ov_degrees`), **Orientation Vector Radians** (`ov_radians`), **Euler Angles** (`euler_angles`), and **Quaternion** (`quaternion`). |
| `geometry`  | Optional | Default: `none`. Collision geometries for defining bounds in the environment of the machine. <br> Units: _mm_ <br> Types: **Sphere** (`sphere`), **Box** (`box`), and **Capsule** (`capsule`). |

{{% alert title="Info" color="info" %}}

The `orientation` parameter offers types for ease of configuration, but the frame system always stores and returns [orientation vectors](/internals/orientation-vector/) in `Orientation Vector Radians`.
Other types will be converted to `ov_radian`.

{{% /alert %}}

{{% alert title="Tip" color="tip" %}}

For [base components](/components/base/), Viam considers `+X` to be to the right, `+Y` to be forwards, and `+Z` to be up.
You can use [the right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule) to understand rotation about any of these axes.

For non base components, there is no inherent concept of "forward," so it is up to the user to define frames that make sense in their application.

{{% /alert %}}

For more information about determining the appropriate values for these parameters, see these two examples:

- [A Reference Frame:](/mobility/frame-system/frame-config/) A component attached to a static surface
- [Nested Reference Frames:](/mobility/frame-system/nested-frame-config/) A component attached to another, dynamic, component

### Visualize the frame system

You can visualize how your machine is oriented in the frame system in [the Viam app](https://app.viam.com).
Navigate to the **CONFIGURE** tab on your machine's page and select the **Frame** mode.

The Viam app shows you a 3D visualization of the spatial configuration of the reference frames of components configured on your machine:

![Default frame system configuration grid visualization for a single component, shown in the Frame System Editor](/mobility/frame-system/frame_system_basic.png)

On this tab, you can simultaneously view and edit the position, orientation, and geometries of your machine's components in the frame system.

For example:

Consider a machine configured with a [`jetson` board](/components/board/), wired to a [`webcam` camera](/components/camera/webcam/) and a [`wheeled` base](/components/base/wheeled/) with two [motors](/components/motor/) driving its wheels.

No reference frame configuration has been specified, so on the **Frame** subtab of the **CONFIGURE** tab, the components are shown to all be located on the default `world` origin point as follows:

![Example machine's default frame configuration shown in the Frame System Editor. All components are stuck on top of each other](/mobility/frame-system/demo_base_unedited.png)

The distance on the floor from the wheeled base to the board and camera setup is 200 millimeters.

Add this value to `"x"` in the base's reference frame `Translation` attribute, and the frame system readjusts to show the base's translation:

![Base translated 200mm forwards shown in the Frame System Editor](/mobility/frame-system/demo_base_edited.png)

The distance from the board to the camera mounted overhead is 50 millimeters.

Add this value to `"z"` in the camera's reference frame `Translation` attribute, and the frame system readjusts to show the camera's translation:

![Camera translated 50 mm overhead shown in the Frame System Editor](/mobility/frame-system/demo_camera_edited_1.png)

Now the distance between these components is accurately reflected in the visualization.
However, the camera doesn't yet display as oriented towards the base.

Adjust the [orientation vector](/internals/orientation-vector/) to 0.5 degrees in `"ox"` in the camera's reference frame `Orientation` attribute, and the frame system readjusts to show the camera's orientation:

![Camera oriented .5 degrees OX shown in the Frame System Editor](/mobility/frame-system/demo_camera_edited_2.png)

Now that the frame system is accurately configured with the machine's spatial orientation, [motion service](/mobility/motion/) methods that take in reference frame information can be utilized.

### Display options

Click and drag on the **Frame** visualization to view the display from different angles, and pinch to zoom in and out:

{{<gif webm_src="/mobility/frame-system/frame_system_demo.webm" mp4_src="/mobility/frame-system/frame_system_demo.mp4" alt="The frame system visualization zooming in and out around the example robot with a camera, board, and wheeled base.">}}

Click the grid icons below and to the right of the **Frame** button or press the **C** key to switch beween the default **perspective** and the **orthographic** view:

{{< tabs name="Toggle Camera Views" >}}
{{% tab name="Perspective" %}}

![Default Perspective Camera view shown in the Frame System Editor](/mobility/frame-system/demo_perspective.png)

{{% /tab %}}
{{% tab name="Orthographic" %}}

![Orthographic Camera view shown in the Frame System Editor](/mobility/frame-system/demo_orthographic.png)

{{% /tab %}}
{{< /tabs >}}

### Bounding geometries

To visualize a component's spatial constraints, add `geometry` properties by selecting a component and selecting a **Geometry** type in the **Frame** subtab of the **CONFIGURE** tab of a machine's page on [the Viam app](https://app.viam.com).

By default, a **Geometry** is shown surrounding the origin point of a component.
You can adjust the parameters of a **Geometry** to change its size.
Parameters vary between **Geometry** types, but units are in _mm_.

{{< tabs name="Visualize Adding Geometry Bounds" >}}
{{% tab name="Box" %}}

![Demo robot with default box bounds added to the wheeled base, shown in the Frame System Editor](/mobility/frame-system/demo_bound_box.png)

For example:

![Demo robot with translated box bounds added to the wheeled base, shown in the Frame System Editor](/mobility/frame-system/demo_bound_box_translation.png)

{{< /tab >}}
{{% tab name="Sphere" %}}

![Demo robot with default sphere bounds added to the wheeled base, shown in the Frame System Editor](/mobility/frame-system/demo_bound_sphere.png)

{{% /tab %}}
{{% tab name="Capsule" %}}

![Demo robot with default capsule bounds added to the wheeled base, shown in the Frame System Editor](/mobility/frame-system/demo_bound_capsule.png)

{{% /tab %}}
{{< /tabs >}}

## How the frame system works

`viam-server` builds a tree of reference frames for your machine with the `world` as the root node and regenerates this tree following reconfiguration.

Access a [topologically-sorted list](https://en.wikipedia.org/wiki/Topological_sorting) of the generated reference frames in the machine's logs at `--debug` level:

![an example of a logged frame system](/mobility/frame-system/frame_sys_log_example.png)

Consider the example of nested reference frame configuration where [two dynamic components are attached](/mobility/frame-system/nested-frame-config/): a robotic arm, `A`, attaches to a gantry, `G`, which in turn is fixed in place at a point on the `World` of a table.

The resulting tree of reference frames looks like:

![reference frame tree](/mobility/frame-system/frame_tree.png)

`viam-server` builds the connections in this tree by looking at the `"frame"` portion of each component in the machine's configuration and defining _two_ reference frames for each component:

1. One with the name of the component, representing the actuator or final link in the component's kinematic chain: like `"A"` as the end of an arm.
2. Another representing the origin of the component, defined with the component's name and the suffix _"\_origin"_.

## Access the frame system

The [Robot API](https://github.com/viamrobotics/api/blob/main/proto/viam/robot/v1/robot.proto) supplies the following method to interact with the frame system:

<!-- prettier-ignore -->
| Method Name | Description |
| ----- | ----------- |
| [`TransformPose`](#transformpose) | Transform a pose measured in one reference frame to the same pose as it would have been measured in another. |
<!-- | [`FrameSystemConfig`](#framesystemconfig) | Return a topologically sorted list of all the reference frames monitored by the frame system. | -->

<!--
### FrameSystemConfig

Returns a topologically sorted list of all the reference frames monitored by the frame system. Any [additional transforms](#additional-transforms) are also merged into the tree, sorted, and returned.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `additional_transforms` (Optional[List[[viam.proto.common.Transform](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)]]): A list of [additional transforms](#additional-transforms).

**Returns:**

- `frame_system` (List[[viam.proto.robot.FrameSystemConfig](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.FrameSystemConfig)]): The configuration of a given robot’s frame system.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_frame_system_config).

```python {class="line-numbers linkable-line-numbers"}
# Get a list of each of the reference frames configured on the machine.
frame_system = await robot.get_frame_system_config()
print(f"Frame System Configuration: {frame_system}")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `additionalTransforms` (Optional[[referenceframe.LinkInFrame](https://pkg.go.dev/go.viam.com/rdk/referenceframe#LinkInFrame)]): A list of [additional transforms](#additional-transforms).

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- `framesystemparts` [(`framesystemparts.Parts`)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): The individual parts that make up a machine's frame system.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
// Print the Frame System configuration
frameSystem, err := robot.FrameSystemConfig(context.Background(), nil)
fmt.Println(frameSystem)
```

{{% /tab %}}
{{< /tabs >}}
-->

### TransformPose

Transform a given source pose from the reference frame to a new specified destination reference frame.
For example, if a 3D camera observes a point in space you can use this method to calculate where that point is relative to another object.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `query` [(`PoseInFrame`)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame): The pose that should be transformed.
- `destination` (str): The name of the reference frame to transform the given pose to.
- `additional_transforms` (Optional[List[[Transform](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)]]): A list of [additional transforms](#additional-transforms).

**Returns:**

- `PoseInFrame` [(PoseInFrame)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame): Transformed pose in destination reference frame.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.transform_pose).

```python {class="line-numbers linkable-line-numbers"}
# Transform a pose into the frame of myArm
first_pose = Pose(x=0.0, y=0.0, z=0.0, o_x=0.0, o_y=0.0, o_z=1.0, theta=0.0)
first_pif = PoseInFrame(reference_frame="world", pose=first_pose)
transformed_pif = await robot.transform_pose(first_pif, "myArm")
print("Position: (x:", transformed_pif.pose.x,
      ", y:", transformed_pif.pose.y,
      ", z:", transformed_pif.pose.z, ")")
print("Orientation: (o_x:", transformed_pif.pose.o_x,
      ", o_y:", transformed_pif.pose.o_y,
      ", o_z:", transformed_pif.pose.o_z,
      ", theta:", transformed_pif.pose.theta, ")")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `pose` ([[PoseInFrame](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame)]): The pose that should be transformed.
- `dst` (string): The name of the reference frame to transform the given pose to.
- `additionalTransforms` (Optional[[LinkInFrame](https://pkg.go.dev/go.viam.com/rdk/referenceframe#LinkInFrame)]): A list of [additional transforms](#additional-transforms).

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- `PoseInFrame` [(referenceframe.PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): Transformed pose in destination reference frame.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot).

```go {class="line-numbers linkable-line-numbers"}
// Define a Pose coincident with the world reference frame
firstPose := spatialmath.NewPoseFromPoint(r3.Vector{X: 0.0, Y: 0.0, Z: 0.0})

// Establish the world as the reference for firstPose
firstPoseInFrame := referenceframe.NewPoseInFrame(referenceframe.World, firstPose)

// Calculate firstPoseInFrame from the perspective of the origin frame of myArm
transformedPoseInFrame, err := machine.TransformPose(context.Background(), firstPoseInFrame, "myArm", nil)
```

{{% /tab %}}
{{< /tabs >}}

## Additional transforms

_Additional transforms_ exist to help the frame system determine the location of and relationships between objects not initially known to the machine.

For example:

- In our [example of nested dynamic attachment](/mobility/frame-system/nested-frame-config/), the arm can be managed by the frame system without additional transforms because the base of the arm is fixed with respect to the gantry's platform, and the gantry's origin is fixed with respect to the `world` reference frame (centered at `(0, 0, 0)` in the machine's coordinate system).

  However, an arm with an attached [camera](/components/camera/) might generate additional information about the poses of other objects with respect to references frames on the machine.

  With the [vision service](/ml/vision/), the camera might detect objects that do not have a relationship to a `world` reference frame.

  If a [camera](/components/camera/) is looking for an apple or an orange, the arm can be commanded to move to the detected fruit's location by providing an additional transform that contains the detected pose with respect to the camera that performed the detection.

  The detecting component (camera) would be fixed with respect to the `world` reference frame, and would supply the position and orientation of the detected object.

  With this information, the frame system could perform the right calculations to express the pose of the object in the `world` reference frame.

Usage:

- You can pass a detected object's frame information to the `supplemental_transforms` parameter in your calls to Viam's motion service's [`GetPose`](/mobility/motion/#getpose) method.
- Functions of some services and components also take in a `WorldState` parameter, which includes a `transforms` property.
- [`TransformPose`](#access-the-frame-system) has the option to take in these additional transforms.
