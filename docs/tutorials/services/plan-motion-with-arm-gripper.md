---
title: "Plan motion with an arm and gripper"
linkTitle: "Use the motion service"
type: "docs"
weight: 40
description: "Use the motion service to move a robot arm and gripper."
videos:
  [
    "/tutorials/videos/motion_armmoving.webm",
    "/tutorials/videos/motion_armmoving.mp4",
  ]
videoAlt: "An arm moving with the motion service"
tags: ["arm", "gripper", "motion", "services"]
authors: []
languages: ["python", "go"]
viamresources: ["arm", "gripper", "motion", "frame_system"]
platformarea: ["mobility"]
level: "Intermediate"
date: "2023-03-07"
# updated: ""
cost: 8400
no_list: true
aliases:
  - /tutorials/services/plan-motion-with-arm-gripper/
---

With Viam you can move individual components, like [arms](/operate/reference/components/arm/), by issuing commands like `MoveToPosition` or `MoveToJointPosition`.
The [motion service](/operate/reference/services/motion/) enables you to do much more sophisticated movement involving one or many components of your robot.
The service abstracts the lower-level commands away so that instead of passing in a series of joint positions, you can call the `Move()` command with the desired destination and any obstacles, and the service will move your machine to the desired location for you.

{{< alert title="Learning Goals" color="info" >}}
After following this tutorial, you will be able to:

- provide a representation of objects in the world to Viam
- use the motion service to move machines or components of your machine

{{< /alert >}}

