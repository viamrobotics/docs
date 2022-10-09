---
title: "SDKs as Client"
linkTitle: "SDKs as Client"
weight: 99
type: "docs"
description: "An introduction to Viam's SDKs and how to use them to access and control your robot."
---

## Introduction

The Viam Client Software Development Kit (SDK) contains wrapper classes that you can use to call the Viam API from your application without having to deal with the low-level code that deals directly with the robot's components. Viam's SDKs make it easy to connect to, build, and code custom logic on your robots.

## What is an SDK?

A software development kit (SDK) is a set of tools provided by Viam to help software developers create robotics applications for that specific platform or programming language. Think of it kind of like a toolkit, or the plastic bag of tools that comes packaged with the parts of a dresser you've bought to assemble yourself---only for robotics application development. You have the building blocks---or development tools---you need to get the job done.

Typically, a basic SDK will include a compiler, debugger, and application programming interfaces (APIs), but they can also include any of the following:

-   Documentation

-   Libraries

-   Testing/analysis tools

-   Drivers

-   Network protocols

For Viam, our SDKs allow software developers to directly control and create custom logic for their robots. Our SDKs allow you to write code using building blocks provided by the SDK for interfacing with the hardware and take care of communication between the Client SDK and the `viam-server` running on your robot.

## What is a Client?

A **client** is a computer hardware device or software that accesses a service made available by a server. The server is often (but not always) located on a separate physical computer.

In the case of Viam, a client can be your development machine running one of our SDKs, your robot, or the Viam App. All of these clients communicate with the `viam-server` that is running directly on your robot.

In fact, one of the best parts about using the Viam SDK is that *it can be run locally on one part of the robot or on an entirely separate computer (like your laptop)* if you wish. The client controlling your robot does not need to be installed and run locally to work since both the web app and the SDK clients use the same APIs. This means that as long as the Viam Server is running on your robot, you can control and code your robot from any machine on your local network.

*Figure: Example architecture showing how SDK-based applications communicate with your robot's main instance of viam-server over gRPC.*

![Example architecture showing how SDK-based applications communicate with your robot's main instance of viam-server over gRPC.](../img/using-our-SDKs-as-a-client-application/viam-high-level-overview-diagram-01.png)


## Why connect using a Client?

The simplest answer is that, the `viam-server` doesn't make your robot autonomous alone. To connect to and control your robot, you must install a Client SDK or connect to your robot using the Viam App.

## Why connect as a Client via the Viam App

After [installing the Viam server on a robot (like a Raspberry Pi)](/getting-started/installation/#installing-viam-server), you can connect your newly minted robot to the [Viam App](https://app.viam.com). The Viam App provides a page for each robot to do the following:

-   **Logs**: Displays `viam-server` logs including status changes and error messages.

-   **Config**: Provides a UI for building out your robot configuration.

-   **Control**: Provides a basic UI for testing your robot components and services without needing to write any script--for example, driving the motors and viewing camera feeds.

-   **Connect**: Contains boilerplate connection code to copy and paste into any script you write using SDKs.

You can read [Viam's guide for connecting your robot to the Viam App](https://docs.viam.com/getting-started/installation/#adding-your-pi-on-the-viam-app) to learn more about how to connect your robot to the Viam App Client.

## Why connect as a Client using Viam's SDKs?

If you want to do anything to your robot that isn't supported out of the box in the Viam App, you will need to use one of our Client SDK libraries to write your application. Our SDKs support building blocks, like [vision services](/services/vision/), [motors](/components/motor/), [cameras](/components/camera/), and [much more](https://docs.viam.com). They also manage the communication between the Client SDK and the `viam-server` running on your robot.

Also, Viam's SDKs allow you to connect from any machine that's on the same network as the robot running `viam-server`.

## Viam's Client SDK Libraries

Viam's Client SDKs support many different ways to connect and control your robots, with lots of new ways to connect coming soon.

-   [Viam App](https://app.viam.com/)

-   [Viam Python SDK](https://python.viam.dev)

## Example usage of connecting as a Client using the Viam Python SDK

The [Viam Python SDK](https://python.viam.dev) makes it easier to use an implementation of your robot's components using the Python programming language, than needing to create them directly using the [Viam RDK](https://docs.viam.com/product-overviews/rdk/).

{{% alert title="Tip" color="tip" %}}  
Viam's Software Development Kits (SDKs) provide a wide array of components to customize. 
You can browse through the [API Reference](https://python.viam.dev/autoapi/viam/components/index.html) to see all of them.
{{% /alert %}}

{{% alert title="Note" color="note" %}}  
We will be assuming that you have already [set up Viam Server](/getting-started/installation/#installing-viam-server) on your robot and [connected your robot to the Viam App](/getting-started/installation#adding-your-pi-on-the-viam-app), and [installed the Viam Python SDK](https://python.viam.dev/index.html) on your client before proceeding.
{{% /alert %}}

### How to connect to your Robot using the Viam Python SDK

The easiest way to get started writing a Python application with Viam is to navigate to the [robot page on the Viam App](https://app.viam.com/robots), select the **Connect** tab, and copy the boilerplate code from the section labeled **Python SDK**. This code snippet imports all the necessary libraries and sets up a connection with the Viam App in the cloud.

{{% alert title="Tip" color="tip" %}}  
You can learn more about connecting to your robot with the [Python SDK](https://python.viam.dev) on the [Connect as a Client page](https://python.viam.dev/examples/example.html#connect-as-a-client).*
{{% /alert %}}
### How to get your Robot's Components with the Viam Python SDK

Once you have a connected `RobotClient`, you can then obtain the robot's components by their name. In this example, we are getting a [camera](https://python.viam.dev/autoapi/viam/components/camera/index.html?highlight=camera#module-viam.components.camera) that has been configured on the robot, then taking a photo and displaying the photo.

```python
  from viam.components.camera import Camera
  
  robot = await connect()
  camera = Camera.from_robot(robot, "camera0")
  image = await camera.get_image()
  display(image)
  
  # Don't forget to close the robot when you're done!
  await robot.close()
```

### How to make service calls with the Viam Python SDK

You can also use the `RobotClient` to make service calls to the connected robot. For example, in the snippet below, we are getting the robot's [vision service](https://python.viam.dev/autoapi/viam/services/vision/index.html?highlight=vision#module-viam.services.vision) and then running a detection model on an image to get a list of detections in the next image given a camera and a detector.

```python
  from viam.services.vision import VisionServiceClient
  
  async def vision():
  robot = await connect()
  vision = VisionServiceClient.from_robot(robot)
  detections = await vision.get_detections_from_camera("camera_1", "detector_1")
```

{{% alert title="Tip" color="tip" %}}  
To learn about all the things you can do with Viam's Python SDK, be sure to check out the [Viam Python SDK Documentation](https://python.viam.dev/index.html).
{{% /alert %}}