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
It drives your hardware (for example, cameras, sensors, and motors) and connects your devices to the cloud.

Viam consists of:

- An open-source binary called `viam-server` that runs on your machine, managing your hardware, software, and data.
- A cloud app called the [Viam app](https://app.viam.com) that you can use to configure and manage your machines and data.
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
- 32-bit microcontrollers (limited support)

Examples of computers that can run Viam:

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

Viam also supports various software services such as [data capture](/data-ai/capture-data/capture-sync/) and [computer vision](/dev/reference/apis/services/vision/), designed to integrate seamlessly with the hardware driver modules.

## How do I get started?

1. [Install `viam-server`](/operate/get-started/setup/) on your computer or [install `viam-micro-server`](/operate/get-started/setup-micro/) on an ESP32 microcontroller.

1. Then, you'll start [configuring](/operate/get-started/supported-hardware/) your machine in the Viam app, adding hardware components and software services.
   You can [share the configuration across multiple machines](/manage/fleet/reuse-configuration/) to scale quickly.

1. If you want to add custom hardware drivers or software services, you can [write your own modules](/operate/get-started/other-hardware/).

1. [Test your configured resources](/operate/get-started/test/) by using the **TEST** panel of the component's config card to, for example, view your camera's stream or turn your motor.

1. Possible next steps include:

- [Collect data from your machines](/data-ai/capture-data/capture-sync/)
- [Create a dataset](/data-ai/ai/create-dataset/) and [train an AI model](/data-ai/ai/train-tflite/)
- Use an SDK of your choice to [write an app](/operate/control/web-app/) to control your machines
- [Deploy control logic to run directly on your machines](/manage/software/control-logic/)