Code examples in this tutorial use a [UFACTORY xArm 6](https://www.ufactory.us/product/ufactory-xarm-6), but you can use any [arm model](/operate/reference/components/arm/).

The [full code](#full-code) is available at the end of this page.

{{< alert title="Caution" color="caution" >}}
Be careful when instructing robot arms to move.
Before running any code, ensure your robotic arm has enough space and that there are no obstacles.
Also pay attention to your surroundings, double-check your code for correctness, and make sure anyone nearby is aware and alert before issuing commands to your robot.
{{< /alert >}}

## Prerequisites

Before starting this tutorial, make sure you have the [Viam Python SDK](https://python.viam.dev/) or the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme) installed.

If you are connecting to a real robotic arm during this tutorial, make sure your computer can communicate with the controller before continuing.

Make sure you have followed these steps to configure an arm and a gripper.

1. [Configure an Arm](/operate/mobility/move-arm/)
2. [Configure your frame system](/operate/mobility/move-arm/frame-how-to/)
3. [Configure components attached to your arm](/operate/mobility/move-arm/configure-additional/)

## Configure a robot

Use the robot configuration from the [prerequisite guide](/operate/mobility/move-arm/) for this tutorial as well.
We will revisit that robot configuration and add new components.

The motion service is one of the "built-in" services, which means that no initial configuration is required to start planning and executing complex motion.
All you need is a robot with a component that can move, such as a robotic arm.

## Access the motion service

Accessing the motion service is very similar to accessing any other component or service within the Viam ecosystem.

{{< tabs >}}
{{% tab name="Python" %}}
You must import an additional Python library to access the motion service.
Add the following line to your import list:

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.plan-motion-include.py" lang="py" class="line-numbers linkable-line-numbers" >}}

Then add the sample code below to your client script:

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.motion-service-from-robot.py" lang="py" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{% tab name="Go" %}}
You must import an additional Go package to access the motion service.
Add the following line to your import list:

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.plan-motion-include.go" lang="go" class="line-numbers linkable-line-numbers" >}}

Then add the sample code below to your client script:

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.motion-service-from-robot.go" lang="go" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{< /tabs >}}

The Motion service has a method that can get the _pose_ of a component relative to a [_reference frame_](/operate/reference/services/frame-system/).
In the tutorial where we interacted with an arm component, we used the `GetEndPosition` method to determine the pose of the end effector of `myArm`.
The `GetPose` method provided by the motion service serves a similar function to `GetEndPosition`, but allows for querying of pose data with respect to other elements of the robot (such as another component or the robot's fixed "world" frame).

{{< tabs >}}
{{% tab name="Python" %}}
Note the use of a hardcoded literal "world" in the following code example.
Any components that have frame information (and, as a result, are added to the frame system) are connected to the "world".

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.get-pose.py" lang="py" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{% tab name="Go" %}}
When you use the [arm API](/dev/reference/apis/components/arm/#api), you call methods on your arm component itself.
To use the [motion service API](/dev/reference/apis/services/motion/#api) with an arm, you need to pass an argument of type `ResourceName` to the motion service method.

Add the following to the section of your code where you access the arm:

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.arm-resource-name-from-robot.go" lang="go" class="line-numbers linkable-line-numbers" >}}

Now you are ready to run a motion service method on your arm.

Note the use of `referenceframe.World` in the following code example.
This is a constant string value in the RDK's `referenceframe` library that is maintained for user and programmer convenience.
Any components that have frame information (and, as a result, are added to the frame system) are connected to the "world".

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.get-pose.go" lang="go" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{< /tabs >}}

In this example, we are asking the motion service where the end of `arm-1` is with respect to the root "world" reference frame.

## Describe the robot's working environment

The motion service can also use information you provide about the environment around a robot.
The world around a robot may be full of objects that you may wish to prevent your robot from running into when it moves.
There could be many reasons for this: there are places or things in the environment you want the robot to avoid, or you may have mounted your robot to a fixed object, such as a table.

You can pass additional information about the environment to various parts of the Viam system through a particular data structure, aptly named `WorldState`.
The code samples below detail how to add geometry to the WorldState to indicate the presence of other objects in your robot's working environment.

{{< tabs >}}
{{% tab name="Python" %}}
The `WorldState` is available through the `viam.proto.common` library, but additional geometry data must be added in a piecewise fashion.
You must add additional imports to access `Pose`, `PoseInFrame`, `Vector3`, `Geometry`, `GeometriesInFrame`, and `RectangularPrism` from the proto `common` library.

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.world-state-from-robot.py" lang="py" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{% tab name="Go" %}}
You must import the r3 package to be able to add an `r3.Vector`, so add `"github.com/golang/geo/r3"` to your import list.
The `WorldState` is available through the `referenceframe` library, but additional geometry data must be added in a piecewise fashion.

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.world-state-from-robot.go" lang="go" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{< /tabs >}}

This example adds a "table" with the assumption that you mounted your robot arm to an elevated surface.
The 2000 millimeter by 2000 millimeter dimensions ensure that a sufficiently large box is constructed, regardless of the real physical footprint of your mounting surface.
Setting the Z component of the origin to -19 mm (half the table's thickness) conveniently positions the top surface of the table at 0.
Feel free to change these dimensions, including thickness (the Z coordinate in the above code samples), to match your environment more closely.
Additional obstacles can also be _appended_ as desired.

## Command an arm to move with the motion service

In previous examples you controlled motion of individual components.
Now you will use the motion service to control the motion of the robot as a whole.
You will use the motion service's [`Move`](/dev/reference/apis/services/motion/#move) method to execute more general robotic motion.
You can designate specific components for motion planning by passing in the resource name (note the use of the arm resource in the code samples below).
The `worldState` we constructed earlier is also passed in so that the motion service takes that information into account when planning.

The sample pose given below can be adjusted to fit your specific circumstances.
Remember that X, Y, and Z coordinates are specified in millimeters.

Again, a note:

{{< alert title="Caution" color="caution" >}}
Executing code presented after this point _will_ induce motion in a connected robotic arm!
Keep the space around the arm clear!
{{< /alert >}}
<br><br>
{{< tabs >}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.move-to-pose.py" lang="py" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.move-to-pose.go" lang="go" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{< /tabs >}}

<!-- TODO : In the future, we should add some specific information on the importance of the frame chosen as the point of reference for PoseInFrame variables -->
<!-- ## Managing Pose References -->

## Command other components to move with the motion service

In this section you will add a new component to your machine.
One device that is very commonly attached to the end of a robot arm is a [_gripper_](/operate/reference/components/gripper/).
Most robot arms pick up and manipulate objects in the world with a gripper, so learning how to directly move a gripper is very useful.
Though various motion service commands cause the gripper to move, ultimately the arm is doing all of the work in these situations.
This is possible because the motion service considers other components of the robot (through the [frame system](/operate/reference/services/frame-system/)) when calculating how to achieve the desired motion.

### Add a gripper component

We need to do several things to prepare a new gripper component for motion.

1. Go back to your machine configuration on [Viam](https://app.viam.com).
2. Navigate to the **Components** tab and click **Create component** in the lower-left corner to add a new gripper component to your robot:
   - Select `gripper` for the type and `fake` for the model.
   - Enter `gripper-1` for the name of your gripper component.
   - Click **Create**.
3. Add a **Frame** to the gripper component:
   - Set the parent as `arm-1`.
   - Set the translation as something small in the +Z direction, such as `90` millimeters.
   - Leave the orientation as the default.
   - For **Geometry Type** choose **Box**.
   - Enter desired values for the box's **Length**, **Width**, and **Height**, and the box origin's **X**, **Y**, and **Z** values.
4. Include the `arm-1` component in the **Depends On** dropdown for `gripper-1`.
5. Save this new machine configuration.
   - Your `viam-server` instance should update automatically.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/motion/plan_03_gripper_config.png" resize="700x" declaredimensions=true alt="Sample gripper configuration with several fields filled out.">}}
</div>

Because the new gripper component is "attached" (with the parent specification in the Frame) to `arm-1`, we can produce motion plans using `gripper-1` instead of `arm-1`.

{{< tabs >}}
{{% tab name="Python" %}}

Add this code to your `main()`:

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.move-gripper-to-pose.py" lang="py" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{% tab name="Go" %}}
Add the following line to your import list:

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.gripper-resource-name-from-robot.go" lang="go" class="line-numbers linkable-line-numbers" >}}

Then add this code to your `main()`:

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper-samples.snippet.move-gripper-to-pose.go" lang="go" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{< /tabs >}}

For the gripper pose, you can change the reference frame information to consider other objects or user-generated frames that exist in the frame system.
Specifying other reference frames is an easy way to move with respect to those frames.
For example, you can specify a pose that is 100 millimeters above the table obstacle featured earlier in this tutorial.
You do not need to calculate that exact pose with respect to the **arm** or **world**.
You must only provide the object name (instead of the `gripperName` you saw in the code samples above) when making the `PoseInFrame` to pass into the `Move` function.
This has implications for how motion is calculated, and what final configuration your robot will rest in after moving.

## Next steps

If you would like to continue onto working with Viam's motion service, check out one of these tutorials:

{{< cards >}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{% card link="/tutorials/services/constrain-motion/" %}}
{{< /cards >}}

{{< snippet "social.md" >}}

## Full code

{{< tabs >}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper.snippet.plan-motion-arm-gripper-full.py" lang="py" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/plan-motion-arm-gripper.snippet.plan-motion-arm-gripper-full.go" lang="go" class="line-numbers linkable-line-numbers" >}}

{{% /tab %}}
{{< /tabs >}}
