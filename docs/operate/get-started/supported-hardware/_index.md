---
linkTitle: "Configure supported hardware"
title: "Configure supported hardware"
weight: 30
layout: "docs"
type: "docs"
imageAlt: "Configure a Machine"
images: ["/viam.svg"]
description: "Use supported hardware with your machine."
modulescript: true
no_list: true
aliases:
  - /program/extend/modular-resources/configure/
  - /extend/modular-resources/configure/
  - /modular-resources/configure/
  - /registry/configure/
  - /registry/modular-resources/
  - /configure/
  - /manage/configuration/
  - /build/configure/
  - /registry/
  - /registry/program/extend/modular-resources/configure/
  - /how-tos/use-cases/configure/
  - /use-cases/configure/
prev: "/operate/get-started/setup/"
next: "/operate/get-started/other-hardware/"
---

## About the Viam Registry of supported hardware and software

Viam has a registry of supported hardware {{< glossary_tooltip term_id="module" text="modules" >}} that implement [standardized APIs](/dev/reference/apis/#component-apis) for each category of hardware {{< glossary_tooltip term_id="component" text="component" >}} (for example, the camera API).
Any hardware that is not already supported by a Viam module can be added into Viam’s system of modular resources by [creating a new module](/operate/get-started/other-hardware/) that provides a driver for the hardware.

The Viam Registry is the storage and distribution system for not just hardware modules but also software modules (called services), ML models, and ML model training scripts.
You can browse the [Viam Registry in the Viam app](https://app.viam.com/registry?type=Module).

Some components are supported by drivers built into `viam-server`, so you won't find them in the registry page.
You can browse all built-in and modular registry components below or on your machine's configuration page in the Viam app.

There are also modules in the registry that do not directly drive any physical hardware, but rather augment physical hardware with another layer of abstraction, or add software functionality such as a chatbot integration.

## Configure hardware on your machine

**Prerequisite:** A machine with [`viam-server` installed and connected to the cloud](/operate/get-started/setup/).

1. Make sure your hardware is physically connected to your machine and powered on.
1. Navigate to your machine's page in the [Viam app](https://app.viam.com).
1. Click the **+** button on your machine's **CONFIGURE** tab.

   {{<imgproc src="/get-started/plus-button.png" alt="Create a resource button in the Viam app." resize="600x" style="width:350px" class="imgzoom shadow">}}

1. Click **Component**.
   This opens a search menu for all existing hardware drivers in the registry.
   Search for and select a component _{{< glossary_tooltip term_id="model" text="model" >}}_ that supports your hardware.
   Search by name, model number, or manufacturer name.
   Or try searching by broader category, for example "webcam" or "motor," since some components do not require drivers that are specific to their exact make and model.

   {{<imgproc src="/get-started/component-search.png" alt="Component search results in the Viam app." resize="600x" style="width:260px" class="imgzoom shadow">}}

   You can also browse the components in the [Browse supported hardware by component API](#browse-supported-hardware-by-component-api) section below.

1. Follow the instructions in the configuration card to configure the component's attributes.

   {{<imgproc src="/get-started/configuration-card.png" alt="Configure a component." resize="900x" style="width:450px" class="imgzoom shadow">}}

   If you need more details, use the link to the module's README.

1. Click the **TEST** panel of the component's configuration card to, for example, view your camera's stream, turn your motor, or see the latest readings from your sensor.

   {{<imgproc src="/get-started/test-panel.png" alt="Sensor test panel showing readings." resize="900x" style="width:400px" class="imgzoom shadow">}}

   If your component is not working as expected, check the **ERROR LOGS** panel for error messages.
   You can also [read more troubleshooting tips](/manage/troubleshoot/troubleshoot/) or click **ASK AI** in the top right corner of the Viam app to get help from Viam's AI assistant.

### How module configuration works

When you add a modular resource _from the registry_, the module that provides it is automatically added at the same time, generating a configuration card for the modular resource and a separate one for the module.
If you add a built-in component, there will only be a configuration card for the component.

For details on configuring versioning and environment variables for modules, see [Modular Resource and Module Configuration Details](/operate/reference/module-configuration/).

Note that for microcontrollers, in order to add a module successfully to the machine’s configuration, the module needs to exist in the [firmware build](/operate/get-started/other-hardware/micro-module/).

## Browse supported hardware by component API

The following modular components are available for computers and SBCs running `viam-server`.
Configure any of these components on your machine by following [the steps above](#configure-hardware-on-your-machine).

If you don't find a component that supports your hardware, you can [create a new module](/operate/get-started/other-hardware/) to add it to the registry.

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
Modules in the list above are officially supported and maintained by Viam only if they are marked as "built-in," or if the first part of their model triplet is `viam`.
{{% /alert %}}

## Next steps

If you have other hardware you need to integrate with a custom module, continue to [Integrate other hardware](/operate/get-started/other-hardware/).
If you have configured all your hardware, you can do a variety of things with your machine:

- [Capture data from your machines](/data-ai/capture-data/capture-sync/)
- [Create a dataset](/data-ai/ai/create-dataset/) and [train an AI model](/data-ai/ai/train-tflite/)
- [Write an app](/operate/control/web-app/) to interact with your machines using any of the Viam SDKs
- [Deploy control logic to run directly on your machines](/manage/software/control-logic/)
- [Share the configuration across multiple machines](/manage/fleet/reuse-configuration/)
