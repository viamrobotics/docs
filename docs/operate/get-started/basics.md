---
linkTitle: "Learn the basics"
title: "Viam basics"
weight: 10
layout: "docs"
type: "docs"
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
no_list: false
description: "Learn the basics of Viam."
carouselscript: true
---

## What is Viam?

Viam is a software platform for data, AI, and automation.

Viam consists of:

- An open-source binary called `viam-server` that runs on your machine, managing your hardware, software, and data.
- A cloud app called the [Viam app](https://app.viam.com) that you can use to configure and manage your machines and data.
- A registry of modules that support many different types of hardware and software.
- Standardized APIs that abstract the underlying hardware and software.
- SDKs for many programming languages that you can use to control your machines.

`viam-server` connects your machine to the Viam app and to SDK clients.

See [Viam architecture](/operate/reference/architecture/) for details on how Viam works.

## What is a machine?

A _machine_ is a computer (often a single-board computer like a Raspberry Pi or Jetson) or microcontroller and all the hardware attached to it, as well as the software running on it.
You can think of one machine as representing one device, or one robot.
Each machine runs an instance of `viam-server`.

When you create a new machine in the Viam app, Viam generates a unique set of credentials for that machine that connect the physical machine to its instance in the Viam app.

## What platforms does Viam run on?

Viam can run on any computer that runs one of the following operating systems:

- Linux 64-bit operating systems running on AArch64 (ARM64) or x86-64 architectures
- macOS
- Windows

Viam can also run on 32-bit microcontrollers such as the ESP32 series.

Examples of computing devices that can run Viam:

{{< board-carousel >}}

## What hardware does Viam support?

In short, anything.

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

1. [Set up your machine and connect it to the Viam app](/operate/get-started/setup/).

1. Next, [configure supported hardware](/operate/get-started/supported-hardware/) and software on your machine in the Viam app.

1. To integrate other hardware or software services that aren't already supported, you can [write your own modules](/operate/get-started/other-hardware/).

1. [Test your machine](/operate/get-started/test/) by using the **TEST** panel of each configured component's config card to, for example, view your camera's stream or turn your motor.

1. From there, you have many options including:

- [Capture data from your machines](/data-ai/capture-data/capture-sync/)
- [Create a dataset](/data-ai/ai/create-dataset/) and [train an AI model](/data-ai/ai/train-tflite/)
- Use an SDK of your choice to [write an app](/operate/control/web-app/) to control your machines
- [Deploy control logic to run directly on your machines](/manage/software/control-logic/)
- [Share the configuration across multiple machines](/manage/fleet/reuse-configuration/).
