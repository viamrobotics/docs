---
linkTitle: "Integrate supported hardware"
title: "Integrate supported hardware"
weight: 20
layout: "docs"
type: "docs"
imageAlt: "Configure a Machine"
images: ["/viam.svg"]
description: "Use supported hardware with your machine."
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
prev: "/operate/get-started/setup/"
next: "/operate/get-started/other-hardware/"
---

Viam supports a wide variety of sensors, cameras, and other physical hardware, with APIs for each of the following types of hardware:

{{< cards >}}
{{% relatedcard link="/dev/reference/apis/components/arm/" %}}
{{% relatedcard link="/dev/reference/apis/components/base/" %}}
{{% relatedcard link="/dev/reference/apis/components/board/" %}}
{{% relatedcard link="/dev/reference/apis/components/camera/" %}}
{{% relatedcard link="/dev/reference/apis/components/encoder/" %}}
{{% relatedcard link="/dev/reference/apis/components/gantry/" %}}
{{% relatedcard link="/dev/reference/apis/components/gripper/" %}}
{{% relatedcard link="/dev/reference/apis/components/input-controller/" %}}
{{% relatedcard link="/dev/reference/apis/components/motor/" %}}
{{% relatedcard link="/dev/reference/apis/components/movement-sensor/" %}}
{{% relatedcard link="/dev/reference/apis/components/power-sensor/" %}}
{{% relatedcard link="/dev/reference/apis/components/sensor/" %}}
{{% relatedcard link="/dev/reference/apis/components/servo/" %}}
{{% relatedcard link="/dev/reference/apis/components/generic/" %}}
{{< /cards >}}

These standardized APIs are implemented by {{< glossary_tooltip term_id="module" text="modules" >}} that provide drivers for specific models of hardware.

Any hardware that is not already supported by a Viam module can be added into Viam's system of modular resources by [creating a new module](../other-hardware/) that provides a driver for the hardware.

{{% alert title="Tip" color="tip" %}}

