---
linkTitle: "How to build a machine"
title: "How to think about building a machine"
weight: 30
layout: "docs"
type: "docs"
images: ["/icons/components.png"]
imageAlt: "Viam building blocks"
description: "Viam works by breaking complex projects into composable building blocks. Your project's complexities become manageable and you gain flexibility."
modulescript: true
aliases:
  - "/tutorials/build-a-mock-robot/"
  - "/tutorials/how-to-build-a-mock-robot/"
  - "/tutorials/configure/build-a-mock-robot/"
date: "2025-10-09"
---

Viam adapts software engineering paradigms to building machines for the physical world.
At its core, Viam works by breaking complex projects into composable building blocks.
With this approach, your project's complexities become manageable, and more importantly, you gain flexibility and testability.

The flexibility means you can, at any point, swap out hardware, change logic, or even switch programming language.

To accomplish this, you must adopt a _modular_ way of thinking.

{{< alert title="You will learn about" color="note" >}}

1. [Identifying the building blocks for your project](#step-1-identify-the-building-blocks)
1. [Starting with a minimal prototype](#step-2-start-with-a-minimal-prototype)
1. [Adding your control logic](#step-3-add-your-control-logic)
1. [Testing and Iterating](#step-4-test-and-iterate)
1. [Considering resource constraints and scaling](#step-5-consider-resource-constraints-and-scaling)
1. [Building a UI](#step-6-build-a-ui)
1. [Scaling and production](#step-7-scaling-and-production)

{{< /alert >}}

This guide will walk you through the high-level process of designing a machine.
At the end of each step of the guide, you'll learn how to apply the step to a fictional example project: the **wood sanding project**.

The following steps will teach you _how to approach_ building machines.
If you are looking to build your first example machine, we recommend you follow the [Desk Safari Tutorial](/operate/hello-world/tutorial-desk-safari/).

## Step 1: Identify the building blocks

When building a project, it's easiest to start by identifying the hardware and software you know you will need.
This will help you determine the main building blocks of your project.

{{< table >}}
{{< tablestep start=1 >}}

<p><strong>Consider the hardware you need.</strong></p>
<p>In Viam, hardware components are <em>components</em>.
To start with the minimum amount of hardware, begin with one robotic arm, one end effector, and one camera.</p>
<p>Review the following list of components and consider which components you may need. If in doubt, click on the component to review its API to understand what the component does.</p>

{{< cards >}}
{{% relatedcard link="/dev/reference/apis/components/arm/" highlight="green" %}}
{{% relatedcard link="/dev/reference/apis/components/base/" %}}
{{% relatedcard link="/dev/reference/apis/components/board/" %}}
{{% relatedcard link="/dev/reference/apis/components/button/" %}}
{{% relatedcard link="/dev/reference/apis/components/camera/" highlight="green" %}}
{{% relatedcard link="/dev/reference/apis/components/encoder/" %}}
{{% relatedcard link="/dev/reference/apis/components/gantry/" %}}
{{% relatedcard link="/dev/reference/apis/components/generic/" %}}
{{% relatedcard link="/dev/reference/apis/components/gripper/" highlight="green" %}}
{{% relatedcard link="/dev/reference/apis/components/input-controller/" %}}
{{% relatedcard link="/dev/reference/apis/components/motor/" %}}
{{% relatedcard link="/dev/reference/apis/components/movement-sensor/" %}}
{{% relatedcard link="/dev/reference/apis/components/power-sensor/" %}}
{{% relatedcard link="/dev/reference/apis/components/sensor/" %}}
{{% relatedcard link="/dev/reference/apis/components/servo/" %}}
{{% relatedcard link="/dev/reference/apis/components/switch/" %}}
{{< /cards >}}

<p><b>Wood sanding project:</b>
Imagine you are building a project to sand wood.
You want to use one or more robotic arms to do the sanding, and cameras or possibly LiDAR to identify where to sand.</p>

<p>The hardware needs for the sanding project can be translated into the following components:</p>
<ul>
<li>one arm</li>
<li>one gripper for the end effector</li>
<li>one camera</li>
</ul>

<p>That covers the hardware for the project.</p>

{{% /tablestep %}}
{{% tablestep %}}
**Consider other components you need.**

Each piece of hardware in a project is a component, but not every component represents a piece of hardware.
Sometimes a component is just software that uses the same API endpoints as a physical component might.

**Wood sanding project:** Let's say you also want a button to start and stop sanding.
You don't need to decide at this point whether the button is physical or software.
For now, let's just add a button component to the list of components for the project.

{{% /tablestep %}}
{{< tablestep >}}

<p><strong>Consider the services you need.</strong></p>
<p>While components mostly operate hardware, <em>services</em> do more complex work such as motion planning or machine learning.
Services often operate on components.</p>
<p>Review the following list of services and consider which services you may need. If in doubt, click on the service to review its API to understand what the service does.</p>

{{< cards >}}
{{% relatedcard link="/dev/reference/apis/services/data/" %}}
{{% relatedcard link="/dev/reference/apis/services/ml/" highlight="green" %}}
{{% relatedcard link="/dev/reference/apis/services/vision/" highlight="green" %}}
{{% relatedcard link="/dev/reference/apis/services/motion/" highlight="green" %}}
{{% relatedcard link="/dev/reference/apis/services/navigation/" %}}
{{% relatedcard link="/dev/reference/apis/services/slam/" %}}
{{% relatedcard link="/dev/reference/apis/services/generic/" %}}
{{% relatedcard link="/dev/reference/apis/services/base-rc/" %}}
{{< /cards >}}

<p><strong>Wood sanding project:</strong> For the software side, you'll want something to identify the areas to sand.
A common technique for sanding is to draw or write something on a piece of wood and then sand until you can no longer see the pencil marks.

To identify where to sand, you can use a vision service that can detect the color of the pencil marks.
Many vision services use a machine learning model, so we may need one as well to support the vision service in identifying where to sand.

For moving the arm, you can use the motion service.</p>

{{% /tablestep %}}
{{< /table >}}

At this point you have identified the main building blocks you need for your project.
In the next step, you'll turn the list of building blocks you need into a minimal prototype.

## Step 2: Start with a minimal prototype

The next step is to build a prototype of your project using hardware and mock components.

Let's consider the arm component.
All arms use the same component API, which means you can call methods like `MoveToPosition()` on any arm component.

Because of this, you can start by using hardware you already have or mock components.
Then you can swap out for real or better hardware later as needed.

{{< table >}}
{{% tablestep start=1 %}}
**Use available components.**

There is a range of available models for each component.
Check whether one of the available components works with your hardware, then configure and test it in the Viam web UI.

If you cannot find a suitable component, skip the component for now.

You can search all the available components in the Viam web UI when adding resources, or in the following expander.

{{% expand "Click to view all available components" %}}

{{< tabs >}}
{{% tab name="All components" %}}

{{<resources api="rdk:component" no-intro="true">}}

{{% /tab %}}
{{% tab name="Arm" %}}

The following models implement the [arm component API](/dev/reference/apis/components/arm/):

{{<resources api="rdk:component:arm" type="arm" no-intro="true">}}

{{% /tab %}}
{{% tab name="Base" %}}

The following models implement the [base component API](/dev/reference/apis/components/base/):

{{<resources api="rdk:component:base" type="base" no-intro="true">}}

{{% /tab %}}
{{% tab name="Board" %}}

The following models implement the [board component API](/dev/reference/apis/components/board/):

{{<resources api="rdk:component:board" type="board" no-intro="true">}}

{{% /tab %}}
{{% tab name="Button" %}}

The following models implement the [button component API](/dev/reference/apis/components/button/):

{{<resources api="rdk:component:button" type="button" no-intro="true">}}

{{% /tab %}}
{{% tab name="Camera" %}}

The following models implement the [camera component API](/dev/reference/apis/components/camera/):

{{<resources api="rdk:component:camera" type="camera" no-intro="true">}}

{{% /tab %}}
{{% tab name="Encoder" %}}

The following models implement the [encoder component API](/dev/reference/apis/components/encoder/):

{{<resources api="rdk:component:encoder" type="encoder" no-intro="true">}}

{{% /tab %}}
{{% tab name="Gantry" %}}

The following models implement the [gantry component API](/dev/reference/apis/components/gantry/):

{{<resources api="rdk:component:gantry" type="gantry" no-intro="true">}}

{{% /tab %}}
{{% tab name="Generic" %}}

The following models implement the [generic component API](/dev/reference/apis/components/generic/):

{{<resources api="rdk:component:generic" type="generic" no-intro="true">}}

{{% /tab %}}
{{% tab name="Gripper" %}}

The following models implement the [gripper component API](/dev/reference/apis/components/gripper/):

{{<resources api="rdk:component:gripper" type="gripper" no-intro="true">}}

{{% /tab %}}
{{% tab name="Input Controller" %}}

The following models implement the [input controller component API](/dev/reference/apis/components/input-controller/):

{{<resources api="rdk:component:input_controller" type="input_controller" no-intro="true">}}

{{% /tab %}}
{{% tab name="Motor" %}}

The following models implement the [motor component API](/dev/reference/apis/components/motor/):

{{<resources api="rdk:component:motor" type="motor" no-intro="true">}}

{{% /tab %}}
{{% tab name="Movement Sensor" %}}

The following models implement the [movement sensor component API](/dev/reference/apis/components/movement-sensor/):

{{<resources api="rdk:component:movement_sensor" type="movement_sensor" no-intro="true">}}

{{% /tab %}}
{{% tab name="Power Sensor" %}}

The following models implement the [power sensor component API](/dev/reference/apis/components/power-sensor/):

{{<resources api="rdk:component:power_sensor" type="power_sensor" no-intro="true">}}

{{% /tab %}}
{{% tab name="Sensor" %}}

The following models implement the [sensor component API](/dev/reference/apis/components/sensor/):

{{<resources api="rdk:component:sensor" type="sensor" no-intro="true">}}

{{% /tab %}}
{{% tab name="Servo" %}}

The following models implement the [servo component API](/dev/reference/apis/components/servo/):

{{<resources api="rdk:component:servo" type="servo" no-intro="true">}}

{{% /tab %}}
{{% tab name="Switch" %}}

The following models implement the [switch component API](/dev/reference/apis/components/switch/):

{{<resources api="rdk:component:switch" type="switch" no-intro="true">}}

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Support notice" color="note" %}}
Only modules marked as "built-in" or starting with `viam:` are officially supported and maintained by Viam.
{{% /alert %}}

{{% /expand %}}

**Wood sanding project:**
You might start with a `webcam` camera component and any webcam you have that works with your computer.
Assuming you don't have a robotic arm and button at hand, let's configure those as mock resources in the next step.

{{% /tablestep %}}
{{% tablestep %}}
**Use mock resources.**

If you cannot find a model that supports your specific hardware, start with the `fake` model for that component.
The `fake` model is a mock model for testing that provides the same UI as real physical components.

More importantly, it exposes the same API methods and returns mock data for testing.

**Wood sanding project:**
To mock the resources you don't have hardware for or which you can't find existing resource models for, you add a `fake` arm and a `fake` button.

{{< imgproc src="/tutorials/building/control-tab.png" class="imgzoom shadow" alt="A machine control tab with a fake component" resize="1000x" >}}

{{% /tablestep %}}
{{% tablestep %}}
**Use available services.**

{{< glossary_tooltip term_id="service" text="Services" >}} often require more knowledge and setup.
We recommend consulting the docs for each service that might be helpful for your project and checking for suitable models and usage information.
Then configure the service and test it.

- [**Data management**](/data-ai/capture-data/capture-sync/): Capture, store, and sync data
- [**Vision**](/data-ai/ai/run-inference/#using-a-vision-service) and [**ML model**](/data-ai/ai/deploy/): Detect objects, classify images, or track movement in camera streams
- [**Motion**](/operate/mobility/motion-concepts/) and [**Frame system**](/operate/reference/services/frame-system/#configuration): Plan and execute complex movements
- [**Navigation**](/operate/reference/services/navigation/): Help machines move autonomously
- [**SLAM (Simultaneous Localization and Mapping)**](/operate/reference/services/slam/): Create maps of surroundings and locate machines within those maps
- [**Generic**](/operate/reference/services/generic/): Perform custom business logic by periodically repeating tasks

If you cannot find suitable services, skip the service for now.

You can search all the available services in the Viam web UI when adding resources.

**Wood sanding project:** To find a suitable vision service, you'd look through the available vision services.
There is a [`color_detector` vision service](/operate/reference/services/vision/color_detector/) which you could use to detect the pencil color on wood.
You could also look for or create a machine learning model that recognizes drawings on wood.

The motion service is built in.
To use it you would follow the motion service docs to set it up with your arm.

{{% /tablestep %}}
{{< /table >}}

With your prototype setup and each resource tested in isolation, you can now start writing the control logic that pulls everything together.

## Step 3: Add your control logic

To write your control logic, you'll create a module with a resource that will access and control your components and services.
Often, people use the `DoCommand` method for control logic and then use a {{< glossary_tooltip term_id="job" text="job" >}} to repeatedly call the `DoCommand` method to execute the logic.

For a step-by-step guide, see [Run control logic](/operate/modules/control-logic/).

**Wood sanding project:**
The control logic for the project might look like this:

```python {class="line-numbers linkable-line-numbers" data-line=""}
async def _sand_at(motion, world_state, arm, x_min, x_max, y_min, y_max):
    # simple sanding logic that moves the arm from x_min, y_min to x_max, y_max
    start_pose = translate_x_y_to_coord(x_min, y_min)
    end_pose = translate_x_y_to_coord(x_max, y_max)
    await motion.move(
        component_name=arm, destination=start_pose, world_state=world_state)
    await motion.move(
        component_name=arm, destination=end_pose, world_state=world_state)
    return True


async def _on_loop(self):
    self.logger.info("Executing control logic")
    # Check vision service for detections of the color of the pencil markings
    # on the wood
    detections = self.vision_service.get_detections_from_camera(
        self.camera_name)

    for d in detections:
        await _sand_at(
            self.motion_service,
            self.world_state,
            self.arm_name,
            d.x_min_normalized,
            d.x_max_normalized,
            d.y_min_normalized,
            d.y_max_normalized
        )


async def do_command(
    self,
    command: Mapping[str, ValueTypes],
    *,
    timeout: Optional[float] = None,
    **kwargs
) -> Mapping[str, ValueTypes]:
    result = {key: False for key in command.keys()}
    for name, args in command.items():
        if name == "action" and args == "run_control_logic":
            await self._on_loop()
            result[name] = True
    return result
```

This logic needs iteration.
The next step is to keep iterating to get closer to a working prototype.

## Step 4: Test and Iterate

As you test and iterate, you should also swap out any mock resources you have been using.
If you find any hardware needs to be different, you can also change the hardware.

{{< table >}}
{{% tablestep start=1 %}}
**Swap mock resources.**

If there is no existing resource that suits your needs and you used `fake` resources, you need to create modules to implement your custom components or services.
Often you can do this by wrapping an existing library.
See [Create a module](/operate/modules/support-hardware/) for more information.

**Wood sanding project:**
At this point, you would write a module for the button to start and stop sanding and integrate it with your control logic.

{{% /tablestep %}}
{{% tablestep %}}
**Swap hardware components.**

The engineering cost of changing hardware is relatively low, due to the standardized API.
If you change a component, you will need to change the model and configuration.
Crucially, you should not need to update your control logic unless you use non-standardized `DoCommand` methods.
If you do use `DoCommand` methods, you may need to update or wrap them.

**Wood sanding project:**
At this point in the project you should be getting an idea of the feasibility of the project.
Since arms can be expensive, you may consider buying a cheap model first for testing.
If the cheaper arm can't do sanding, you might test wiping drawings on a whiteboard.
Once you're ready to invest, you can swap to a different arm model.

You might also want to consider adding LiDAR.
With a webcam, you can identify where to sand in a 2-dimensional space but arms move in 3D space.
This means you might need to manually control the third coordinate for now.
This may be fine depending on the use case, or you may consider adding LiDAR to measure the distance to the object being sanded.

{{% /tablestep %}}
{{% tablestep %}}
**Swap services.**

Similar to swapping hardware, you can also swap services.
Maybe you have more powerful hardware and now want to run a TensorFlow model instead of a TensorFlow Lite model.
You can change the ML model service, the model, and the vision service by removing the old services and adding the new services with the same name.
Again, you should not need to update your control logic unless you use non-standardized `DoCommand` methods.
If you do use `DoCommand` methods, you may need to update or wrap them.

**Wood sanding project:**
This is where you'd probably test whether the `color_detector` vision service is sufficient for the project.
If not, you might need to swap it for another vision service.

{{% /tablestep %}}
{{% tablestep %}}
**Manage resource configurations efficiently.**

As you iterate, you may find that you want to save configurations of resources for future use or for reuse across different machines.
Fragments are reusable configuration blocks that make tasks like switching between different resources or adding a configured resource to different machines easier.

To view and create fragments, see the [**FRAGMENTS**](https://app.viam.com/fragments) tab.

**Wood sanding project:**
Your arm configurations are likely to have a lot of parameters that configure where your arm is in 3D space.
If you want to try different arms, or use the arm for a different project, we recommend saving the reusable blocks of the configuration as a fragment.

{{% /tablestep %}}
{{< /table >}}

At this point your project should be mostly functional.
However, you may find that as you move from a minimum viable prototype to a real-world product, you need additional resources.

## Step 5: Consider resource constraints and scaling

You can use {{< glossary_tooltip term_id="part" text="parts" >}} to chain multiple computers together to build complex machines with Viam.

If you are dealing with resource constraints or need to use a specific operating system for some hardware or software, you can add sub-parts to your machine.

If your project requires multiple machines to collaborate, you can use a remote part to share certain resources across the different machines, such as a camera that provides an overview for all machines.

**Wood sanding project:**
If you want multiple arms for the sanding project, you may require multiple computers to drive the arms.
In that case, you can set them up as sub-parts.

Read [Machine architecture: Parts](/operate/reference/architecture/parts/) for more information.

You will likely continue to iterate and fine-tune your machine's logic and configuration.
As you do that you may find a UI useful.

## Step 6: Build a UI

Most projects benefit from a UI, even if just to adjust settings.
Viam provides SDKs for creating web and mobile applications.

You can deploy a static web application as a [Viam application](/operate/control/viam-applications/), where Viam manages hosting infrastructure and authentication for you.

**Wood sanding project:**
You might consider a UI that shows the webcam's view of the surface to be sanded, as well as information about the motion plan for sanding.
If you decide to start and stop sanding with the UI, this is also where you might call the button from.

Your project is now a working prototype.
In the next step, you'll learn about a few tools to consider to take your prototype to production.

## Step 7: Scaling and production

If you intend to ship machines, Viam provides the following features:

- [**Provisioning**](/manage/fleet/provision/setup/): ship machines with a preconfigured setup so customers can connect them to the internet and get them up and running
- [**Remote monitoring**](/manage/troubleshoot/monitor/): monitor, operate, and troubleshoot machines from anywhere in the world
- [**Machine settings**](/manage/fleet/system-settings/): manage operating system package updates, network configuration, and system-level logging
- [**Billing**](/manage/manage/white-labeled-billing/): bill customers for usage through the Viam platform

**Wood sanding project:**
A sanding project might be bespoke enough that you will install it for your customers, so you may not require provisioning.

Remote monitoring means you will be able to check on your clients' machines, perform updates, and troubleshoot should they need help.

You probably do want to configure operating system package updates to ensure the machines update as you expect them to.

The billing setup might be to charge end-customers a fixed cost per machine alongside usage cost.

With this knowledge, you can take your machines from prototype to production.

## Next steps

Now you know how to build any machine, at least in theory.
If you are ready to put the theory into practice, get started and [Set up a computer or SBC](/operate/install/setup/).
