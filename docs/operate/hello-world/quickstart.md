---
linkTitle: "Quick Start"
title: "Quick Start"
weight: 10
layout: "docs"
type: "docs"
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
no_list: false
description: "Learn the basics of the Viam platform."
---

Welcome to the Viam documentation! This page will give you an introduction to 80% of the concepts that you will use when using Viam.

{{< alert title="You will learn" color="note" >}}
TODO

{{< /alert >}}

Concepts etc...

## Overview

By installing `viam-server` on your device, you've turned your computer into a Viam {{< glossary_tooltip term_id="machine" text="machine" >}}.

At this point, your machine only runs the Viam software.
To make your machine do something interesting, you must add functionality to it.

When you use Viam to build a machine, you mix and match different building blocks, to make the machine do exactly what you need it to.
The building blocks you'll use in this tutorial are **components**, **services**, and **modules**.
These are the main building blocks that make up all machines.

### Components

**Components** are the resources that your machine uses to sense and interact with the world, such as cameras, motors, sensors, and more.
They represent the _eyes_, _ears_, _hands_, and other physical capabilities of your machine.

Components can also be resources that others use to give a machine input, such as buttons and switches.

Components often represent physical hardware but they can also represent purely software-based resources.
Imagine a button that is accessible in an app, or a sensor that retrieves the current temperature from an API.

### Services

**Services** are higher-level software capabilities that process and interpret data or interact with the world.
Many services depend on components.
Common services include:

- **Vision services**: detect objects, classify images, or track movement on camera streams
- **Motion services**: plan and execute complex movements
- **Data management**: capture, store, and sync data
- **Navigation**: help machines move around autonomously

### Modules

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

Check out the [tutorial](/operate/hello-world/use-first-modules/) to build your first machine.
