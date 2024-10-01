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

Machines are everywhere, from small machines like IoT sensors, to home automation systems, robotic systems, cars and boats, and even more complex enterprise systems.
All these machines start by combining hardware and software.

Viam is a software platform that makes it easy to combine and integrate hardware and software to build machines, connect them with the cloud, and make them smarter with machine learning.

<img src="../about-viam.png" width="800px" alt="Viam architecture on device where viam-server uses the machine configuration to manage drivers for different hardware and in the cloud where the platform offer data management, ML, and extended functionality.">

## `viam-server`

At the core of Viam is the open-source `viam-server` executable which runs on a computer and provides drivers for hardware and manages software and data for a machine.
If you are working with microcontrollers, [`viam-micro-server`](/installation/) is a lightweight version of `viam-server` which can run on resource-limited embedded systems that cannot run the fully-featured `viam-server`.

To use Viam with a machine, you create a configuration specifying which hardware and software the machine consists of.
Viam has many built-in {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} that run within `viam-server`.
The components and services are configurable building blocks you can put together to make your machine.
`viam-server` then manages and runs the drivers for the configured hardware components and software services.

For example, if you are building a pet-feeding machine you might install `viam-micro-server` on a microcontroller and create a machine configuration with a camera and a servo for the hardware you are using.

### Standard APIs

Each category of {{< glossary_tooltip term_id="resource" text="resource" >}} has a **standardized API** that you can access with an [SDK (software development kit)](/sdks/) in your preferred programming language.
For example, you can send the same [`SetPower` command](/appendix/apis/components/motor/#setpower) to any kind of motor, using any of the available SDKs:

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

The standardized nature of Viam's resource APIs means that when you build machines, **you can swap out components such as one motor for another motor of a different brand without changing any code**.
The only change needed is to your machine configuration.

However, if you need more custom behaviour, you can [extend these APIs to suit your own needs](/registry/advanced/create-subtype/).

### Connect from anywhere

{{<gif webm_src="/fleet/mobile-app-control.webm" mp4_src="/fleet/mobile-app-control.mp4" alt="Using the control interface under the locations tab on the Viam mobile app" class="alignright" max-width="300px">}}

Viam uses WebRTC and gRPC for **secure peer-to-peer communications across network boundaries**.

In factory settings or remote environments, you can operate and monitor your machines over a local area network (LAN).
Any monitoring or control applications can **connect directly to `viam-server` without internet connection** or run on the machines themselves.

If your machines are connected to the internet, you can operate and monitor them **from anywhere in the world**.

You can use the Viam app and the Viam mobile app, to control and monitor your machines securely.
Or you can use Viam's SDKs to build your own apps.

### Support

The `viam-server` executable runs on **any computer that runs on 64-bit Linux OS, macOS, or Windows Subsystem for Linux**.
Viam also supports microcontrollers with [`viam-micro-server`](/installation/#install-viam-micro-server).

Here are some of the systems Viam runs on:

{{< board-carousel >}}
<br>

## Viam Cloud

The [Viam app](https://app.viam.com) is the ecosystem for configuring and managing machines which provides:

- the user interface for configuring machines
- a community registry of resources for machines
- capabilities to make your machines better and smarter

### Configuration

As you configure your machine, you can test each resource to confirm it is working as expected in the same UI you use for configuration.

{{<gif webm_src="/test.webm" mp4_src="/test.mp4" alt="Test a camera stream" max-width="600px" class="aligncenter">}}

### Extensibility

For everything that is not built-in, you can deploy _{{< glossary_tooltip term_id="module" text="modules" >}}_ from the [**Viam Registry**](/registry/).
Modules provide custom components or services as _modular resources_ which are run and managed by `viam-server` as processes.
When configuring your machine, you can choose and configure built-in components and services, as well as any available from the Viam Registry.
You can also create your own resources for any hardware or software and add them to the Viam Registry.

### Better and smarter machines

<div>
<img src="data-ml.svg" alt="A rover detecting a flower" class="alignright" width="400px" >
</div>

The Viam app provides several higher-level functionalities to make your machines smarter and better, such as:

- **Data Management**: You can collect data from any machine and automagically sync it to the cloud.
  Intermittent connectivity is not a problem, data syncs when possible.
  From there you can query it using SQL, MQL, or with code.
- **Machine Learning**: You can use collected data to train machine learning models within the platform.
  Once trained, you can deploy ML models to all your machines to enable them to intelligently see and interpret the world around them.
  The models run locally and do not require internet access at scoring time.
- **Simultaneous Localization And Mapping (SLAM)**: You can use machines to map their surroundings and to find their own positions on a map.

{{< alert title="Example Applications" color="note" >}}

- Capture sensor data on 100s of boats and sync it to the cloud when machines have internet connectivity.

- Use Machine Learning to detect wildlife and when detected start data capture and send alerts.

- Allow delivery robots to use their location and SLAM to navigate intelligently between GPS coordinates.
  {{< /alert >}}

### Managing many machines

Viam allows you to manage not just individual machines but entire fleets of thousands of machines.
The [Viam app](https://app.viam.com)'s **fleet management** capabilities enable you to:

- Manage software across your fleet, including deployment of code and machine learning models.
- Update software, Configure, control, debug, and manage groups of machines in one go.
- Manage permissions within your organization and locations.

You can collaborate on your machines and manage permissions for your fleet using **Role-Based Access Control** (RBAC).
Users can have access to different fleet management capabilities depending on whether they are an owner or an operator of a given organization, location, or machine.

## Next steps

In the next few pages we will guide you through the platform.
You don't need to buy or own any hardware to follow along.

Continue to the [Control a motor](/get-started/control-motor/) quickstart:

{{< cards >}}
{{% card link="/get-started/control-motor/" %}}
{{< /cards >}}
