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
You can browse all built-in and modular registry components on your machine's configuration page in the Viam app.

## Configure hardware on your machine

**Prerequisite:** A machine with [`viam-server` installed and connected to the cloud](/operate/get-started/setup/).

1. Make sure your hardware is physically connected to your machine and powered on.
1. Navigate to your machine's page in the [Viam app](https://app.viam.com).
1. Click the **+** button on your machine's **CONFIGURE** tab.

   {{<imgproc src="/get-started/plus-button.png" alt="Create a resource button in the Viam app." resize="600x" style="width:350px" class="imgzoom shadow">}}

1. Click **Component**, and search for and select a component that supports your hardware.
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

## Browse supported hardware

You can browse supported hardware and software modules on your machine's configuration page in the Viam app as described above.
The list below is provided for reference.
The following modular components are available for computers and SBCs running `viam-server`.

Search for the name, model number, or manufacturer name of your hardware to see if there is already a hardware driver (_component {{< glossary_tooltip term_id="model" text="model" >}}_) for it.
Or try searching by broader category name, for example "webcam" or "motor," since some components do not require drivers that are specific to their exact make and model.

{{<resources api="rdk:component" no-intro="true">}}

{{% alert title="Support notice" color="note" %}}
Modules in the list above are officially supported and maintained by Viam only if they are marked as "built-in," or if the first part of their model triplet is `viam`.
{{% /alert %}}

### Virtual hardware components

In addition to physical hardware, there are "virtual" hardware modules in the registry that do not directly drive any physical hardware, but rather augment physical hardware with another layer of abstraction, or add other functionality, for example:

- [A "sensor" that allows you to designate a primary sensor and backup sensors in case of failure](https://github.com/viam-modules/failover)
- [A "movement sensor" that calculates the estimated the position of a wheeled rover based on the output of other components](/operate/reference/components/movement-sensor/wheeled-odometry/)
- [A ChatGPT integration module](https://github.com/jeremyrhyde/chat-gpt-module)

These modules implement the same [component APIs](/dev/reference/apis/#component-apis) as physical hardware modules, and are configured in the same way as other components, using the **+** button and selecting **Component** from the dropdown menu.

## Next steps

With your machine configured, you have a number of options:

- [Capture data from your machines](/data-ai/capture-data/capture-sync/)
- [Create a dataset](/data-ai/ai/create-dataset/) and [train an AI model](/data-ai/ai/train-tflite/)
- [Write an app](/operate/control/web-app/) to interact with your machines using any of the Viam SDKs
- [Deploy control logic to run directly on your machines](/manage/software/control-logic/)
- [Share the configuration across multiple machines](/manage/fleet/reuse-configuration/)
