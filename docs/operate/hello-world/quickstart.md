---
linkTitle: "Quick Start"
title: "Quick Start"
weight: 10
layout: "docs"
type: "docs"
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
no_list: false
description: "An introduction to the core concepts you need to know when using Viam."
aliases:
  - /operate/modules/basics/
carouselscript: true
---

Welcome to the Viam documentation! This page introduces you to the core concepts you need to know when using Viam.

{{< alert title="You will learn about" color="note" >}}

- [the Viam platform](#the-viam-platform)
- [Machines](#machines)
- the main building blocks of machines: [components](#components), [services](#services), and [modules](#modules)

{{< /alert >}}

## The Viam platform

Viam is a unified software platform for bringing data management, AI, and automation to the physical world.

The Viam platform consists of:

- **One open-source binary (`viam-server`)** runs on a computer and manages hardware, software, and data
- **Standardized APIs** work across all hardware types
- **Built-in services** for motion planning, machine learning, vision, and data management
- A **registry** of modules for popular hardware and common software needs
- **Cloud-based architecture** for managing machines and controlling configuration updates
- **SDKs** (Python, Go, TypeScript, C++, Flutter)

## Why should I build XYZ with Viam?

If the project you are thinking of is technically possible, you can build it with Viam.
Already have a working system you just want to improve?
That's fine too.

Viam offers:

- **Flexible hardware integration**: Powered by modular code and standardized APIs, you can swap out hardware like arms or motors without code changes.
  That means no vendor lock-in.
- **Real-time data and historic data**: Manage data across machines real-time for data-driven optimization, predictive maintenance, quality assurance and more.
- **AI integration**: Capture data and train models to allow your machines to detect issues, alert you, or act autonomously.
- **Motion control & planning**: A built-in motion service allows for path planning, obstacle avoidance, and more.
- **Fleet management & remote operations**: Remotely monitor operations or control, troubleshoot, or update machines.
- **Industrial-grade reliability**: Viam uses a versioned approach to software deployment, allowing you to test software and control rollout.

## Machines

A _machine_ consists of at least one computer running `viam-server` (often a single-board computer like a Raspberry Pi or Jetson) along with all the hardware components and software services that the computer controls.

When you use Viam to build a machine, you create exactly what you need by mixing and matching different building blocks:

- {{< glossary_tooltip term_id="component" text="components" >}}
- {{< glossary_tooltip term_id="service" text="services" >}}
- {{< glossary_tooltip term_id="module" text="modules" >}}
- {{< glossary_tooltip term_id="trigger" text="triggers" >}}
- {{< glossary_tooltip term_id="job" text="jobs" >}}

### Supported platforms

`viam-server` can run on any computer that runs one of the following operating systems:

- Linux 64-bit operating systems running on AArch64 (ARM64) or x86-64 architectures
- macOS
- Windows

Viam also supports 32-bit microcontrollers such as the ESP32 series.

Examples of computing devices that Viam supports:

{{< board-carousel >}}

## Components

_Components_ are the resources that your machine uses to sense and interact with the world, such as cameras, motors, sensors, and more.
They represent the _eyes_, _ears_, _hands_, and other physical capabilities of your machine.

Components often represent physical hardware, but they can also represent purely software-based resources or control elements.
For example, imagine a sensor that retrieves the current temperature from an API, or a button in an app.

### Supported hardware

**Any type of hardware can be integrated with Viam.**

Viam supports a wide variety of sensors, cameras, and other physical hardware, with standardized APIs.

Common component APIs include:

{{< cards >}}
{{% relatedcard link="/dev/reference/apis/components/arm/" %}}
{{% relatedcard link="/dev/reference/apis/components/base/" %}}
{{% relatedcard link="/dev/reference/apis/components/board/" %}}
{{% relatedcard link="/dev/reference/apis/components/button/" %}}
{{% relatedcard link="/dev/reference/apis/components/camera/" %}}
{{% relatedcard link="/dev/reference/apis/components/motor/" %}}
{{% relatedcard link="/dev/reference/apis/components/sensor/" %}}
{{% relatedcard link="/dev/reference/apis/components/servo/" %}}
{{% relatedcard link="/dev/reference/apis/components/switch/" %}}
{{< /cards >}}

Anything that does not fit the specialized APIs can use the Generic component API.

{{< cards >}}
{{% relatedcard link="/dev/reference/apis/components/generic/" %}}
{{< /cards >}}

## Services

**Services** are higher-level software capabilities that process and interpret data or interact with the world.
Many services depend on components.

Common service APIs include:

- **Vision services**: detect objects, classify images, or track movement in camera streams
- **Motion services**: plan and execute complex movements
- **Data management**: capture, store, and sync data
- **Navigation**: help machines move around autonomously
- **SLAM (Simultaneous Localization and Mapping)**: create maps of surroundings and locate machines within those maps
- **Generic**: The generic service is a flexible service type to perform custom business logic by periodically repeating a task.
## Modules

**Modules** are packages of code that contain components and services.
They allow you to add functionality to machines without modifying Viam's core software.
You can think of modules as plugins that provide drivers for specific hardware models, custom software, or control logic.

Viam has a registry of modules that you can use when building your machines.
Of course, you can also build your own modules.

The components and services provided by modules implement the standardized component and service APIs.

### How everything works together

In practice, these concepts work together as follows:

- Your **computer** runs `viam-server`
- `viam-server` manages connected hardware **components**, such as webcams, motors, and more
- `viam-server` also manages **services**, such as vision services that detect objects in camera streams
- **Modules** are the plugins that provide components, services, and control logic

## Next Steps

Now you know about the most important concepts for using Viam.

We recommend putting these concepts into practice by following the [Desk Safari tutorial](/operate/hello-world/tutorial-desk-safari/) to build your first machine.

If you'd like to learn more about how Viam works, see [Viam architecture](/operate/reference/architecture/).
