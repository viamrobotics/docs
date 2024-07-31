---
title: "Viam in 3 minutes"
linkTitle: "What is Viam?"
description: "Viam is a complete software platform for working with hardware and software."
weight: 10
no_list: true
type: docs
imageAlt: "/general/understand.png"
images: ["/general/understand.png"]
---

{{< alert title="In this page" color="tip" >}}

1. [What is Viam?](#what-is-viam)
1. [How does it work?](#how-does-it-work)
1. [How do I use it?](#how-do-i-use-it)

{{< /alert >}}

## What is Viam?

<img src="https://assets-global.website-files.com/62fba5686b6d47fe2a1ed2a6/633d91b848050946efcf0690_viam-overview-illustrations-build.svg" alt="A diagram of machine parts and software" class="alignright" style="width:200px;"></img>

**Viam is a software platform that makes it easy to work with hardware and software.**

It is a modular system that provides built-in support for a wide variety of standard hardware components and high-level software capabilities, and allows you to add your own {{< glossary_tooltip term_id="module" text="modules" >}} for custom hardware and software.

In addition to the software that runs on your machine, Viam integrates cloud tools for managing data (for example images and sensor readings) and for managing fleets of many machines.

### Built-in functionality

By using existing hardware drivers, you don't need to rewrite code to, for example, run a motor.

By using existing software {{< glossary_tooltip term_id="service" text="services" >}}, you get functionality like machine learning and motion planning built into one software stack, with SDKs for your preferred programming language.

<details>
  <summary><strong>Click to see built-in hardware components and software services</strong></summary>
  <div class="cards max-page">
    <div class="row">
      <div class="col sectionlist">
          <div>
          <h4>Components:</h4>
          {{<sectionlist section="/components/">}}
          </div>
      </div>
      <div class="col sectionlist">
        <div>
          <h4>Services:</h4>
          {{<sectionlist section="/services/">}}
          </div>
      </div>
    </div>
  </div>
</details>

### Modular design

Viam's APIs are standardized across all hardware of a given type, so for example, if you write code to use motion planning with one robot arm and then switch to a different brand and model of arm, you do not need to edit your code.

Viam's modular resource [registry](/registry/) provides a framework for adding and sharing modules seamlessly, all using the standard APIs.

### Cloud connectivity

Viam is designed to work whether your machine is connected to the internet continuously or intermittently.
For more information on how Viam stores and syncs data, see [Data Management](/data/).

## How does it work?

{{< imgproc src="/viam/board-viam-server.png" alt="A diagram of a single-board computer running viam-server." resize="270x" class="alignright" style="max-width:270px" >}}

At the core of Viam is the open-source `viam-server` executable which runs on your computer, IoT device, or robot.
`viam-server`:

- Creates, configures, and maintains any machine on which it is installed.
- Securely handles all communications.
- Runs drivers, custom code, and any other software.
- Accepts API requests.
- Runs {{< glossary_tooltip term_id="service" text="services">}} like computer vision, motion planning, data management, machine learning, and more.

`viam-server` runs on Linux and macOS.

For more information on the cloud and on how communications are handled, see Viam Architecture.

## How do I use it?

Viam's APIs are standardized across all models of a given component or service.
This means you can test and change hardware without changing code.

### Step 1: Install

To get started, first [install `viam-server`](/get-started/installation/) on your smart machine's computer.
If you are using a microcontroller instead of a 64-bit computer, you can install a [lightweight version of `viam-server`](/get-started/installation/microcontrollers/).
You can install `viam-server` on your personal computer, or on a single-board computer (SBC) such as one of the following:
<br><br>

{{< board-carousel >}}

### Step 2: Configure

Machines can be small and simple or very complex.
A machine can be a single-board computer with a single sensor or LED wired to it, or a machine can consist of multiple computers with many physical components connected, acting as one unit.

The term {{% glossary_tooltip term_id="component" text="_component_" %}} describes a piece of hardware that a computer controls, like an arm or a motor.

For each component that makes up your machine:

<p>
{{< imgproc src="/viam/test_components.png" alt="Multiple components being tested in the Viam app." resize="320x" style="max-width:320px" class="alignright" >}}
</p>

1. Add it to your machine by [choosing the component type](/build/configure/#components) (example: `camera`) and model (example: `webcam`).
2. Test it with the visual [control tab](/fleet/control/).
3. See any problems with in-app [logs](/cloud/machines/#logs), review or roll back [configuration history](/cloud/machines/#configure).

If a component or service you want to use for your project is not natively supported, see whether it is supported as a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} in the [registry](/registry/) or build your own modular resource.

After configuring your machine's hardware, you can configure [high level functionality](/services/) the same way:

- **Data Management** enables you to capture and sync data from one or more machines, and use that data for machine learning and beyond.
- **Fleet management** enables you to configure, control, debug, and manage entire fleets of machines.
- **Motion planning** enables your machine to plan and move itself.
- **Vision** enables your machine to intelligently see and interpret the world around it.
- **Simultaneous Localization And Mapping (SLAM)** enables your machine to map its surroundings and find its position on a map.

<div>
{{< imgproc src="/viam/machine-components.png" alt="Machine components" resize="600x" class="aligncenter" >}}
</div>

### Step 3: Program

[Program your smart machine](/build/program/) with an SDK in your preferred coding language.

Each category of {{< glossary_tooltip term_id="resource" text="resource" >}} has a standardized API that you can access with an SDK (software development kit) in your preferred programming language.
For example, you can send the same commands to any kind of motor, using any of the following programming languages:

{{<sectionlist section="/sdks">}}
