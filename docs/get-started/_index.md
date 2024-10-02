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

<img src="../about-viam.png" width="800px" alt="Viam architecture on device where viam-server uses the machine configuration to manage drivers for different hardware and in the cloud where the platform offer data management, ML, and extended functionality.">

## Support

Viam runs on microcontrollers and 64-bit Linux OS, macOS, or Windows Subsystem for Linux.

{{< board-carousel >}}
<br>

## Viam on your machine

At the core of Viam is the open-source `viam-server` executable which runs on a computer and provides drivers for hardware and manages software and data for a machine.
If you are working with microcontrollers, [`viam-micro-server`](/installation/) is a lightweight version of `viam-server` which can run on resource-limited embedded systems.

- **Configuration**: Create a configuration file specifying which hardware {{< glossary_tooltip term_id="component" text="components" >}} and software {{< glossary_tooltip term_id="service" text="services" >}} the machine consists of and `viam-server` runs the hardware drivers and software to operate your machine.
- **Standard APIs**: Each {{< glossary_tooltip term_id="resource" text="resource" >}} type has a standard, hardware-agnostic API.

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

- **Remote control**: You can use the Viam app, the Viam mobile app, or your own custom apps, to control and monitor your machines securely **from anywhere in the world**.
- **Local control**: In factory settings or remote environments, you can operate and monitor your machines over a local area network (LAN).

## Viam Cloud

The [Viam app](https://app.viam.com) is the ecosystem for configuring and managing machines which provides:

- **Configuration**: As you configure your machine, you can test each resource to confirm it is working. as expected in the same UI you use for configuration.
- **Extensibility**: To support more hardware and software, you can use _{{< glossary_tooltip term_id="module" text="modules" >}}_ from the [Viam Registry](/registry/) or create your own for custom needs.
- **Intelligence**: Make your machines smarter and better with [data management](/services/data/), [machine learning](/services/ml/), [SLAM](/services/slam/) and more.

{{% expand "Click here to see example projects you can build with this" %}}

- Capture sensor data on 100s of boats and sync it to the cloud when machines have internet connectivity.

- Use machine learning to detect wildlife and when detected start data capture and send alerts.

- Allow delivery robots to use their location and SLAM to navigate intelligently between GPS coordinates.

{{% /expand%}}

### Fleet management

The [Viam app](https://app.viam.com)'s **fleet management** capabilities enable you to:

- **Deployment**: Configure and update hardware, software, and machine learning models for groups of machines in one go.
- **Management** Manage deployment and permissions using RBAC.
- **Observability & Teleoperation**: Control and debug machines.

## Next steps

In the next few pages we will guide you through the platform.
You don't need to buy or own any hardware to follow along.

Continue to the [Detect people](/get-started/detect-people/) quickstart:

{{< cards >}}
{{% card link="/get-started/detect-people/" %}}
{{< /cards >}}
