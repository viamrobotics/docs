---
linkTitle: "Quick Start"
title: "Quick Start"
weight: 10
layout: "docs"
type: "docs"
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
no_list: false
description: "An introduction to 80% of the concepts that you will use when using Viam."
aliases:
  - /operate/modules/basics/
carouselscript: true
---

Welcome to the Viam documentation! This page will give you an introduction to 80% of the concepts that you will use when using Viam.

{{< alert title="You will learn about" color="note" >}}

- [the Viam platform](#the-viam-platform)
- [Machines](#machines)
- the main building blocks you can use with a machine: [components](#components), [services](#services), and [modules](#modules)

{{< /alert >}}

## The Viam platform

Viam is a software platform for building smart applications for the physical world.

The Viam platform consists of:

- An open-source binary called `viam-server` that runs on your machine, managing your local hardware, software, and data, and connecting your device to Viam's cloud.
- A [cloud app](https://app.viam.com) that you can use to configure and manage your machines and data.
- Simple APIs for common types of hardware (for example, cameras, sensors, and motors), and software services (such as computer vision).
- A registry of modules that implement the hardware and software APIs.
  This includes support for many popular hardware models.
- SDKs for many programming languages that you can use to interact with your machines.

`viam-server` connects your machine to Viam and to SDK clients.

See [Viam architecture](/operate/reference/architecture/) for details on how Viam works.

## Machines

By installing `viam-server` on your device, you've turned your computer into a Viam {{< glossary_tooltip term_id="machine" text="machine" >}}.

At this point, your machine only runs the Viam software.
To make your machine do something interesting, you must add functionality to it.

When you use Viam to build a machine, you mix and match different building blocks, to make the machine do exactly what you need it to.
The building blocks you'll use in this tutorial are **components**, **services**, and **modules**.
These are the main building blocks that make up all machines.

### What is a machine?

A _machine_ is a computer (often a single-board computer like a Raspberry Pi or Jetson) or microcontroller and all the hardware attached to it, as well as the software running on it.
You can think of one machine as representing one device, such as an Intel RealSense camera connected to a Raspberry Pi.
Each machine runs an instance of `viam-server`.

When you create a new machine on Viam, Viam generates a unique set of credentials for that machine that connect the physical machine to its instance in Viam.

### What platforms does Viam run on?

`viam-server` can run on any computer that runs one of the following operating systems:

- Linux 64-bit operating systems running on AArch64 (ARM64) or x86-64 architectures
- macOS
- Windows

Viam also supports 32-bit microcontrollers such as the ESP32 series.

Examples of computing devices that Viam supports:

{{< board-carousel >}}

## Components

**Components** are the resources that your machine uses to sense and interact with the world, such as cameras, motors, sensors, and more.
They represent the _eyes_, _ears_, _hands_, and other physical capabilities of your machine.

Components can also be resources that others use to give a machine input, such as buttons and switches.

Components often represent physical hardware but they can also represent purely software-based resources.
Imagine a button that is accessible in an app, or a sensor that retrieves the current temperature from an API.

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

Any hardware that is not already supported by a Viam module can be added into Viam's system of modular resources by [creating a new module](/operate/modules/other-hardware/create-module/) that provides a driver for the hardware.

## Services

**Services** are higher-level software capabilities that process and interpret data or interact with the world.
Many services depend on components.
Common services include:

- **Vision services**: detect objects, classify images, or track movement on camera streams
- **Motion services**: plan and execute complex movements
- **Data management**: capture, store, and sync data
- **Navigation**: help machines move around autonomously

## Modules

**Modules** are packages of code that contain components and services.
Modules allow you to add new functionality without modifying Viam's core software.
They're like plugins that expand what your machine can do.

Viam has a registry of modules that you can use when building your machines.
Of course, you can also build your own modules.
In fact, modules are how you add your control logic to a machine.

### How everything works together

Here's how these concepts work together in practice for this tutorial:

- **Your machine**, that is your laptop or desktop computer, runs the Viam software
- A **component**, a webcam, provides access to a camera stream.
- A **service** runs a publicly-available machine learning model, and another service uses the running model and the camera stream to detect objects.
- **Modules** are the plugins that provide the two services.
  You will also create a module for the game logic.

## Next Steps

Now you know how machines work in Viam.

Check out the [Desk Safari tutorial](/operate/hello-world/tutorial-desk-safari/) to build your first machine and learn more about Viam.
