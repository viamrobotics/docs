---
title: "Learn about Viam"
linkTitle: "Learn about Viam"
weight: 5
description: "Viam is a complete software platform for smart machines which provides modular components and services for vision, motion, SLAM, ML, and data management."
no_list: true
type: docs
aliases:
  - "/getting-started/"
  - "/getting-started/high-level-overview"
  - "/product-overviews/"
  - "/viam/"
  - "/viam/app.viam.com/"
imageAlt: "/general/understand.png"
images: ["/general/understand.png"]
carouselscript: true
---

Viam is a software platform that makes it easy to work with hardware and software.

<div>
{{< imgproc src="/viam/viam.png" alt="Viam overview" resize="800x" class="aligncenter" >}}
</div>

<div>
{{< imgproc src="/viam/pet-feeder.png" alt="Machine components" resize="400x" class="alignright" >}}
</div>

At the core of Viam is the open-source `viam-server` executable which runs on a device and manages hardware and software for a machine.
To use Viam with a machine, you create a configuration that contains components and services and you can choosen from a wide variety of available models for different resources.
For example, if you have a pet-feeding machine you might install `viam-server` on a Raspberry Pi and create a machine configuration using a camera model and a servo model for the hardware you are using.

The Viam App provides the user interface for configuring your machine.
It allows you to configure builtin drivers or drivers from the Viam Registry.
`viam-server` then manages and runs the drivers for the configured resources.
As you configure your machine, you can test each resource to confirm it is working as expected.

{{<gif webm_src="/test.webm" mp4_src="/test.mp4" alt="Test a camera stream" max-width="700px" class="aligncenter">}}

Viam is built to be extensible, allowing you to create your own resources for custom hardware or software and deploy your code using modules through the Viam Registry.

On top of configuration, the Viam App also provides several higher-level functionalities for your machine, such as:

- **Data Management**: Any data on your machine can be synced to the cloud, from where you can query it using SQL, MQL, or with code.
- **Machine Learning**: Train machine learning models on collected data and deploy ML models to machines to enable them to intelligently see and interpret the world around them.
- **Motion Planning**: Plan and move machine components.
- **Simultaneous Localization And Mapping (SLAM)**: A machine can map its surroundings and find its position on a map.

## Standardized APIs

Each category of {{< glossary_tooltip term_id="resource" text="resource" >}} has a standardized API that you can access with an [SDK (software development kit)](/sdks/) in your preferred programming language.
For example, you can send the same [`SetPower` command](/components/motor/#setpower) to any kind of motor, using any of the available SDKs.

The standardized nature of the resource APIs, means that when you build machines, you can swap out components such as motors without changing any code.
The only change needed is to your machine configuration.

The Viam [Registry](/registry/) provides a marketplace for adding and sharing modules, all using these standard APIs.

## Scale

The Viam App does not limit you to managing just one machine.
Viam's **fleet management** capabilities enable you to:

- Manage permissions within your organization and locations.
- Manage software across your fleet, including deployment of code and machine learning models.
- Configure, control, debug, and manage groups of machines in one go.

## Support

Viam supports devices running **any** 64-bit Linux OS or macOS.
Here are some of the boards Viam supports:

{{< board-carousel >}}
<br>

## Network flexibility

Your machine does not need to be connected to the cloud.
Viam is designed to work whether your machine is connected to the internet continuously or intermittently.

Once `viam-server` is installed, it resides on your machine and alongside your configurations, your code, and services.
In scenarios without cloud connectivity, you can still connect your machine to a local area network (LAN), or to any relevant devices (such as a gamepad):

- All APIs work locally or in the cloud
- Data is cached locally and synced when possible
- Configuration is cached

## Next steps

In the next few pages we will guide you through the platform.
You don't need to buy or own any hardware to complete these quickstarts.

Continue to the [Drive a rover](/get-started/drive-rover/) quickstart:

{{< cards >}}
{{% card link="/get-started/drive-rover/" %}}
{{< /cards >}}
