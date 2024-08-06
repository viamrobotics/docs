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

Viam is a software platform that makes it easy to combine and integrate hardware and software to build machines, connect them with the cloud, and make them smarter with machine learning.

Machines are everywhere, from small machines like IoT sensors, to home automation systems, robotic systems, cars and boats, and even more complex enterprise systems.
All these machines start by combining hardware and software.

<div>
{{< imgproc src="/viam/viam.png" alt="Viam overview" resize="800x" class="aligncenter" >}}
</div>

## `viam-server` and the Viam app

At the core of Viam is the open-source `viam-server` executable which runs on a computer and manages hardware, software, and data for a machine.
To use Viam with a machine, you create a configuration specifying which hardware and software the machine consists of.
`viam-server` then manages and runs the drivers for the configured hardware components and software services.

For example, if you are building a pet-feeding machine you might install `viam-server` on a Raspberry Pi and create a machine configuration with a camera and a servo for the hardware you are using.

If you are working with microcontrollers, the [micro-RDK](/installation/) is a lightweight version of `viam-server` which can run on resource-limited embedded systems that cannot run the fully-featured `viam-server`.

The [Viam app](https://app.viam.com) provides the user interface for configuring your machine.
You can put together any of the available resources across microcontrollers and computers as configurable building blocks.
As you configure your machine, you can test each resource to confirm it is working as expected.

{{<gif webm_src="/test.webm" mp4_src="/test.mp4" alt="Test a camera stream" max-width="600px" class="aligncenter">}}

Viam has many built-in {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} that run within `viam-server`.

### Extensibility

For everything that is not built-in, you can deploy _{{< glossary_tooltip term_id="module" text="modules" >}}_ from the [**Viam Registry**](/registry/).
Modules provide custom components or services as _modular resources_ which are run and managed by `viam-server` as processes.
When configuring your machine, you can choose and configure built-in components and services, as well as any available from the Viam Registry.
You can also create your own resources for any hardware or software and add them to the Viam Registry.

### Standard APIs

Each category of {{< glossary_tooltip term_id="resource" text="resource" >}}, whether a builtin component or service or a custom component or service from the registry, has a **standardized API** that you can access with an [SDK (software development kit)](/sdks/) in your preferred programming language.
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

However, if you need more custom behaviour, you can [extend these APIs to suit your own needs](/registry/advanced/create-subtype/).

### Connect from anywhere

You can use Viam's SDKs, as well as the Viam app, and the Viam mobile app, to control and monitor your machines securely.
Viam uses WebRTC and gRPC for secure peer-to-peer communications across network boundaries.

If `viam-server` can connect to the internet, you can control and monitor your machines securely **from anywhere in the world**.
In scenarios where machines are connected to a local area network (LAN) with intermittent or no cloud connectivity, you can control and monitor machines from the local network or with code on the machines themselves.

### Better and smarter machines

<div>
<img src="data-ml.svg" alt="A rover detecting a flower" class="alignright" width="400px" >
</div>

The Viam app does not just provide a useful configuration interface.
It also provides several higher-level functionalities to make your machines smarter and better, such as:

- **Data Management**: Any data on your machine can be synced to the cloud.
  From there you can query it using SQL, MQL, or with code.
- **Machine Learning**: Train machine learning models on collected data and deploy ML models to machines to enable them to intelligently see and interpret the world around them.
- **Simultaneous Localization And Mapping (SLAM)**: A machine can map its surroundings and find its position on a map.

### Managing many machines

Viam allows you to manage not just individual machines but entire fleets.
The [Viam app](https://app.viam.com)'s **fleet management** capabilities enable you to:

- Manage software across your fleet, including deployment of code and machine learning models.
- Configure, control, debug, and manage groups of machines in one go.
- Manage permissions within your organization and locations.

You can collaborate on your machines and manage permissions for your fleet using **Role-Based Access Control** (RBAC).
Users can have access to different fleet management capabilities depending on whether they are an owner or an operator of a given organization, location, or machine.

## Support

The `viam-server` executable runs on **any** 64-bit Linux OS or macOS Computer or Windows Subsystem for Linux.
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
