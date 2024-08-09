---
title: "Viam Architecture"
linkTitle: "Architecture"
weight: 409
type: "docs"
description: "How a machine running on Viam is structured, from on-device to cloud communications."
imageAlt: "Viam architecture"
images: ["/viam/machine-components.png"]
tags: ["components", "services", "communication"]
menuindent: true
---

## `viam-server`

`viam-server` is the open-source executable binary that runs on your machine's SBC or other computer.

`viam-server` does the following locally:

- Runs drivers for your hardware
- Runs motion planning and vision services
- Runs {{< glossary_tooltip term_id="module" text="modules" >}}
- Manages local connections between all these resources
- Captures and stores data

When `viam-server` can connect to the cloud, it also:

- Automatically pulls configuration updates you make in the Viam app
- Gets new versions of software packages
- Uploads and syncs image and sensor data
- Allows you to remotely control your machine from the Viam app

`viam-server` can use the internet (WAN) or local networks (LAN) to establish peer-to-peer connections between two {{< glossary_tooltip term_id="machine" text="machines" >}}, or to a client application.

## Components, services, modules

A [_component_](/components/) represents a physical piece of hardware in your {{< glossary_tooltip term_id="machine" text="machine" >}}, and the software that directly supports that hardware.

A [_service_](/services/) is a software package that makes it easier to add complex capabilities such as motion planning or object detection to your machine.

Viam has many built-in components and services that run within `viam-server`.

A [_modular resource_](/registry/) is a custom component or service, not built into `viam-server` but rather provided by a _module_ that you or another user have created.
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

## Communication

<img src="https://assets-global.website-files.com/62fba5686b6d47fe2a1ed2a6/63334e5e19a68d329b1c5b0e_viam-overview-illustrations-manage.svg" alt="A diagram illustrating secure machine control." class="alignleft" style="max-width:270px;"></img>

