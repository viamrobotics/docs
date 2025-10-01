---
linkTitle: "How to build a machine"
title: "How to build a machine"
weight: 30
layout: "docs"
type: "docs"
images: ["/icons/components.png"]
imageAlt: "Viam building blocks"
description: "Viam works by breaking complex projects into composable building blocks.
With this approach, your project's complexities become manageable but more importantly, you gain flexibility."
modulescript: true
---

Viam adapts software engineering paradigms to building machines for the physical world.
At its core, Viam works by breaking complex projects into composable building blocks.
With this approach, your project's complexities become manageable but more importantly, you gain more flexibility and testability.

The flexibility means you can, at any point, swap out hardware, change logic, or even change the programming language you're working in.

To accomplish this, you must adopt a _modular_ way of thinking.

At the beginning of a project, you must identify the building blocks of your projects.
Then you can build a prototype with mock resources or real resources.
The next step is to write control logic for your project.
Finally, you iterate and swap any mock resources out for reals ones and make improvements.

The following guide will guide you through the high-level process of designing a machine.
We strongly recommend you follow the [Desk Safari Tutorial before continuing](/operate/hello-world/tutorial-desk-safari/).

## Step 1: Identify the building blocks

Imagine you are building a project to sand wood.
You want to use some robotic arms to do the sanding and cameras or possibly Lidar to identify where to sand.
That's the hardware mostly identified.

For the software-side, you'll want something to identify the areas to sand.
A common technique with sanding is to draw or write something on a piece of wood and sand until you can't see the pencil anymore.

This is enough to get us started identifying the main building blocks.

{{< table >}}
{{< tablestep start=1 >}}

<p><strong>Consider the hardware you need.</strong></p>
<p>In Viam, hardware components are <em>components</em>.
To start with the minimum amount of hardware, you start with one robotic arm, one end-effector, and one camera.</p>
<p>Viam has the following types of components:</p>

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

<p>Your hardware needs can be translated into the following components:</p>
<ul>
<li>one arm</li>
<li>one gripper for the end-effector</li>
<li>one camera</li>
</ul>

{{% /tablestep %}}
{{% tablestep %}}
**Consider other components you need.**

Each piece of hardware in a project is a component, but not every component represents a piece of hardware.
Sometimes components are just software that use the same API endpoints as a physical component might.

Let's say you also want a few buttons to start and stop sanding.
You don't need to at this point decide whether those buttons are physical or software.
For now let's just plan in two buttons using the button component.

{{% /tablestep %}}
{{< tablestep >}}

<p><strong>Consider the services you need.</strong></p>
<p>In Viam, <em>services</em> do more complex work such as motion planning or machine learning.</p>

{{< cards >}}
{{% relatedcard link="/dev/reference/apis/services/data/" %}}
{{% relatedcard link="/dev/reference/apis/services/ml/" highlight="green" %}}
{{% relatedcard link="/dev/reference/apis/services/vision/" highlight="green" %}}
{{% relatedcard link="/dev/reference/apis/services/motion/" highlight="green" %}}
{{% relatedcard link="/dev/reference/apis/services/navigation/" %}}
{{% relatedcard link="/dev/reference/apis/services/SLAM/" %}}
{{% relatedcard link="/dev/reference/apis/services/generic/" %}}
{{% relatedcard link="/dev/reference/apis/services/base-rc/" %}}
{{< /cards >}}

<p>To get the arm to move, you'll want the motion service. For identifying where to sand, you'll need a vision service and an appropriate machine learning model.</p>

{{% /tablestep %}}
{{< /table >}}

## Step 2: Start with a minimal prototype

At this point you have identified the main building blocks you need.
The next step is to build a prototype of your project.

Let's start with hardware components, like the arm component.
All arms use the exact same component API, which means you can call methods like `MoveToPosition()` on any arm component.

Because of this, you can start by using hardware you already have.
Then you can swap out the hardware at a later point for more specialized hardware as needed.

{{< table >}}
{{% tablestep start=1 %}}
**Use available components.**

There are a range of available models for each component.
Check whether one of the available components work with your hardware.

If you cannot find a suitable component, skip the component for now.

