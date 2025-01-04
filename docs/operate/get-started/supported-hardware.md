---
linkTitle: "Integrate supported hardware"
title: "Integrate supported hardware"
weight: 20
layout: "docs"
type: "docs"
no_list: false
description: "Use supported hardware with your machine."
modulescript: true
---

Viam supports a wide variety of sensors, cameras, motors, robotic arms, and other physical hardware.
Viam also supports various software services such as [data capture](/data-ai/get-started/capture-sync/), [computer vision](/data-ai/ai/create-dataset/), and [motion planning](/operate/mobility/move-arm/), designed to integrate seamlessly with the hardware driver modules.

Any hardware that is not already supported by a Viam {{< glossary_tooltip term_id="module" text="module" >}} can be added into Viam's system of modular resources by [creating a new module](../other-hardware/) that provides a driver for the hardware.

<details>
  <summary>You can also create a module to support new software-only functionality.</summary>

In addition to physical hardware, there are "virtual" hardware modules that do not directly drive any physical hardware, but rather augment physical hardware with another layer of abstraction, or add other functionality, for example:

- [A "camera" that takes a camera feed from a physical camera, and crops it, overlays it, or otherwise transforms the output](/components/camera/transform/)
- [A "sensor" that allows you to designate a primary sensor and backup sensors in case of failure](https://github.com/viam-modules/failover)
- [A ChatGPT integration module](https://github.com/jeremyrhyde/chat-gpt-module)

These software-only "hardware" modules implement the same [component APIs](/dev/reference/apis/#component-apis) as physical hardware modules.

</details><br>

After [setting up your machine's computer](/operate/get-started/setup/), you can start adding supported hardware.

## Supported hardware

Many modules are designed to run alongside the full version of [`viam-server`](/operate/get-started/setup/), which runs on 64-bit architectures such as single-board computers and laptop/desktop computers running 64-bit Linux, as well as macOS.

Other modules are designed to run on microcontrollers alongside `viam-micro-server`.

{{< expand "For use with 64-bit architecture" >}}

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

{{< /expand >}}
{{< expand "For use with ESP-32 microcontrollers" >}}

The following is a selection of components (some built-ins and some modules) written for use with `viam-micro-server`.
To use any of the built-in components, configure them according to their readmes.
To use a module with `viam-micro-server`, you need to [build firmware that combines `viam-micro-server` with one or more modules](/operate/get-started/other-hardware/micro-module).

<!--prettier-ignore-->
| Model | Description | Built-in |
| ----- | ----------- | -------- |
| `gpio` | A servo controlled by GPIO pins. [Configuration info](/components/servo/gpio-micro-rdk/). | Yes |
| `two_wheeled_base` | A robotic base with differential steering. [Configuration info](/components/base/two_wheeled_base/). | Yes |
| `free_heap_sensor` | Ships with `viam-micro-server`. [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | No |
| `wifi_rssi_sensor` | Ships with `viam-micro-server`. [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | No |
| `moisture_sensor` | [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | No |
| `water_pump` | [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | No |

{{< /expand >}}

## Configure hardware on your machine

After installing `viam-server` or `viam-micro-server` on your computer or microcontroller, you can configure hardware components on your machine's page in the [Viam app](https://app.viam.com):

1. Click the **+** button on your machine's **CONFIGURE** tab.
1. Click **Component**, then select from available components from the Viam Registry (as well as built-in resources).
1. Use the link to the module README to find information on configuring that specific component.

   {{<gif webm_src="/integrate/configure.webm" mp4_src="/integrate/configure.mp4" alt="Configuring a board and ultrasonic sensor." max-width="600px">}}

   When you add a modular resource _from the registry_, the module that provides it is automatically added at the same time, generating a configuration card for the modular resource and a separate one for the module.
   If you add a built-in component, there will only be a configuration card for the component.

   For details on configuring versioning and environment variables for modules, see [Modular Resource and Module Configuration Details](/operate/reference/module-configuration/).

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

Modules run alongside [`viam-server`](/architecture/viam-server/) as separate processes, communicating with `viam-server` over UNIX sockets.
When a module initializes, it registers its {{< glossary_tooltip term_id="model" text="model or models" >}} and associated [APIs](/appendix/apis/) with `viam-server`, making the new model available for use.
`viam-server` manages the [dependencies](/architecture/viam-server/#dependency-management), [start-up](/architecture/viam-server/#start-up), [reconfiguration](/architecture/viam-server/#reconfiguration), [data management](/services/data/#configuration), and [shutdown](/architecture/viam-server/#shutdown) behavior of your modular resource.
