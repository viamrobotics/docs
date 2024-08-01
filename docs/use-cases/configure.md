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

{{< table >}}
{{% tablestep %}}
**1. Create a machine in the Viam app**

First, [create a Viam account](https://app.viam.com/) if you haven't already. Log in.

Then create a machine by typing in a name and clicking **Add machine**.

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

{{% /tablestep %}}
{{% tablestep link="/get-started/installation/" %}}
**2. Install Viam on your machine**

All of the software that runs your smart machine is packaged into a binary called `viam-server`. Install it on the computer controlling your smart machine by following the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} in the [Viam app](https://app.viam.com/).

{{% /tablestep %}}
{{% tablestep link="/components/" %}}
**3. Configure your components**

Each physical piece of your smart machine that is controlled by a computer is called a _component_. For example, if your smart machine includes a Raspberry Pi, a motor, and a camera, each of those is a component.

You need to [_configure_](/configure/) your machine so that `viam-server` can interact with its hardware.
Use the configuration builder tool in the Viam app to create a file that describes what hardware you are using and how it is connected.
For example, if you have a DC motor, follow the [corresponding configuration instructions](/components/motor/gpio/) to tell the software which pins it is connected to.

{{% /tablestep %}}
{{% tablestep %}}

<!-- markdownlint-disable MD036 -->

**4. Test your components**

When you configure a component, a remote control panel is generated for it in the **CONTROL** tab of the Viam app.
With the panels, you can drive motors at different speeds, view your camera feeds, see sensor readings, and generally test the basic functionality of your machine before you've even written any code.

{{<gif webm_src="/fleet/control.webm" mp4_src="/fleet/control.mp4" alt="The Viam app Control tab with a control panel for each component. The panel for a DC motor is clicked, expanding to show power controls." max-width="400px" class="fill alignleft">}}

{{% /tablestep %}}
{{% tablestep link="/services/" %}}

**5. Configure services**

Services are built-in Viam software packages that add high-level functionality to your smart machine like computer vision or motion planning.
If you want to use any services, see their [documentation](/services/) for configuration and usage information.
If you are making a simple machine that doesn't use services, you can skip this step!

{{% /tablestep %}}
{{% tablestep link="/sdks/" %}}

**6. Do more with code**

Write a program to control your smart machine using the programming language of your choice.
Viam has [SDKs](/sdks/) for Python, Golang, C++, TypeScript and Flutter.

The easiest way to get started is to copy the auto-generated boilerplate code from the **Code sample** page of the **CONNECT** tab on your machine's page in the Viam app.
You can run this code directly on the machine or from a separate computer; it then connects to the machine using API keys.

{{% /tablestep %}}
{{< /table >}}

## Next steps

{{< cards >}}
{{% card link="/get-started/try-viam/" %}}
{{% card link="/tutorials/get-started/lazy-susan/" %}}
{{% card link="/tutorials/get-started/blink-an-led/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{< /cards >}}