Viam uses peer-to-peer communication, where all machines running `viam-server` or the [micro-RDK](/installation/micro-rdk-dev/) (the version of `viam-server` for microcontrollers) communicate directly with each other as well as with the cloud.
This peer-to-peer connectivity is enabled by sending [gRPC commands over WebRTC connections](/architecture/machine-to-machine-comms/#low-level-inter-robotsdk-communication).

On startup, `viam-server` establishes a {{< glossary_tooltip term_id="webrtc" text="WebRTC" >}} connection with the [Viam app](https://app.viam.com).
`viam-server` pulls its configuration from the app, caches it locally, and initializes all components and services based on that configuration.

If [sub-parts or remote parts](#complex-machines-with-multiple-parts) are configured, communications are established between the `viam-server` instances on each of them.

If you have client code running on a separate computer, that code sends API requests to `viam-server` using gRPC over WebRTC.
If a WebRTC connection cannot be established, the request is sent directly over gRPC.
When a built-in service communicates with a component, for example when the vision service requests an image from a camera, `viam-server` handles that request as well.

When you control your machine or view its camera streams or sensor outputs from the Viam app **CONTROL** tab, those connections happen over WebRTC.
The Viam app hits the same API endpoints as your SDK client code, with `viam-server` handling requests.

{{% alert title="Protobuf APIs" color="info" %}}
All Viam APIs are defined with the [Protocol Buffers (protobuf)](https://protobuf.dev/) framework.
This is what enables Viam to provide SDKs in a variety of different programming languages.
{{% /alert %}}

For more details, see [Machine-to-Machine Communication](/architecture/machine-to-machine-comms/).

### Security

TLS certificates certificates provided by the Viam app ensure that all communication is authenticated and encrypted.

Viam uses API keys with [role-based access control (RBAC)](/fleet/rbac/) to control access to machines from client code.

## Data management flow

{{<imgproc src="/architecture/data-flow.svg" resize="x1100" declaredimensions=true alt="Data flowing from local disk to cloud to the Viam app, SDKs, and MQL and SQL queries." >}}
<br>

Data is captured and synced to the Viam cloud as follows:

1. Data collected by your components, such as sensors and cameras, is first stored locally in a specified directory (defaults to <file>~/.viam/capture</file>).
   You control how often to capture data and where to store it using the configuration file.

   - You can also sync data from other sources by putting it into this folder.
     <br><br>

1. `viam-server` syncs data to a MongoDB database in the cloud at your specified interval, and deletes the data from the local directory.

1. You can view your data from the Viam app or query it using Viam SDKs, MQL, or SQL.

If a device has intermittent internet connectivity, data is stored locally until the machine can reconnect to the cloud.

For more information, see [Data Management](/services/data/).

## Basic machine example

<p>
{{<imgproc src="/architecture/simple-machine.png" class="alignright" resize="x1100" declaredimensions=true alt="viam-server running on a board connected to a sensor. Data is stored on a local folder and synced to a folder in the Viam app cloud." style="max-width:400px" >}}
</p>

Imagine you have a simple device consisting of a temperature sensor connected to the GPIO pins of a single-board computer (SBC).
You want to capture sensor data at regular intervals, and sync it to the cloud.
Here is how this works in Viam:

- You create a configuration file in the Viam app that includes:
  - A sensor {{< glossary_tooltip term_id="component" text="component" >}}
    - Configure which pins of the SBC the sensor is connected to.
  - Data management {{< glossary_tooltip term_id="service" text="service" >}}
    - Configure the intervals at which to capture and sync data.
- `viam-server` runs on the SBC, managing all communications between hardware and the cloud using gRPC over {{< glossary_tooltip term_id="webrtc" text="WebRTC" >}}.
  On startup, `viam-server` uses credentials stored locally to establish a connection with the Viam app and fetches its configuration.
- Sensor data is cached in a local folder, then synced to the cloud at a configurable interval.
- You can use the tools in the Viam app to remotely view sensor data as well as to change your machine's configuration, to view logs, and more.

Now imagine you want to run code to turn on a fan when the temperature sensor reads over 100 degrees Fahrenheit:

- Configure the fan motor as a motor component and wire the fan motor relay to the same board as the sensor.
- Write your script using one of the Viam [SDKs](/sdks/), for example the Viam Python SDK, using the sensor API and motor API.
- You then run this code either locally on the SBC, or on a separate server.
  Your code connects to the machine, authenticating with API keys, and uses the [sensor API](/components/sensor/#api) to get readings and the [motor API](/components/motor/#api) to turn the motor on and off.

  ![alt](/build/program/sdks/robot-client.png)

Now, imagine you want to change to a different model of temperature sensor from a different brand:

- You power down your device, disconnect the old sensor from your SBC and connect the new one.
- You update your configuration in the Viam app to indicate what model you are using, and how it's connected (imagine this one uses USB instead of GPIO pins).
- You turn your device back on, and `viam-server` automatically fetches the config updates.
- You do not need to change your SDK code, because the API is the same for all models of sensor.

## Complex machines with multiple parts

In Viam, a _{{< glossary_tooltip term_id="part" text="part" >}}_ is an organizational concept consisting of one instance of `viam-server` running on a SBC or other computer, and all the hardware and software that that `viam-server` instance controls.

Many simple {{< glossary_tooltip term_id="machine" text="machines" >}} consist of only one part: just one computer running `viam-server`.
If you have a more complex situation with multiple computers and associated hardware working together, you have two options for organization:

- One complex {{< glossary_tooltip term_id="machine" text="machine" >}} consisting of multiple parts, working together.
- Multiple individual machines, linked by a {{< glossary_tooltip term_id="remote-part" text="remote" >}} connection.

These two options are very similar: in both cases, the parts communicate with each other securely and directly using gRPC/{{< glossary_tooltip term_id="webrtc" text="WebRTC" >}}.

Because the parts are interconnected, you can write SDK code that establishes a connection with one of them and controls them all in a coordinated way.

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

See [Parts, Sub-parts and Remotes](/architecture/parts/) for more details.

## Next steps

This page has provided an overview of the architecture of just one machine.
For information on organizing a fleet of many machines, see [Cloud Organization Hierarchy](/fleet/).

For more details on the architecture of a single machine, see the following:
