---
linkTitle: "Use registry modules"
title: "Configure registry modules"
weight: 10
layout: "docs"
type: "docs"
imageAlt: "Configure a Machine"
images: ["/viam.svg"]
description: "Use modules from the registry and their contained hardware components and software services on your machine."
modulescript: true
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
  - /operate/get-started/supported-hardware/
  - /operate/modules/supported-hardware/
date: "2025-11-04"
---

Viam has a registry of {{< glossary_tooltip term_id="module" text="modules" >}} that implement [standardized APIs](/dev/reference/apis/#component-apis) for categories of hardware {{< glossary_tooltip term_id="component" text="components" >}} and software {{< glossary_tooltip term_id="service" text="services" >}}.

If you are using an ESP32 microcontroller, see the [ESP32-specific instructions](/operate/install/setup-micro/#configure-and-test-your-machine) for how to add modules to the firmware build.

## About the Viam Registry of supported hardware and software

The [registry](https://app.viam.com/registry?type=Module) is the storage and distribution system for {{< glossary_tooltip term_id="module" text="modules" >}}.
Each module can contain any number of {{< glossary_tooltip term_id="resource" text="resources" >}}: components which wrap hardware drivers or services which implement software like ML models.

There are also modules in the registry that do not directly drive any physical hardware, but rather augment physical hardware with another layer of abstraction, or add software functionality such as a chatbot integration.

Some components and services are built into `viam-server`, so you won't find them in the registry.

You can browse all built-in and modular registry components below or on your machine's configuration page.

## Configure hardware or software on your machine

**Prerequisite:** A machine with [`viam-server` installed and connected to the cloud](/operate/install/setup/) and with any hardware physically connected to your machine and powered on.

1. Navigate to your machine's page.
1. Click the **+** button on your machine's **CONFIGURE** tab.

   {{<imgproc src="/get-started/plus-button.png" alt="Create a resource button." resize="600x" style="width:350px" class="imgzoom shadow">}}

1. Click **Component or service**.
   This opens a search menu for all existing hardware and software drivers.
   Search for and select a _{{< glossary_tooltip term_id="model" text="model" >}}_ that supports your hardware or implements your software.
   For hardware, search by name, model number, or manufacturer name.
   Or try searching by broader category, for example "webcam" or "motor," since some components do not require drivers that are specific to their exact make and model.

   {{<imgproc src="/get-started/component-search.png" alt="Component search results." resize="600x" style="width:260px" class="imgzoom shadow">}}

   You can also browse available components in the [Browse supported hardware by component API](#browse-supported-hardware-by-component-api) section and services in the [Browse supported software by service API](#browse-supported-software-by-service-api) section.

1. Follow the instructions in the configuration card to configure the model's attributes.

   {{<imgproc src="/get-started/configuration-card.png" alt="Configure a component or service." resize="900x" style="width:450px" class="imgzoom shadow">}}

   If you need more details, use the link to the module's README.

1. Click the **TEST** panel of the component's configuration card to, for example, view your camera's stream, turn your motor, or see the latest readings from your sensor.

   {{<imgproc src="/get-started/test-panel.png" alt="Sensor test panel showing readings." resize="900x" style="width:400px" class="imgzoom shadow">}}

   If your resource is not working as expected, check the **ERROR LOGS** panel for error messages.
   You can also [read more troubleshooting tips](/manage/troubleshoot/troubleshoot/) or get help from Viam's AI assistant by clicking on the **Ask AI** button.

### How module configuration works

When you add a modular resource _from the registry_, Viam automatically adds the module that provides it at the same time, generating a configuration card for the modular resource and a separate one for the module.
If you add a built-in resource, Viam only adds a configuration card for the resource itself.

For details on configuring versioning and environment variables for modules, see [Modular Resource and Module Configuration Details](/operate/modules/advanced/module-configuration/).

{{< alert title="Tip: Organize resources into folders" color="tip" >}}

If you have many components and services on one machine, you can add folders to your fragment and use them to organize the resources.

{{< /alert >}}

## Browse supported hardware by component API

The following built-in and modular components are available for computers and SBCs running `viam-server`.
Configure any of these components on your machine by following the steps in [Configure hardware or software on your machine](#configure-hardware-or-software-on-your-machine).

If you don't find a component that supports your hardware, you can [create a new module](/operate/modules/support-hardware/) to add it to the registry.

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

## Browse supported software by service API

The following built-in and modular services are available for computers and SBCs running `viam-server`.
Configure any of these services on your machine by following the steps in [Configure hardware or software on your machine](#configure-hardware-or-software-on-your-machine).

If you don't find a service that supports your use case, you can [create a new module](/operate/modules/support-hardware/) to add it to the registry.
If you are looking to write control logic, see [Run control logic](/operate/modules/control-logic/) instead.

{{< tabs >}}
{{% tab name="All services" %}}

{{<resources api="rdk:service" no-intro="true">}}

{{% /tab %}}
{{% tab name="Vision" %}}

The following models implement the [vision service API](/dev/reference/apis/services/vision/):

{{<resources api="rdk:service:vision" type="vision" no-intro="true">}}

{{% /tab %}}
{{% tab name="ML model" %}}

The following models implement the [ML model service API](/dev/reference/apis/services/ml/):

{{<resources api="rdk:service:mlmodel" type="mlmodel" no-intro="true">}}

{{% /tab %}}
{{% tab name="Motion" %}}

The following models implement the [motion service API](/dev/reference/apis/services/motion/):

{{<resources api="rdk:service:motion" type="motion" no-intro="true">}}

{{% /tab %}}
{{% tab name="Generic" %}}

The following models implement the [generic service API](/dev/reference/apis/services/generic/):

{{<resources api="rdk:service:generic" type="generic" no-intro="true">}}

{{% /tab %}}
{{% tab name="SLAM" %}}

The following models implement the [SLAM service API](/dev/reference/apis/services/slam/):

{{<resources api="rdk:service:slam" type="slam" no-intro="true">}}

{{% /tab %}}
{{% tab name="Discovery" %}}

The following models implement the [discovery service API](/dev/reference/apis/services/discovery/):

{{<resources api="rdk:service:discovery" type="discovery" no-intro="true">}}

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Support notice" color="note" %}}
Modules in the list above are officially supported and maintained by Viam only if they are marked as "built-in," or if the first part of their model triplet is `viam`.
{{% /alert %}}

## Next steps

If you have other hardware or software you wish to use, continue to [Support additional hardware and software](/operate/modules/support-hardware/).
If you have configured all your hardware and software, you can do a variety of things with your machine:

- [Deploy control logic to run directly on your machines](/operate/modules/control-logic/)
- [Write an app](/operate/control/web-app/) to interact with your machines using any of the Viam SDKs
- [Capture data from your machines](/data-ai/capture-data/capture-sync/)
- [Create a dataset](/data-ai/train/create-dataset/) and [train an AI model](/data-ai/train/train-tf-tflite/)
- [Share the configuration across multiple machines](/manage/fleet/reuse-configuration/)
