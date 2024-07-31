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

## What is Viam?

<img src="https://assets-global.website-files.com/62fba5686b6d47fe2a1ed2a6/633d91b848050946efcf0690_viam-overview-illustrations-build.svg" alt="A diagram of machine parts and software" class="alignright" style="width:200px;"></img>

**Viam is a software platform that makes it easy to work with hardware and software.**

It is a flexible system that provides built-in support for a wide variety of standard hardware components and high-level software capabilities, and allows you to add your own {{< glossary_tooltip term_id="module" text="modules" >}} for custom hardware and software.

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

### The core: `viam-server`

<p>
{{< imgproc src="/viam/board-viam-server.png" alt="A diagram of a single-board computer running viam-server." resize="270x" class="alignright" style="max-width:270px" >}}
</p><br>

At the core of Viam is the open-source `viam-server` executable which runs on your computer, IoT device, or robot.
`viam-server`:

- Creates, configures, and maintains any machine on which it is installed.
- Securely handles all communications.
- Runs drivers, custom code, and any other software.
- Accepts API requests.
- Runs {{< glossary_tooltip term_id="service" text="services">}} like computer vision, motion planning, data management, machine learning, and more.

`viam-server` runs on Linux and macOS and supports a wide variety of popular systems, including:

{{< board-carousel >}}

## How do I use it?

{{< expand "Step 1: Install" >}}

### Step 1: Install

To get started, first [install `viam-server`](/get-started/installation/) on your smart machine's computer.
If you are using a microcontroller instead of a 64-bit computer, you can install a [lightweight version of `viam-server`](/get-started/installation/microcontrollers/).
You can install `viam-server` on your personal computer, or on a single-board computer (SBC).

{{< /expand >}}
{{< expand "Step 2: Configure" >}}

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

{{< /expand >}}
{{< expand "Step 3: Program" >}}

[Program your smart machine](/build/program/) with an SDK in your preferred coding language.

Each category of {{< glossary_tooltip term_id="resource" text="resource" >}} has a standardized API that you can access with an SDK (software development kit) in your preferred programming language.
For example, you can send the same commands to any kind of motor, using any of the following programming languages:

{{<sectionlist section="/sdks">}}

{{< /expand >}}

### Examples

#### Create a smart machine with real-time control, monitoring, and data management

{{<imgproc src="/tutorials/pet-treat-dispenser/preview.png" resize="300x" declaredimensions=true alt="A dog interacting with the smart pet feeder." class="alignleft">}}

Consider a pet feeder which is made up of a webcam and a motor as well as a board with the programming for the device.

<p>
{{<imgproc src="/get-started/camera-motor-board.png" resize="300x" declaredimensions=true alt="A camera, a motor, and a board.">}}</p>

With the Viam app, you can configure the motor and webcam as {{< glossary_tooltip term_id="component" text="components" >}}.

By configuring your machine with Viam, you can now:

{{< table >}}
{{% tablestep link="/cloud/machines/#control"%}}
<img src="/get-started/feed.gif" alt="Viewing the camera feed from the Viam app Control tab" style="max-width:600px" class="fill alignleft">

**Remotely access and control the machine**

Using the Viam app or the Viam mobile app, you can view the camera feed and turn on the motor to feed your pet.

{{% /tablestep %}}
{{% tablestep link="/services/data/"%}}
{{<imgproc src="/get-started/bowl-images.png" class="fill alignleft" resize="800x" style="max-width: 500px" declaredimensions=true alt="Screenshot of food bowl pictures">}}
**Collect and upload data to the cloud**

You can configure the camera to capture a photo of the food bowl periodically and automatically sync these photos to the cloud.

{{% /tablestep %}}
{{% tablestep link="/services/ml/"%}}
{{<imgproc src="/get-started/bowl-label.jpg" class="fill alignright" resize="600x" style="max-width: 200px" declaredimensions=true alt="Screenshot of food bowl pictures with labels">}}
**Use collected data to build data sets and train and machine learning models**