You can search all the available components, in the Viam web UI, when adding resources or in the following expander.

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
Only modules marked as "built-in," or starting with `viam:` are officially supported and maintained by Viam.
{{% /alert %}}

{{% /expand%}}

{{% /tablestep %}}
{{% tablestep %}}
**Use available services.**

{{< glossary_tooltip term_id="service" text="Services" >}} frequently require more knowledge and setup.
We recommend consulting the docs for each service that might be helpful for your project and checking for suitable models and usage information.

- [**Data management**](/data-ai/capture-data/capture-sync/): Capture, store, and sync data
- [**Vision**](/data-ai/ai/run-inference/#using-a-vision-service) and [**ML model**](/data-ai/ai/deploy/): Detect objects, classify images, or track movement in camera streams.
- [**Motion**](/operate/mobility/motion-concepts/) and [**Frame system**](/operate/reference/services/frame-system/#configuration): Plan and execute complex movements
- [**Navigation**](/operate/reference/services/navigation/): Help machines move around autonomously
- [**SLAM (Simultaneous Localization and Mapping)**](/operate/reference/services/slam/): Create maps of surroundings and locate machines within those maps
- [**Generic**](/operate/reference/services/generic/): Perform custom business logic by periodically repeating tasks

If you cannot find suitable services, skip the service for now.

You can search all the available services, in the Viam web UI, when adding resources.

{{% /tablestep %}}
{{% tablestep %}}
**Use mock resources.**

If you cannot find a model that supports your specific hardware, start with the `fake` model for that component.
The `fake` model is a mock model for testing which returns mock data when you call its API methods.

{{% /tablestep %}}
{{< /table >}}

## Step 3: Consider resource-constraints and scaling

If you are dealing with resource constraints or need to use a specific operating system for some hardware or software, you can add sub-parts to your machine.
If your project requires multiple machines to collaborate, you may wish to use a remote part to share certain resources across the different machines, such as a camera that provides an overview for all machines.

For more information, read [Machine architecture: Parts](/operate/reference/architecture/parts/).

## Step 4: Add your control logic

With your prototype setup, you can now start writing the control logic for the machine.
To do that you'll create a module with a resource in it which will access and control your components and services
You can use any component or service API that fits.
Often, people use the `DoCommand` method for control logic.

For the sanding machine, the logic might look like this:

- Check vision service for detections of the color of the pencil markings on the wood.
- Use lidar camera to identify location of the surface to be sanded in 3D space.
- Use motion service to calculate a plan for the arm and the attached end-effector with the sanding paper to move around the area that needs sanding.
- Repeat.

For a step-by-step guide, see [Run control logic](/operate/modules/control-logic/).

## Step 5: Iterate

{{< table >}}
{{% tablestep start=1 %}}
**Swap mock resources.**

If there is no existing resource that suits your need and you used `fake` resources, you need to create modules to implement your custom components or services.
Often you can do this by wrapping an existing library.
See [Create a module](/operate/modules/other-hardware/create-module/) for more information.

{{% /tablestep %}}
{{% tablestep %}}
**Swap hardware components.**

The engineering cost of changing hardware is relatively low, due to the standardized API.
If you change the robotic arm, you will need to change the arm model and the arm configuration.
Crucially, you should not need to update your control logic, unless you use non-standardized `DoCommand` methods.
If you do use `DoCommand` methods, you may need to update or wrap those.

{{% /tablestep %}}
{{% tablestep %}}
**Swap services.**

Similar to swapping hardware you can also swap services.
Maybe you have more powerful hardware and now you want to run a TensorFlow model instead of a TFLite model.
You can change the ml model service, the model, and the vision service by removing the old services and adding the new services with the same name.
Again, you should not need to update your control logic, unless you use non-standardized `DoCommand` methods.
If you do use `DoCommand` methods, you may need to update or wrap those.

{{% /tablestep %}}
{{< /table >}}

## Next steps

Now you know how to build any machine in theory.
If you are ready to build your project, see [Set up a computer or SBC](/operate/install/setup/).

If you want to learn more, read about:

- Creating a [Viam application](/operate/control/viam-applications/) as a user interface for the machine(s)
- Setting up many machines with [provisioning](/manage/fleet/provision/setup/)
