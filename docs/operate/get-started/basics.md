---
linkTitle: "Learn the basics"
title: "Viam basics"
weight: 10
layout: "docs"
type: "docs"
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
no_list: false
description: "Learn the basics of the Viam platform."
carouselscript: true
---

## What is Viam?

Viam is a software platform for building smart applications for the physical world.

Viam consists of:

- An open-source binary called `viam-server` that runs on your machine, managing your local hardware, software, and data, and connecting your device to Viam's cloud.
- A cloud app called the [Viam app](https://app.viam.com) that you can use to configure and manage your machines and data.
- Simple APIs for common types of hardware (for example, cameras, sensors, and motors), and software services (such as computer vision).
- A registry of modules that implement the hardware and software APIs.
  This includes support for many popular hardware models.
- SDKs for many programming languages that you can use to interact with your machines.

`viam-server` connects your machine to the Viam app and to SDK clients.

See [Viam architecture](/operate/reference/architecture/) for details on how Viam works.

## What is a machine?

A _machine_ is a computer (often a single-board computer like a Raspberry Pi or Jetson) or microcontroller and all the hardware attached to it, as well as the software running on it.
You can think of one machine as representing one device, such as an Intel RealSense camera connected to a Raspberry Pi.
Each machine runs an instance of `viam-server`.

When you create a new machine in the Viam app, Viam generates a unique set of credentials for that machine that connect the physical machine to its instance in the Viam app.

## What platforms does Viam run on?

`viam-server` can run on any computer that runs one of the following operating systems:

- Linux 64-bit operating systems running on AArch64 (ARM64) or x86-64 architectures
- macOS
- Windows

Viam also supports 32-bit microcontrollers such as the ESP32 series.

Examples of computing devices that Viam supports:

{{< board-carousel >}}

## What hardware does Viam support?

In short, any type of hardware can be integrated with Viam.

Viam supports a wide variety of sensors, cameras, and other physical hardware, with APIs for each of the following types of hardware:

{{< cards >}}
{{% relatedcard link="/dev/reference/apis/components/arm/" %}}
{{% relatedcard link="/dev/reference/apis/components/base/" %}}
{{% relatedcard link="/dev/reference/apis/components/board/" %}}
{{% relatedcard link="/dev/reference/apis/components/button/" %}}
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
{{% relatedcard link="/dev/reference/apis/components/switch/" %}}
{{% relatedcard link="/dev/reference/apis/components/generic/" %}}
{{< /cards >}}

These standardized APIs are implemented by {{< glossary_tooltip term_id="module" text="modules" >}} that provide drivers for specific models of hardware.

Any hardware that is not already supported by a Viam module can be added into Viam's system of modular resources by [creating a new module](/operate/get-started/other-hardware/) that provides a driver for the hardware.

## How do I get started?

1. To start, [set up a computer or SBC](/operate/get-started/setup/) or [set up an ESP32](/operate/get-started/setup-micro/) and connect it to the Viam app.

1. Next, you'll configure hardware and software on your machine in the Viam app.
   You can test it with the UI in the app.

1. From there, you have many options including:

- Capturing data from your machines
- Training and deploying an AI model
- Using an SDK of your choice to write an app to interact with your machines
- Deploying control logic
- Sharing the configuration across many machines