Having captured pictures of the food bowl, you can organize them into a dataset and label each as empty or full.
Once you have the data labeled, you can train a machine learning model within Viam to recognize empty and full food bowls.

{{% /tablestep %}}
{{% tablestep link="/services/ml/deploy/"%}}
{{<imgproc src="/services/deploy-model.png" class="fill alignright" resize="800x" style="max-width: 500px" declaredimensions=true alt="Screenshot of food bowl view with classifier">}}
**Deploy machine learning models to make your machine even smarter**

`viam-server` not only supports components but also allows you to deploy services.
We can use the ML model service to deploy the model that recognizes empty and full food bowls, and deploy a vision service to apply the model to a camera stream.

{{% /tablestep %}}
{{% tablestep link="/build/program/"%}}

**Write code to control the machine using Python, Go, C++, or other programming languages**

You can now program your pet feeder to feed your pet at different times of the day and you can use the vision service to programmatically know if the food bowl is full or empty.
If the food bowl is empty, use the Motor API to turn on the motor for 30 seconds, which will fill up the bowl:

{{< expand "See the entire robot logic in 42 lines" >}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio
import datetime
import os

from viam.robot.client import RobotClient
from viam.components.motor import Motor
from viam.services.vision import VisionClient


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key=os.environ.get("FEEDER_API_KEY"),
        api_key_id=os.environ.get("FEEDER_API_KEY_ID")
    )
    return await RobotClient.at_address(os.environ.get("FEEDER_URI"), opts)


async def main():
    now = datetime.datetime.now()

    if now.hour < 6:
        print("No feeding")
        return 0

    feeder = Motor.from_robot(robot, "feeder")

    bowl = VisionClient.from_robot(robot, "bowl")
    xStart = datetime.datetime.now()
    classifications = await bowl.get_classifications_from_camera("cam", 1)
    xTime = datetime.datetime.now() - xStart
    print(f"bowl classifications return value: {classifications} in {xTime}")

    if len(ret) == 1:
        c = classifications[0]
        if c.class_name == "empty" and c.confidence > 0.5:
            print("Feeding time")
            await feed(feeder)

    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{< /expand >}}

{{% /tablestep %}}
{{< /table >}}

#### Connect to networks of devices, providing comprehensive real-time and historical data

Consider another example where you want to get data from a network of boats.

DIAGRAM

{{< table >}}
{{% tablestep link="/appendix/apis/#component-apis"%}}
{{<imgproc src="/get-started/boat-data.png" class="fill alignright" resize="800x" style="max-width: 600px" declaredimensions=true alt="Screenshot of food bowl pictures with labels">}}

**Real-time camera and sensor data**

Viam can work with existing hardware and, once configured, you have access to real time location, camera feeds, and sensor data.

{{% /tablestep %}}
{{% tablestep link="/appendix/apis/data-client/"%}}

**Real-time and historical data through one API**

Adding data management to that allows you to not just obtain real-time data but also historical data, which is queryable through one API.

{{% expand "Click to view" %}}
Code
{{% /expand%}}

{{% /tablestep %}}
{{< /table >}}

#### Enable efficient fleet-wide software deployment, real-time tracking, and data analysis

{{< table >}}
{{% tablestep link="/appendix/apis/#component-apis"%}}
{{<imgproc src="/get-started/boat-data.png" class="fill alignright" resize="800x" style="max-width: 600px" declaredimensions=true alt="Screenshot of food bowl pictures with labels">}}

**Single user interface**

{{% /tablestep %}}
{{% tablestep link="/appendix/apis/data-client/"%}}

**Debug individual machines**

{{% /tablestep %}}
{{% tablestep link="/appendix/apis/data-client/"%}}

**Code deployment for an entire fleet**

{{% /tablestep %}}

{{< /table >}}
