---
title: "Create and configure a smart machine"
linkTitle: "Configure a smart machine"
weight: 10
type: "docs"
description: "Create a machine in a few steps using Viam's modular system of components and services without writing much or any code."
images: ["/platform/build.svg", "/services/ml/configure.svg"]
icon: true
tags: ["components", "configuration"]
aliases:
  - /use-cases/configure/
  - use-cases/configure/
languages: []
viamresources: []
platformarea: ["fleet", "core"]
level: "Beginner"
date: "2024-08-02"
# updated: "2024-08-26"  # When the tutorial was last entirely checked
cost: "0"
---

You can get a smart machine running with Viam in just a few steps.

Viam's modular system of {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} means that you can start doing interesting things with your machine without writing much or any code.

{{% alert title="In this page" color="info" %}}

- [Configure a machine](#configure-a-machine)

{{% /alert %}}

## Prerequisites

{{% expand "A device that can run viam-server or viam-micro-server" %}}

See [`viam-server` Platform requirements](/installation/viam-server-setup/#platform-requirements) and [`viam-micro-server` Platform requirements](/installation/viam-micro-server-setup/#platform-requirements) for more information on if your device is suitable.

{{% /expand%}}

## Configure a machine

{{< table >}}
{{% tablestep %}}
**1. Create a machine in the Viam app**

First, [create a Viam account](https://app.viam.com/) if you haven't already. Log in.

Then create a machine by typing in a name and clicking **Add machine**.

{{<imgproc src="/fleet/app-usage/create-machine.png" resize="600x" declaredimensions=true alt="The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.">}}

{{% /tablestep %}}
{{% tablestep link="/installation/" %}}
**2. Install Viam on your machine**

All of the software that runs your machine on a computer is packaged into a binary called `viam-server`.
If you are using a microcontroller, use `viam-micro-server` instead.
Install it on the computer controlling your smart machine by following the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} in the [Viam app](https://app.viam.com/).

You can install `viam-server` on your personal computer, or on a single-board computer (SBC).
After following the setup instructions, your machine should connect and appear as **Live** on the Viam app.

{{% /tablestep %}}
{{% tablestep link="/configure/" %}}
**3. Navigate to the CONFIGURE tab of your machine**

Machines can be small and simple or very complex but they are all configured on the **CONFIGURE** tab of the [Viam app](https://app.viam.com/).
A machine can be a single-board computer with a single sensor or LED wired to it, or a machine can consist of multiple computers with many physical components connected, acting as one unit.

<div>
{{< imgproc src="/how-tos/new-machine-configured.png" alt="A machine on the CONFIGURE tab with a board, two motors, and a camera" resize="600x" class="aligncenter" >}}
</div>

Click on the **CONFIGURE** tab of your machine's page in the Viam app to navigate to it.

{{% /tablestep %}}
{{% tablestep link="/components/" %}}
**4. Configure your components**

Each physical piece of your smart machine that is controlled by a computer is called a {{% glossary_tooltip term_id="component" text="_component_" %}}. For example, if your smart machine includes an arm, a motor, and a camera, each of those is a component.

For each component that makes up your machine:

1. Physically connect the hardware to your machine's computer.
2. Find an appropriate model for your hardware.
   You can find the available models on the [component pages](/components/).
   For example, you can scroll through available sensor models on the [sensor page](/components/sensor/#available-models).
3. You need to [_configure_](/configure/) your machine so that `viam-server` can interact with its hardware.
   Use the configuration builder tool in the Viam app to create a file that describes what hardware you are using and how it is connected.
   For example, if you have a DC motor, follow the [corresponding configuration instructions](/components/motor/gpio/) to tell the software which pins it is connected to.
4. Add a suitable model to your machine on the **CONFIGURE** page:

   - Click the + icon next to your machine part in the left-hand menu and select Component.
   - Choose any component type (example: `camera`) and model (example: `webcam`). If a component you want to use for your project is not natively supported, you can [build your own modular resource](/how-tos/create-module/).

5. When you add a component model, it will create a panel in the configuration builder tool. Fill in any required attributes, following the documentation for the specific model.
6. Click the **TEST** area of the configuration panel to test your component, for example to view a camera feed or turn a motor.
7. If any problems occur check the [**LOGS** tab](/cloud/machines/#logs). You can also review the [configuration history](/cloud/machines/#configure) and roll back changes if needed.

{{% /tablestep %}}
{{% tablestep %}}

<!-- markdownlint-disable MD036 -->

**5. Control your components**

When you configured each component, you saw the **TEST** panel on its configuration panel.
You can also access the control interfaces for all your components in one place from the **CONTROL** tab.
With the panels, you can drive motors at different speeds, view your camera feeds, see sensor readings, and generally test the basic functionality of your machine before you've even written any code.

{{<gif webm_src="/fleet/control.webm" mp4_src="/fleet/control.mp4" alt="The Viam app Control tab with a control panel for each component. The panel for a DC motor is clicked, expanding to show power controls." max-width="600px" class="fill alignleft">}}

{{% /tablestep %}}
{{% tablestep link="/services/" %}}

**6. Configure services**

Services are built-in Viam software packages that add high-level functionality to your smart machine such as:

- **Data Management**: Capture and sync data from one or more machines, and use that data for machine learning and beyond.
- **Fleet Management**: Configure, control, debug, and manage entire fleets of machines.
- **Motion Planning**: Make your machine plan its movement and move itself.
- **Vision**: Enable your machine to intelligently see and interpret the world around it.
- **Simultaneous Localization And Mapping (SLAM)**: Make your machine map its surroundings and find its position on a map.

If you want to use any services, see their [documentation](/services/) for configuration and usage information.
If you are making a simple machine that doesn't use services, you can skip this step!

{{% /tablestep %}}
{{< /table >}}

## Next steps

For more information, see the [configuration documentation](/configure/).
Once you have configured your machine, continue to develop an application.
Or, if you have many machines, learn about how you can use _{{< glossary_tooltip term_id="fragment" text="fragments" >}}_ to configure multiple similar machines in one go:

{{< cards >}}
{{% card link="/how-tos/develop-app/" %}}
{{% card link="/how-tos/one-to-many/" %}}
{{< /cards >}}

To see full sample projects that configure and control machines, check out these tutorials:

{{< cards >}}
{{% card link="/tutorials/get-started/lazy-susan/" %}}
{{% card link="/tutorials/get-started/blink-an-led/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{< /cards >}}
