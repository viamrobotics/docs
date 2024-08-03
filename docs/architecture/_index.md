---
title: "Viam Architecture"
linkTitle: "Architecture"
weight: 409
type: "docs"
description: "Overview of how a machine running on Viam is structured."
imageAlt: "Viam architecture"
images: ["/get-started/installation/thumbnails/configure.svg"]
tags: ["components", "services", "communication"]
menuindent: true
---

![Viam data, ML and registry in the cloud and Viam fleet and build on-premises. Viam core is the communication layer that connects the cloud to the on-device portion.](/architecture/cloud-premises.png)

TODO: replace the above diagram with something similar but that more clearly shows viam-server etc.

## Basic structure of a simple machine

<p>
{{<imgproc src="/architecture/simple-machine.png" class="alignright" resize="x1100" declaredimensions=true alt="viam-server running on a board connected to a sensor. Data is stored on a local folder and synced to a folder in the Viam app cloud." style="max-width:400px" >}}
</p>

Imagine you have a simple device consisting of a temperature sensor connected to the GPIO pins of a single-board computer (SBC).
You want data from the sensor to be captured at regular intervals, and synced to the cloud.
To set this up, you would do the following:

- Install `viam-server` on the SBC.
- Create a configuration file in the Viam app indicating that you are using a sensor {{< glossary_tooltip term_id="component" text="component" >}}, and indicating which pins of the SBC it is connected to.
- Configure data capture and sync:
  - Edit your configuration to indicate the interval at which to capture data, and the interval at which to sync it.

When `viam-server` starts, it uses credentials stored locally to establish a connection with the Viam app over {{< glossary_tooltip term_id="webrtc" text="WebRTC" >}}.
It fetches its configuration, which in our example contains the sensor pin information, from the Viam app.

<details>
  <summary>Click for information on local configuration</summary>
  <p>
  If you need to run your machine offline, you can manually create a local configuration file, eliminating the need for <code>viam-server</code> to fetch its config.<br><br>
  The advantages of using the credentials and pulling the config from the Viam app are:
  <ul>
    <li>The config builder UI in the Viam app is more user-friendly than writing JSON manually</li>
    <li>You can easily share configs across multiple identical machines and update them from one place</li>
    <li>etc....TODO</li>
  </ul>
  If your machine usually runs offline but can connect online occasionally, it can pull a configuration from the Viam app and cache it locally to use until the next time it has an internet connection.
  </p>
</details><br>

`viam-server` runs your machine, securely managing all communications between hardware and to the cloud.

You can use the tools in the Viam app to remotely view sensor data as well as to change your machine's configuration, to view logs, and more.

Now imagine you want to run code to send you an email when the temperature sensor reads over 100 degrees Fahrenheit:

- You write code using any of the Viam [SDKs](/sdks/), for example the Viam Python SDK.
- You then run this code either locally on the SBC, or on a separate computer such as a laptop.
  Either way, you include a few lines of code at the top of your script that set up a connection to your machine's `viam-server` instance so you can access the sensor component and use the [sensor API](/components/sensor/#api) to get readings.

  ![alt](/build/program/sdks/robot-client.png)

Now, imagine you want to change to a different model of temperature sensor from a different brand:

- You power down your device, disconnect the old sensor from your SBC and connect the new one.
- You update your configuration in the Viam app to indicate what model you are using, and how it's connected (imagine this one uses USB instead of GPIO pins).
- You turn your device back on, and `viam-server` automatically fetches the config updates.
- You do not need to change your SDK code, because the API is the same for all models of sensor.

## `viam-server`

`viam-server` is the open-source executable binary that runs on your machine's SBC or other computer.

`viam-server` can run your machine without any connection to the internet; it contains all the drivers for your hardware, and it manages local connections between hardware drivers, runs motion planning and vision services locally, and captures and stores data locally.

However, for most use cases you'll want `viam-server` to connect to the cloud so that it can:

- Automatically pull configuration updates you make in the Viam app
- Get new versions of software packages
- Upload and sync image and sensor data
- Allow you to remotely control your machine from the Viam app

## Components, services, modules

A _component_ represents a physical piece of hardware in your {{< glossary_tooltip term_id="machine" text="machine" >}}, and the software that directly supports that hardware.

A _service_ is a software package that makes it easier to add complex capabilities such as motion planning or object detection to your machine.

Viam has many built-in components and services that run within `viam-server`.

A _modular resource_ is a custom component or service, not built into `viam-server` but rather provided by a _module_ that you or another user have created.
A module runs in parallel to `viam-server` on your machine, communicating over UNIX sockets, and `viam-server` manages its lifecycle.

{{<imgproc src="/viam/machine-components.png" resize="x1100" declaredimensions=true alt="Machine structure" style="max-width:600px" >}}

{{< expand "Click for an example" >}}

Imagine you have a wheeled rover with two motors, a GPS unit, and a camera, controlled by a single-board computer (SBC) such as a Raspberry Pi.

