---
title: "Build a simple smart machine"
linkTitle: "Build simple smart machines"
weight: 10
type: "docs"
description: "Build a simple smart machine in a few steps using Viam's modular system of components and services without writing much or any code."
images: ["/platform/build.svg", "/services/ml/configure.svg"]
tags: ["components", "configuration"]
---

You can get a smart machine running with Viam in just a few steps.

Viam's modular system of {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} means that you can start doing interesting things with your machine without writing much or any code.

## Configure a machine

{{< table >}}
{{% tablestep %}}
**1. Create a machine in the Viam app**

First, [create a Viam account](https://app.viam.com/) if you haven't already. Log in.

Then create a machine by typing in a name and clicking **Add machine**.

{{<imgproc src="/fleet/app-usage/create-machine.png" resize="600x" declaredimensions=true alt="The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.">}}

{{% /tablestep %}}
{{% tablestep link="/get-started/installation/" %}}
**2. Install Viam on your machine**

All of the software that runs your smart machine is packaged into a binary called `viam-server`.
Install it on the computer controlling your smart machine by following the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} in the [Viam app](https://app.viam.com/).

If you are using a microcontroller instead of a 64-bit computer, you can install a [lightweight version of `viam-server`](/get-started/installation/microcontrollers/).
You can install `viam-server` on your personal computer, or on a single-board computer (SBC).

{{% /tablestep %}}
{{% tablestep link="/configure/" %}}
**3. Navigate to the CONFIGURE page of your machine**

Machines can be small and simple or very complex but they are all configured on the **CONFIGURE** tab.
A machine can be a single-board computer with a single sensor or LED wired to it, or a machine can consist of multiple computers with many physical components connected, acting as one unit.

<div>
{{< imgproc src="/viam/machine-components.png" alt="Machine components" resize="600x" class="aligncenter" >}}
</div>

{{% /tablestep %}}
{{% tablestep link="/components/" %}}
**4. Configure your components**

Each physical piece of your smart machine that is controlled by a computer is called a {{% glossary_tooltip term_id="component" text="_component_" %}}. For example, if your smart machine includes an arm, a motor, and a camera, each of those is a component.

For each component that makes up your machine:

1. Find an appropriate model for your hardware. For example, you can scroll through available sensor models on the [sensor page](/components/sensor/#available-models).
2. Add a suitable model to your machine on the **CONFIGURE** page by [choosing the component type](/build/configure/#components) (example: `camera`) and model (example: `webcam`).
3. Click on the **Test** area of the configuration panel to test your component.
4. If any problems occur check the [logs](/cloud/machines/#logs) or review or roll back the [configuration history](/cloud/machines/#configure).

If a component you want to use for your project is not natively supported, you can [build your own modular resource](/use-cases/create-module).

You need to [_configure_](/configure/) your machine so that `viam-server` can interact with its hardware.
Use the configuration builder tool in the Viam app to create a file that describes what hardware you are using and how it is connected.
For example, if you have a DC motor, follow the [corresponding configuration instructions](/components/motor/gpio/) to tell the software which pins it is connected to.

{{% /tablestep %}}
{{% tablestep %}}

<!-- markdownlint-disable MD036 -->

**5. Test your components**

When you configure a component, a remote control panel is generated for it in the **CONTROL** tab of the Viam app.
With the panels, you can drive motors at different speeds, view your camera feeds, see sensor readings, and generally test the basic functionality of your machine before you've even written any code.

{{<gif webm_src="/fleet/control.webm" mp4_src="/fleet/control.mp4" alt="The Viam app Control tab with a control panel for each component. The panel for a DC motor is clicked, expanding to show power controls." max-width="400px" class="fill alignleft">}}

{{% /tablestep %}}
{{% tablestep link="/services/" %}}

**6. Configure services**

Services are built-in Viam software packages that add high-level functionality to your smart machine such as:

- **Data Management** enables you to capture and sync data from one or more machines, and use that data for machine learning and beyond.
- **Fleet management** enables you to configure, control, debug, and manage entire fleets of machines.
- **Motion planning** enables your machine to plan and move itself.
- **Vision** enables your machine to intelligently see and interpret the world around it.
- **Simultaneous Localization And Mapping (SLAM)** enables your machine to map its surroundings and find its position on a map.

If you want to use any services, see their [documentation](/services/) for configuration and usage information.
If you are making a simple machine that doesn't use services, you can skip this step!

{{% /tablestep %}}
{{< /table >}}

## Next steps

For more information, see the [configuration documentation](/configure/).
Once you have configured your machine, continue to develop an application:

{{< cards >}}
{{% card link="/use-cases/develop-app/" %}}
{{< /cards >}}

To see full sample projects, that configure and control machines, check out these tutorials:

{{< cards >}}
{{% card link="/get-started/quickstarts/drive-rover/" %}}
{{% card link="/tutorials/get-started/blink-an-led/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{< /cards >}}