Viam also supports various [software services](#add-software-services-to-your-machine) such as [data capture](/data-ai/capture-data/capture-sync/) and [computer vision](/dev/reference/apis/services/vision/), designed to integrate seamlessly with the hardware driver modules.

{{% /alert %}}

## Supported hardware

Many modules are designed to run alongside the full version of [`viam-server`](/operate/reference/viam-server/), which runs on 64-bit architectures such as single-board computers and laptop/desktop computers running 64-bit Linux, as well as macOS.

Other modules are designed to run on microcontrollers alongside [the Micro-RDK](/operate/reference/viam-micro-server/).

### For use with 64-bit architecture

The following modular components are available for computers and SBCs running `viam-server`.

Search for the name, model number, or manufacturer name of your hardware to see if there is already a hardware driver (_component {{< glossary_tooltip term_id="model" text="model" >}}_) for it.
Also try searching by broader category name, for example "webcam" or "motor," since some components do not require drivers that are specific to their exact make and model.

{{<resources api="rdk:component" no-intro="true">}}

{{% alert title="Info" color="tip" %}}
Some components are supported by drivers built into `viam-server`.
The list above contains both modular components and built-in components.
You can also browse these same built-in and modular registry components on your machine's configuration page in the Viam app.

The Viam Registry is the storage and distribution system for not just hardware modules but also software modules (called services), ML models, and ML model training scripts.
You can browse the [Viam Registry in the Viam app](https://app.viam.com/registry?type=Module).
{{% /alert %}}

{{% alert title="Support notice" color="note" %}}
Modules in the list above are officially supported and maintained by Viam if and only if they are marked as "built-in," or if the first part of their model triplet is `viam`.
{{% /alert %}}

### For use with ESP-32 microcontrollers

The following is a selection of components (some built-ins and some modules) written for use with the Micro-RDK.
To use any of the built-in components, configure them according to their readmes.
You can either install the pre-built `viam-micro-server` firmware that ships with a few common modules, or [build your own firmware that combines the Micro-RDK with one or more modules of your choice](/operate/get-started/other-hardware/micro-module/).

<!--prettier-ignore-->
| Model | Description | Ships with `viam-micro-server`? |
| ----- | ----------- | ------------------------------- |
| `gpio` | A servo controlled by GPIO pins. [Configuration info](/operate/reference/components/servo/gpio-micro-rdk/). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `two_wheeled_base` | A robotic base with differential steering. [Configuration info](/operate/reference/components/base/two_wheeled_base/). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `free_heap_sensor` | Reports the amount of free memory space. [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `wifi_rssi_sensor` | A WiFi signal strength sensor. [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `moisture_sensor` | A moisture sensor. [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| `water_pump` | A water pump. [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |

## Configure hardware on your machine

After [installing `viam-server` or `viam-micro-server`](/operate/get-started/setup/) on your computer or microcontroller, you can configure hardware components on your machine's page in the [Viam app](https://app.viam.com):

1. Click the **+** button on your machine's **CONFIGURE** tab.
1. Click **Component**, then select from available components from the Viam Registry (as well as built-in resources).
1. Use the link to the module README to find information on configuring that specific component.

   {{<gif webm_src="/integrate/configure.webm" mp4_src="/integrate/configure.mp4" alt="Configuring a board and ultrasonic sensor." max-width="600px">}}

   When you add a modular resource _from the registry_, the module that provides it is automatically added at the same time, generating a configuration card for the modular resource and a separate one for the module.
   If you add a built-in component, there will only be a configuration card for the component.

   For details on configuring versioning and environment variables for modules, see [Modular Resource and Module Configuration Details](/operate/reference/module-configuration/).

   Note that for microcontrollers, in order to add a module successfully to the machine’s configuration, the module needs to exist in the [firmware build](/operate/get-started/other-hardware/micro-module/).

### Configure virtual hardware components

In addition to physical hardware, there are "virtual" hardware modules that do not directly drive any physical hardware, but rather augment physical hardware with another layer of abstraction, or add other functionality, for example:

- [A "sensor" that allows you to designate a primary sensor and backup sensors in case of failure](https://github.com/viam-modules/failover)
- [A "movement sensor" that calculates the estimated the position of a wheeled rover based on the output of other components](/operate/reference/components/movement-sensor/wheeled-odometry/)
- [A ChatGPT integration module](https://github.com/jeremyrhyde/chat-gpt-module)

These modules implement the same [component APIs](/dev/reference/apis/#component-apis) as physical hardware modules, and are configured in the same way as other components.

## Add software services to your machine

In addition to hardware driver _{{< glossary_tooltip term_id="component" text="components" >}}_ and abstracted "virtual hardware" components, Viam offers _{{< glossary_tooltip term_id="service" text="services" >}}_ to provide higher-level software capabilities.
You can read more about the Viam-maintained services and how to configure them in their respective documentation:

- [Data capture and sync](/data-ai/capture-data/capture-sync/)
- [ML model deployment](/data-ai/ai/deploy/)
- [Computer vision](/data-ai/ai/run-inference/)
- Motion planning for [robot arm motion](/operate/mobility/move-arm/), [mobile robot navigation](/operate/mobility/move-base/), and [gantry motion planning](/operate/mobility/move-gantry/)

To add a service to your machine:

1. Click the **+** button on your machine's **CONFIGURE** tab.
1. Click **Service**, then select from available services.
   The dropdown list includes services from the Viam Registry as well as the built-in services.
1. Add required attributes according to the README or other documentation.

## How modules run

Modules for 64-bit architecture run alongside [`viam-server`](/operate/reference/viam-server/) as separate processes, communicating with `viam-server` over UNIX sockets.
When a module initializes, it registers its {{< glossary_tooltip term_id="model" text="model or models" >}} and associated [APIs](/dev/reference/apis/) with `viam-server`, making the new model available for use.
`viam-server` manages the [dependencies](/operate/reference/viam-server/#dependency-management), [start-up](/operate/reference/viam-server/#start-up), [reconfiguration](/operate/reference/viam-server/#reconfiguration), [data management](/data-ai/capture-data/capture-sync/), and [shutdown](/operate/reference/viam-server/#shutdown) behavior of your modular resource.

For microcontrollers, you must flash a [firmware build that includes the Micro-RDK](/operate/get-started/other-hardware/micro-module/) and one or more modules onto your device.
