---
title: "Create and configure a machine"
linkTitle: "Configure a machine"
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

You can get any device running with Viam in just a few steps.

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

First, [create a Viam account](https://app.viam.com/) if you haven't already. Log in to the [Viam app](https://app.viam.com/)

Create a {{< glossary_tooltip term_id="machine" text="machine" >}} in any location by clicking **Add machine** and typing in a name and.

{{<imgproc src="/fleet/app-usage/create-machine.png" resize="600x" declaredimensions=true alt="The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.">}}

{{% /tablestep %}}
{{% tablestep link="/installation/viam-server-setup/" %}}
**2. Install Viam on your machine**

Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} on your machine page to install `viam-server`.
If you are using a microcontroller, install `viam-micro-server` instead.
Follow tge setup instructions until your machine connects and appear as **Live** in the Viam app.

{{% /tablestep %}}
{{% tablestep link="/configure/" %}}
**3. Navigate to the CONFIGURE tab of your machine**

All {{< glossary_tooltip term_id="machine" text="machines" >}} are configured on the **CONFIGURE** tab.

<div>
{{< imgproc src="/how-tos/new-machine-configured.png" alt="A machine on the CONFIGURE tab with a board, two motors, and a camera" resize="600x" class="aligncenter" >}}
</div>

Click on the **CONFIGURE** tab of your machine's page in the Viam app to navigate to it.

{{% /tablestep %}}
{{% tablestep link="/configure/#components" %}}
**4. Configure your components**

You will now create a configuration that describes any connected hardware as well as any software your device uses.
The {{% glossary_tooltip term_id="component" text="_components_" %}} in your configuration can describe:

- Physical hardware, such as arms, motors, or cameras.
- Wrappers that provide additional functionality for other configured components, for example a failover motor that switches from one motor to another if the primary motor fails.
- Software that maps to the API calls that you would use for existing hardware types. For example, a temperature sensor may provide temperature readings based on an online service instead of hardware readings. Another such type of sensor that is frequently used returns _readings_ confirming it is safe to sync data or reconfigure a machine.
- Software that does not map well to the existing APIs, such as a switch that you'd like to be able to turn on an off. For these types of components, you use the generic component API.

Follow these for each component that makes up your machine:

1.  On your machine's **CONFIGURE** tab, click the **+** button next to your machine part and select **Component**.
2.  Select the component type you need.
3.  Select from the available models for the component.
    You can find more information about the available models in each component's documentation.
    For example, you can scroll through available sensor models on the [sensor page](/components/sensor/#configuration).

    {{< alert title="Tip" color="tip" >}}

If a component you want to use for your project is not natively supported, you can [build your own modular resource](/how-tos/create-module/).

    {{< /alert >}}

4.  When you add a component, it will create a panel in the configuration builder tool. Fill in any required attributes, following the documentation for the specific model.
    You can find this documentation by following the link to the model's documentation from the available resources clicking on the respective model in each component's documentation

5.  Click the **TEST** area of the configuration panel to test your component.
6.  If any problems occur check the **LOGS** tab or check the component page for component-specific troubleshooting.

{{% /tablestep %}}
{{% tablestep %}}

<!-- markdownlint-disable MD036 -->

**5. Control your components**

When you configured each component, you saw the **TEST** panel on its configuration panel.
You can also access the control interfaces for all your components in one place from the **CONTROL** tab.

{{<gif webm_src="/fleet/control.webm" mp4_src="/fleet/control.mp4" alt="The Viam app Control tab with a control panel for each component. The panel for a DC motor is clicked, expanding to show power controls." max-width="600px" class="fill alignleft">}}

{{% /tablestep %}}
{{% tablestep link="/configure/#services" %}}

**6. Configure services**

Services are software packages that add high-level functionality to your smart machine such as:

- **Data Management**: Capture and sync data from one or more machines, and use that data for machine learning and beyond.
- **Computer Vision**: Enable your machine to intelligently see and interpret the world around it.
- **Motion Planning**: Make your machine plan its movement and move itself.
- **Simultaneous Localization And Mapping (SLAM)**: Make your machine map its surroundings and find its position on a map.

To use these or other services, see their documentation for configuration and usage information.

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
