---
title: "A tour of Viam"
linkTitle: "Tour of Viam"
description: "Viam is a complete software platform for smart machines which provides modular components and services for vision, motion, SLAM, ML, and data management."
weight: 10
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
---

Viam is a software platform that makes it easy to work with hardware and software.
At the core of Viam is the open-source `viam-server` executable which:

- Creates, configures, and maintains any machine on which it is installed
- Securely handles all communications.
- Runs drivers, custom code, and any other software.
- Accepts API requests.
- Runs {{< glossary_tooltip term_id="service" text="services">}} like computer vision, motion planning, data management, machine learning, and more.

`viam-server` **runs on Linux and macOS** and supports a wide variety of popular systems, including:

{{< board-carousel >}}
<br>

## Creating a smart machine with real-time control, monitoring, and data management

{{<imgproc src="/tutorials/pet-treat-dispenser/preview.png" resize="300x" declaredimensions=true alt="Image of a dog interacting with the smart pet feeder." class="alignleft">}}

Consider a pet feeder which is made up of a webcam and a motor as well as a board with the programming for the device.

TODO: Diagram

With the Viam app, you can configure the motor and webcam as {{< glossary_tooltip term_id="component" text="components" >}}.

### Benefits of the Viam platform

By configuring your machine with Viam, you can now:

{{< table >}}
{{% tablestep link="/cloud/machines/#control"%}}
<img src="/get-started/feed.gif" style="max-width:600px" class="fill alignleft">

**Remotely access and control the machine**

Using the Viam app or the Viam mobile app, you can view the camera feed and turn on the motor to feed your pet.

{{% /tablestep %}}
{{% tablestep link="/services/data/"%}}
{{<imgproc src="/get-started/bowl-images.png" class="fill alignleft" resize="800x" style="max-width: 600px" declaredimensions=true alt="Screenshot of food bowl pictures">}}
**Collect and upload data to the cloud**

You can configure the camera to capture a photo of the food bowl periodically and automatically sync these photos to the cloud.

{{% /tablestep %}}
{{% tablestep link="/services/ml/"%}}
{{<imgproc src="/get-started/bowl-label.jpg" class="fill alignright" resize="600x" style="max-width: 200px" declaredimensions=true alt="Screenshot of food bowl pictures with labels">}}
**Use collected data to build data sets and train and Machine Learning models**

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

## Connect to networks of devices, providing comprehensive real-time and historical data

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


## Enable efficient fleet-wide software deployment, real-time tracking, and data analysis

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