The motors, GPS, and camera each require software drivers so that signals can be sent to or from them from your board.
These drivers are called _{{< glossary_tooltip term_id="component" text="components" >}}_.
There is also a _component_ for the board itself that allows Viam software to communicate with the pins on the board.
If you configure a [base component](/components/base/), you can specify the size of the wheels attached to the motors, and how wide the rover base is, so `viam-server` can calculate how to coordinate the motion of the rover base.

If your rover includes a piece of hardware (such as a particular sensor) that is not yet supported in Viam, write a {{< glossary_tooltip term_id="module" text="module" >}} to integrate it into your machine.

Say you want your machine to navigate intelligently between GPS coordinates.
Instead of writing code from scratch, use Viam's built-in navigation service by adding it to your configuration, specifying how the GPS and any additional movement sensors are oriented with respect to your hardware.
Since your configuration now includes information about the wheeled base of your rover as well as how that base is oriented in relation to your GPS and other sensors, `viam-server` can use the motion and navigation services to calculate how much power to send to each motor to get it to a point on the map.

If you want to add some other high-level software functionality beyond the built-in services (for example, your own flavor of navigation service), you can add your own service with a module.

{{< /expand >}}

## Complex machine with many sub-parts

In Viam, a _{{< glossary_tooltip term_id="part" text="part" >}}_ is an organizational concept consisting of one instance of `viam-server` running on a SBC or other computer, and all the hardware and software that that `viam-server` instance controls.

Many simple {{< glossary_tooltip term_id="machine" text="machines" >}} consist of only one part: just one computer running `viam-server`.
If you have a more complex situation with multiple computers and associated hardware working together, you have two options for organization:

- One complex {{< glossary_tooltip term_id="machine" text="machine" >}} consisting of multiple parts, working together.
- Multiple individual machines, linked by a {{< glossary_tooltip term_id="remote-part" text="remote" >}} connection.

These two options are very similar; in both cases, the parts communicate with each other securely using gRPC/{{< glossary_tooltip term_id="webrtc" text="WebRTC" >}}.

Because the parts are interconnected, you can write SDK code that establishes a connection with one of them and controls them all in a coordinated way.

TODO: Find a good example, and explain why you'd want to use one multi-part machine versus many single-part machines

{{< expand "Multi-part example" >}}

Imagine you have a robotic arm with a camera on it, connected to a SBC such as a Raspberry Pi.
You want to use the Viam motion service to control the arm, and you want to use the vision service on the output from the camera, but the SBC does not have the compute power to plan complex motion and also interpret camera output quickly.
You can set up a second {{< glossary_tooltip term_id="part" text="part" >}} on a desktop or laptop computer, either as a sub-part of the same machine or as a separate machine connected as a remote, and offload the heavy compute to that part.

{{< /expand >}}

See [Parts, Sub-parts and Remotes](/architecture/parts/) for more details.

## Communication flow

TODO: Communication flow diagram

On startup, `viam-server` establishes a {{< glossary_tooltip term_id="webrtc" text="WebRTC" >}} connection with the [Viam app](https://app.viam.com).
`viam-server` pulls its configuration from the app, caches it locally, and initializes all components and services based on that configuration.

If sub-parts or remote parts are configured, communications are established between the `viam-server` instances on each of them.

If you have client code running on a separate computer, that code sends API requests to `viam-server` over wifi using gRPC.
If a built-in service is communicating with a component, for example when the vision service requests an image from a camera, `viam-server` handles that request.

{{% alert title="Protobuf APIs" color="info" %}}
All Viam APIs are defined with the [Protocol Buffers (protobuf)](https://protobuf.dev/) framework.
This is what enables Viam to provide SDKs in a variety of different programming languages.
{{% /alert %}}

When you control your machine or view its camera streams or sensor outputs from the Viam app **CONTROL** tab, those connections happen over WebRTC.
The Viam app hits the same API endpoints as your SDK client code, with `viam-server` handling requests.

{{% alert title="Security" color="info" %}}
TLS certificates certificates provided by the app ensure that all communication is authenticated and encrypted.
{{% /alert %}}

For more details, see [Machine-to-Machine Communication](/architecture/machine-to-machine-comms/).

## Data management flow

TODO: Data flow diagram

Here's how data flows in Viam:

1. Data collected by your components, such as sensors and cameras, is first stored locally in a specified directory (defaults to <file>~/.viam/capture</file>).
   You control how often to capture data and where to store it using the configuration file.

   - You can also sync data from other sources by putting it into this folder.
     <br><br>

1. `viam-server` syncs data to a MongoDB database in the cloud at your specified interval, and deletes the data from the local directory.

1. You can view your data from the Viam app or query it using Viam SDKs, MQL, or SQL.

For more information, see [Data Management](/services/data/).

## Next steps

This page has provided an overview of the architecture of just one machine.
For information on organizing a fleet of many machines, see [Cloud Organization Hierarchy](/fleet/).

For more details on the architecture of a single machine, see the following:
