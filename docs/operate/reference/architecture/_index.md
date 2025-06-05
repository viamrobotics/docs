---
title: "Viam architecture"
linkTitle: "Viam architecture"
weight: 10
type: "docs"
description: "How a machine running on Viam is structured, from on-device to cloud communications."
imageAlt: "Viam architecture"
images: ["/viam/machine-components.png"]
tags: ["components", "services", "communication"]
date: "2024-08-13"
aliases:
  - /architecture/
# updated: ""  # When the content was last entirely checked
---

This page provides an overview of how a machine is structured, including on-device and cloud communications:

- [`viam-server` and `viam-micro-server`](#viam-server-and-viam-micro-server)
- [Components, services and modules](#components-services-modules)
- [Communication flow and security](#communication)
- [How data flows in Viam](#data-management-flow)
- [Basic machine example](#basic-machine-example)
- [Structure of more complex machines](#complex-machines-with-multiple-parts)

{{<imgproc class="imgzoom" src="/architecture/architecture-diagram.svg" resize="x1100" declaredimensions=true alt="Viam-server runs on your machine and communicates with processes running on your machine, with the Viam Cloud, with API clients, and with other machines running viam-server." >}}

## `viam-server` and `viam-micro-server`

`viam-server` is the open-source executable binary that runs on your machine's SBC or other computer.

`viam-server` does the following locally:

- Runs drivers for your hardware
- Runs motion planning and vision services
- Runs {{< glossary_tooltip term_id="module" text="modules" >}}
- Manages local connections between all these resources
- Captures and stores data

When `viam-server` can connect to the cloud, it also:

- Automatically pulls configuration updates you make
- Gets new versions of software packages
- Uploads and syncs image and sensor data
- Handles requests from client code you write with [SDKs](/dev/reference/sdks/)
- Allows you to remotely monitor and control your machine

`viam-server` can use the internet, wide area networks (WAN) or local networks (LAN) to establish peer-to-peer connections between two {{< glossary_tooltip term_id="machine" text="machines" >}}, or to a client application.

[`viam-micro-server`](/operate/reference/viam-micro-server/) is the lightweight version of `viam-server` that you can run on ESP32 microcontrollers.
It supports a limited set of {{< glossary_tooltip term_id="resource" text="resources" >}} and can connect with the cloud as well as with devices running `viam-server`.

## Components, services, modules

A {{< glossary_tooltip term_id="component" text="component" >}} represents a physical piece of hardware in your {{< glossary_tooltip term_id="machine" text="machine" >}}, and the software that directly supports that hardware.

A {{< glossary_tooltip term_id="service" text="service" >}} is a software package that adds complex capabilities such as motion planning or object detection to your machine.

Viam has many built-in components and services that run within `viam-server`.

A _modular resource_ is a custom component or service, not built into `viam-server` but rather provided by a _module_ that you or another user have created.
A module runs as a process managed by `viam-server` on your machine, communicating over UNIX sockets, and `viam-server` manages its lifecycle.

{{<imgproc src="/viam/machine-components.png" resize="x1100" declaredimensions=true alt="Machine structure" style="width:600px" >}}

{{< expand "Click for an example" >}}

Imagine you have a wheeled rover with two motors, a GPS unit, and a camera, controlled by a single-board computer (SBC) such as a Raspberry Pi.

The motors, GPS, and camera each require software drivers so that the board can send signals to them and receive signals from them.
These drivers are called _{{< glossary_tooltip term_id="component" text="components" >}}_.
There is also a _component_ for the board itself that allows Viam software to communicate with the pins on the board.

If you configure a [base component](/operate/reference/components/base/), you can specify the size of the wheels attached to the motors, and how wide the rover base is, so `viam-server` can calculate how to coordinate the motion of the rover base.

If your rover includes a piece of hardware (such as a particular sensor) that is not yet supported as a built-in in by Viam, check the registry for a contributed {{< glossary_tooltip term_id="module" text="module" >}} or write your own module to integrate it into your machine.

Say you want your machine to navigate intelligently between GPS coordinates.
Instead of writing code from scratch, you can use Viam's built-in navigation service by adding it to your configuration, specifying how the GPS and any additional movement sensors are oriented with respect to your hardware.
Since your configuration includes information about the wheeled base of your rover as well as how that base is oriented in relation to your GPS and other sensors, `viam-server` can use the motion and navigation services to calculate how much power to send to each motor to get it to a point on the map.

If you want to add some other high-level software functionality beyond the built-in services (for example, your own flavor of navigation service), you can add your own service with a module.

{{< /expand >}}

## Communication

<img src="https://assets-global.website-files.com/62fba5686b6d47fe2a1ed2a6/63334e5e19a68d329b1c5b0e_viam-overview-illustrations-manage.svg" alt="A diagram illustrating secure machine control." class="alignleft" style="width:270px;"></img>

Viam uses peer-to-peer communication, where all machines running `viam-server` or [`viam-micro-server`](/operate/reference/viam-micro-server/) (the version of `viam-server` for microcontrollers) communicate directly with each other as well as with the cloud.
This peer-to-peer connectivity is enabled by sending [gRPC commands over WebRTC connections](/operate/reference/architecture/machine-to-machine-comms/#low-level-inter-robotsdk-communication).

On startup, `viam-server` establishes a {{< glossary_tooltip term_id="webrtc" text="WebRTC" >}} connection with the [Viam app](https://app.viam.com).
`viam-server` pulls its configuration from the app, caches it locally, and initializes all components and services based on that configuration.

If [sub-parts or remote parts](#complex-machines-with-multiple-parts) are configured, communications are established between the `viam-server` instances on each of them.

If you have client code running on a separate computer, that code sends API requests to `viam-server` using gRPC over WebRTC.
If a WebRTC connection cannot be established, the request is sent directly over gRPC.
When a built-in service communicates with a component, for example when the vision service requests an image from a camera, `viam-server` handles that request as well.

When you control your machine or view its camera streams or sensor outputs from the **CONTROL** tab, those connections happen over WebRTC.
The web UI uses the same API endpoints as your SDK client code (in fact, it uses the Viam TypeScript SDK), with `viam-server` handling requests.

{{% alert title="Protobuf APIs" color="info" %}}
All Viam APIs are defined with the [Protocol Buffers (protobuf)](https://protobuf.dev/) framework.
{{% /alert %}}

For more details, see [Machine-to-Machine Communication](/operate/reference/architecture/machine-to-machine-comms/).

### Security

TLS certificates automatically provided by Viam ensure that all communication is authenticated and encrypted.

Viam uses API keys with [role-based access control (RBAC)](/manage/manage/rbac/) to control access to machines from client code.

## Data management flow

{{<imgproc src="/architecture/data-flow.svg" resize="x1100" declaredimensions=true alt="Data flowing from local disk to cloud to Viam, SDKs, and MQL and SQL queries." >}}
<br>

Data is captured and synced to the Viam Cloud as follows:

1. Data collected by your resources, such as sensors and cameras, is first stored locally in a specified directory (defaults to <file>~/.viam/capture</file>).
   You control what data to capture, how often to capture it, and where to store it using the configuration.

   - You can also sync data from other sources by putting it into folders you specify.
     <br><br>

1. `viam-server` syncs data to the cloud at your specified interval, and deletes the data from the local directory.

1. You can view your data in the web UI or query it using Viam SDKs, MQL, or SQL.

If a device has intermittent internet connectivity, data is stored locally until the machine can reconnect to the cloud.

For more information, see [Data management service](/data-ai/capture-data/capture-sync/).

## Basic machine example

<p>
{{<imgproc src="/architecture/simple-machine.png" class="alignright" resize="x1000" declaredimensions=true alt="viam-server running on a board connected to a sensor. Data is temporarily stored on a local folder until it is synced to Viam." style="width:400px" >}}
</p>

Imagine you have a simple device consisting of a temperature sensor connected to the GPIO pins of a single-board computer (SBC).
You want to capture sensor data at regular intervals, and sync it to the cloud.
Here is how this works in Viam:

- You configure your machine in the web UI with a sensor {{< glossary_tooltip term_id="component" text="component" >}} and the data management {{< glossary_tooltip term_id="service" text="service" >}}.
- `viam-server` runs on the SBC, managing all communications between hardware and the cloud using gRPC over {{< glossary_tooltip term_id="webrtc" text="WebRTC" >}}.
  On startup, `viam-server` uses credentials stored locally to establish a connection with Viam and fetches its configuration.
- Sensor data is cached in a local folder, then synced to the cloud at a configurable interval.
- You can use the tools on Viam to remotely view sensor data as well as to change your machine's configuration, to view logs, and more.

Now imagine you want to run code to turn on a fan when the temperature sensor reads over 100 degrees Fahrenheit:

- Configure the fan motor as a motor component and wire the fan motor relay to the same board as the sensor.
- Write your script using one of the Viam [SDKs](/dev/reference/sdks/), for example the Viam Python SDK, using the sensor API and motor API.
- You then run this code either locally on the SBC, or on a separate server.
  See [Create a headless app](/operate/control/headless-app/) for more information.
  Your code connects to the machine, authenticating with API keys, and uses the [sensor API](/operate/reference/components/sensor/#api) to get readings and the [motor API](/operate/reference/components/motor/#api) to turn the motor on and off.

  {{< imgproc src="/build/program/sdks/robot-client.png" resize="x400" declaredimensions=true alt="A desktop computer (client in this case) sends commands to robot 1 (server) with gRPC over wifi." >}}

Now, imagine you want to change to a different model of temperature sensor from a different brand:

- You power down your device, disconnect the old sensor from your SBC and connect the new one.
- You update your configuration in the web UI to indicate what model you are using, and how it's connected (imagine this one uses USB instead of GPIO pins).
- You turn your device back on, and `viam-server` automatically fetches the config updates.
- You do not need to change your control code, because the API is the same for all models of sensor.

## Complex machines with multiple parts

In Viam, a _{{< glossary_tooltip term_id="part" text="part" >}}_ is an organizational concept consisting of one instance of `viam-server` (or `viam-micro-server`) running on a SBC or other computer, and all the hardware and software that the `viam-server` instance controls.

Many simple {{< glossary_tooltip term_id="machine" text="machines" >}} consist of only one part: just one computer running `viam-server` with configured components and services.
If you have a more complex situation with multiple computers and associated hardware working together, you have two options for organization:

- One complex {{< glossary_tooltip term_id="machine" text="machine" >}} consisting of multiple parts, working together.
- Multiple individual machines (each made up of one or more parts), linked by a {{< glossary_tooltip term_id="remote-part" text="remote" >}} connection.

These two options are very similar: in both cases, the parts communicate with each other securely and directly using gRPC/{{< glossary_tooltip term_id="webrtc" text="WebRTC" >}}.
Any given part can be a remote part of multiple machines, whereas a part can only be a sub-part of one machine.
In other words, remote connections allow sharing of resources across multiple machines, whereas main parts and sub-parts are a way to hierarchically organize one machine.

Connecting parts (either as main part and sub-part, or as part and remote part) means that you can write control code that establishes a connection with the main part and controls all parts in a coordinated way.
This streamlines authentication because you do not need to provide multiple sets of API keys as you would if you were using separate API clients.
However, in some high-bandwidth cases it is better to establish a direct connection from an API client to a part, because connections to remotes and to sub-parts use the main part's bandwidth.

{{< expand "Multi-part and remote examples" >}}

- **Compute power example:** Imagine you have a robotic arm with a camera on it, connected to a SBC such as a Raspberry Pi.
  You want to use the Viam motion service to control the arm, and you want to use the vision service on the output from the camera, but the SBC does not have the compute power to plan complex motion and also interpret camera output quickly.
  You can set up a second {{< glossary_tooltip term_id="part" text="part" >}} on a server, as a sub-part of the same machine, and offload the heavy compute to that part.

- **One weather station to many boats:** Imagine you have one weather station collecting data, and multiple boats (perhaps some in different {{< glossary_tooltip term_id="organization" text="organizations" >}}) whose behavior depends on that weather data.
  You can set up a remote connection from each of the `viam-server` instances running on the boats to the `viam-server` instance on the weather station and get that data more directly, without having to wait for the data to sync to the cloud.

- **One camera to many rovers:** Imagine you have a fleet of rovers in a factory.
  One camera has an overhead view of the entire factory floor.
  The camera is set up as one machine.
  Each of the rovers is a separate machine, and they can each have the camera configured as a remote so that they can access the overhead camera stream.

{{< /expand >}}

See [Parts, Sub-parts and Remotes](/operate/reference/architecture/parts/) for more details.

## Next steps

This page has provided an overview of the architecture of just one machine.
For information on organizing a fleet of many machines, see [Organize your machines](/manage/reference/organize/).

For more details on the architecture of a single machine, see the following:
