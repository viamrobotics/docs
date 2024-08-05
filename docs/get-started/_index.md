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

<div>
{{< imgproc src="/viam/viam.png" alt="Viam overview" resize="800x" class="aligncenter" >}}
</div>

Viam is a software platform that makes it easy to work with hardware and software.

<div>
{{< imgproc src="/viam/pet-feeder.png" alt="Machine components" resize="400x" class="alignright" >}}
</div>

At the core of Viam is the open-source `viam-server` executable which runs on a device and manages hardware and software for a machine.
To use Viam with a machine, you create a configuration that contains components and services you choose from a wide variety of available models for different resources.
For example, if you are building a pet-feeding machine you might install `viam-server` on a Raspberry Pi and create a machine configuration using a camera model and a servo model for the hardware you are using.

The [Viam app](https://app.viam.com) provides the user interface for configuring your machine.
It allows you to configure builtin drivers or drivers from the Viam Registry.
`viam-server` then manages and runs the drivers for the configured resources.
As you configure your machine, you can test each resource to confirm it is working as expected.

{{<gif webm_src="/test.webm" mp4_src="/test.mp4" alt="Test a camera stream" max-width="700px" class="aligncenter">}}

Viam is built to be extensible, allowing you to create your own resources for any hardware or software and deploy your code using modules through the Viam Registry.

On top of configuration, the Viam app also provides several higher-level functionalities for your machine, such as:

- **Data Management**: Any data on your machine can be synced to the cloud, from where you can query it using SQL, MQL, or with code.
- **Machine Learning**: Train machine learning models on collected data and deploy ML models to machines to enable them to intelligently see and interpret the world around them.
- **Simultaneous Localization And Mapping (SLAM)**: A machine can map its surroundings and find its position on a map.

## Standardized APIs

Each category of {{< glossary_tooltip term_id="resource" text="resource" >}} has a standardized API that you can access with an [SDK (software development kit)](/sdks/) in your preferred programming language.
For example, you can send the same [`SetPower` command](/components/motor/#setpower) to any kind of motor, using any of the available SDKs:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")
# Set the power to 40% forwards.
await my_motor.set_power(power=0.4)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myMotorComponent, err := motor.FromRobot(machine, "my_motor")
// Set the motor power to 40% forwards.
myMotorComponent.SetPower(context.Background(), 0.4, nil)
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart {class="line-numbers linkable-line-numbers"}
final base = Motor.fromRobot(client, "my_motor");
// Set the power to  40% forwards.
await myMotor.setPower(0.4);
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers"}
const myMotor = new VIAM.MotorClient(client, "my_motor");
// Set the power to  40% forwards.
await myMotor.setPower(0.4);
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp {class="line-numbers linkable-line-numbers"}
std::shared_ptr<Motor> motor = robot->resource_by_name<Motor>("my_motor");
// Set the power to  40% forwards.
motor->set_power(0.4);
```

{{% /tab %}}
{{< /tabs >}}

The standardized nature of Viam's resource APIs means that when you build machines, you can swap out components such as motors without changing any code.
The only change needed is to your machine configuration.

The Viam [Registry](/registry/) provides a marketplace for adding and sharing modules, all using these standard APIs.

## Connect from anywhere

If `viam-server` can connect to the internet, you can

- control and monitor your machines securely from anywhere using the Viam app, the Viam mobile app, or Viam's SDKs
- sync data from machines to the cloud

In scenarios where machines are connected to a local area network (LAN) with intermittent or no cloud connectivity, you can

- control and monitor machines from the local network or with code on the machines themselves
- cache data on the machines and sync it when possible

## Scale

The [Viam App](https://app.viam.com)'s does not limit you to managing just one machine.
Viam's **fleet management** capabilities enable you to:

- Manage permissions within your organization and locations.
- Manage software across your fleet, including deployment of code and machine learning models.
- Configure, control, debug, and manage groups of machines in one go.

## Collaboration

You can collaborate on your machines and manage permissions for your fleet using Role-Based Access Control (RBAC).
Users can have access to different fleet management capabilities depending on whether they are an owner or an operator of a given organization, location, or machine.

## Support

Viam supports devices running **any** 64-bit Linux OS or macOS.
Here are some of the boards Viam supports:

{{< board-carousel >}}
<br>

Viam also supports microcontrollers with the [micro-RDK](/installation/#install-micro-rdk).

## Next steps

In the next few pages we will guide you through the platform.
You don't need to buy or own any hardware to follow along.

Continue to the [Drive a rover](/get-started/drive-rover/) quickstart:

{{< cards >}}
{{% card link="/get-started/drive-rover/" %}}
{{< /cards >}}
