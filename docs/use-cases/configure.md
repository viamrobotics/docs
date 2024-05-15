---
title: "Build a simple smart machine"
linkTitle: "Build simple smart machines"
weight: 10
type: "docs"
description: "Build a simple smart machine in a few steps using Viam's modular system of components and services without writing much or any code."
images: ["/platform/build.svg", "/app/ml/configure.svg"]
tags: ["components", "configuration"]
---

You can get a smart machine running with Viam in just a few steps.

Viam's modular system of {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} means that you can start doing interesting things with your machine without writing much or any code.

{{< table >}}
{{< tablestep >}}

{{<imgproc src="/use-cases/signup-narrow.png" class="fill alignleft" resize="500x" style="max-width: 200px" declaredimensions=true alt="Viam app login screen.">}}
**1. Create a machine in the Viam app**

First, [create a Viam account](https://app.viam.com/) if you haven't already. Log in.

Then create a machine by typing in a name and clicking **Add machine**.

{{<imgproc src="/use-cases/new-machine.png" class="fill aligncenter" resize="400x" style="max-width: 250px" declaredimensions=true alt="Viam app login screen.">}}

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/machine/services/icons/data-capture.svg" class="fill alignright" style="max-width: 150px" declaredimensions=true alt="Installation icon">}}
**2. Install Viam on your machine**

All of the software that runs your smart machine is packaged into a binary called `viam-server`. Install it on the computer controlling your smart machine by following the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} in the [Viam app](https://app.viam.com/).

{{< /tablestep >}}
{{< tablestep >}}

{{<imgproc src="/icons/components.png" class="fill alignleft" resize="400x" style="max-width: 220px" declaredimensions=true alt="An assortment of components.">}}
**3. Configure your components**

Each physical piece of your smart machine that is controlled by a computer is called a _component_. For example, if your smart machine includes a Raspberry Pi, a motor, and a camera, each of those is a component.

You need to [_configure_](/machine/configure/) your machine so that `viam-server` can interact with its hardware.
Use the configuration builder tool in the Viam app to create a file that describes what hardware you are using and how it is connected.
For example, if you have a DC motor, follow the [corresponding configuration instructions](/machine/components/motor/gpio/) to tell the software which pins it is connected to.

{{< /tablestep >}}
{{< tablestep >}}
{{<gif webm_src="/app/fleet/control.webm" mp4_src="/app/fleet/control.mp4" alt="The Viam app Control tab with a control panel for each component. The panel for a DC motor is clicked, expanding to show power controls." max-width="400px" class="fill alignleft">}}

<!-- markdownlint-disable MD036 -->

**4. Test your components**

When you configure a component, a remote control panel is generated for it in the **CONTROL** tab of the Viam app.
With the panels, you can drive motors at different speeds, view your camera feeds, see sensor readings, and generally test the basic functionality of your machine before you've even written any code.

{{< /tablestep >}}
{{< tablestep >}}

{{<imgproc src="/app/ml/collect.svg" class="fill alignright" style="max-width: 220px"  declaredimensions=true alt="Services">}}
**5. Configure services**

Services are built-in Viam software packages that add high-level functionality to your smart machine like computer vision or motion planning.
If you want to use any services, see their [documentation](/machine/services/) for configuration and usage information.
If you are making a simple machine that doesn't use services, you can skip this step!

{{< /tablestep >}}
{{< tablestep >}}

{{<imgproc src="/app/ml/configure.svg" class="fill alignleft" style="max-width: 210px"  declaredimensions=true alt="Services">}}
**6. Do more with code**

Write a program to control your smart machine using the programming language of your choice.
Viam has [SDKs](/sdks/) for Python, Golang, C++, TypeScript and Flutter.

The easiest way to get started is to copy the auto-generated boilerplate code from the **Code sample** page of the **CONNECT** tab on your machine's page in the Viam app.
You can run this code directly on the machine or from a separate computer; it then connects to the machine using API keys.

{{< /tablestep >}}
{{< /table >}}

## Next steps

{{< cards >}}
{{% card link="/get-started/try-viam/" %}}
{{% card link="/tutorials/get-started/lazy-susan/" %}}
{{% card link="/tutorials/get-started/blink-an-led/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{< /cards >}}
