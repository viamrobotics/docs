---
title: "Program your Robot with Viam's SDKs"
linkTitle: "Program your Robot with Viam's SDKs"
weight: 40
type: "docs"
description: "An introduction to Viam's SDKs and how to use them to write code to access and control your robot."
tags: ["client", "sdk"]
---

Viam offers software development kits (SDKs) that wrap the `viam-server` [gRPC](https://grpc.io/) [APIs](https://github.com/viamrobotics/api) and streamline connection, authentication, and encryption.

<img src="../img/SDK-as-client/image1.png" alt="Example diagram showing how a client connects to a robot with Viam. Diagram shows a client as a computer sending commands to a robot. Robot 1 then communicates with other robotic parts over gRPC and WebRTC and communicating that information back to the client."><br>

Use the SDK of your preferred language to write code to control your robots.

Viam currently offers SDKs for the following two languages:

* [Python SDK](https://python.viam.dev/)
* [Go SDK](https://pkg.go.dev/go.viam.com/rdk)

Click on the links above to read more about installation and usage of each SDK.

## Installation

Python:

```shell
pip install viam-sdk
```

Go:

``` shell
go get go.viam.com/rdk/robot/client
```

## Usage

{{% alert title="Note" color="note" %}}

Before you get started, ensure that you:

* Go to [app.viam.com](https://app.viam.com/).

* Create a new robot.

* Go to the **SETUP** tab and follow the instructions there.

* Install either the [Go](https://pkg.go.dev/go.viam.com/rdk) or [Python](https://python.viam.dev/) SDK on your computer.

{{% /alert %}}

{{% alert title="Tip" color="tip" %}}

You can find more examples of Viam's SDKs on the [Python SDK example GitHub repository](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/server/v1) or the [Go SDK example GitHub repository](https://github.com/viamrobotics/rdk/tree/main/examples).

{{% /alert %}}

### Connection Code Snippets

To get starting writing programs with your preferred SDK, navigate to your robot's page on [the Viam app](https://app.viam.com/robots), select the **CODE SAMPLE** tab, select the language (**Python** or **Golang**) and copy the boilerplate code.

These boilerplate connection code snippets import all of the necessary libraries and set up a client connection to your remote or local robot.

Your boilerplate connection code snippet should look similar to this:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='SECRET FROM THE VIAM APP')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
package main

import (
  "context"

  "github.com/edaniels/golog"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/rdk/utils"
  "go.viam.com/utils/rpc"
)

func main() {
  logger := golog.NewDevelopmentLogger("client")
  robot, err := client.New(
      context.Background(),
      "ADDRESS FROM THE VIAM APP",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "SECRET FROM THE VIAM APP",
      })),
  )
  if err != nil {
      logger.Fatal(err)
  }
  defer robot.Close(context.Background())
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())
}
```

{{% /tab %}}
{{< /tabs >}}

### Control Code Snippets

#### Get an Image from a Camera

{{< readfile "/static/include/components/camera-sample.md" >}}

#### Control a Motor

This sends power commands to [motors](/components/motor/) on the robot.

Assumption: Motors called "motor1" and "motor2" are configured as components of your robot.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.components.motor import Motor

robot = await connect() # refer to connect code above
motor1 = Motor.from_robot(robot, "motor1")
motor2 = Motor.from_robot(robot, "motor2")

# power motor1 at 100% for 3 seconds
await motor1.set_power(1)
await asyncio.sleep(3)
await motor1.stop()

# Run motor2 at 1000 rpm for 200 rotations
await motor2.go_for(1000, 200)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
"time"
"go.viam.com/rdk/components/motor"
)

// grab the motors from the robot
m1, err := motor.FromRobot(robot, "motor1")
m2, err := motor.FromRobot(robot, "motor2")

// power motor1 at 100% for 3 seconds
m1.SetPower(context.Background(), 1, nil)
time.Sleep(3 * time.Second)
m1.Stop(context.Background(), nil)

// Run motor2 at 1000 RPM for 200 rotations
m2.GoFor(context.Background(), 1000, 200, nil)
```

{{% /tab %}}
{{< /tabs >}}

#### Control a Sensor

This example code reads values from a [sensor](/components/sensor/) (an ultrasonic sensor in this example) connected to a robot.

Assumption: A sensor called "ultra1" is configured as a component of your robot.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.components.sensor import Sensor
robot = await connect()
sensor = Sensor.from_robot(robot, "ultra1")
distance = await sensor.get_readings()["distance"]
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
"go.viam.com/rdk/components/sensor"
)

ultra, err := sensor.FromRobot(robot, "ultra1")
distance, err := ultra.Readings(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

#### Use the Viam Vision Service

The following code gets the robot's [Vision Service](https://python.viam.dev/autoapi/viam/services/vision/index.html?highlight=vision#module-viam.services.vision) and then runs a detection model on an image to get a list of detections from the image.

Assumption: A camera called "camera0" and a Vision Service called "detector_1" are configured as a component and a service on your robot.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionServiceClient

robot = await connect()
vision = VisionServiceClient.from_robot(robot)
detections = await vision.get_detections_from_camera("camera_0", "detector_1")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
"go.viam.com/rdk/services/vision"
)

// gets Viam's Vision Service to add a TF-Lite model for person detection
visionSrv, err := vision.FirstFromRobot(r)

// get detection bounding boxes
detections, err := visionSrv.Detections(context.Background(), img, "find_objects")
```

{{% /tab %}}
{{< /tabs >}}

## Run Your Code

After saving the above code as a new `.py` or `.go` file, run this program you've written to control your Viam-connected robot!

Navigate to your computer's terminal and run the following commands, editing the example filepath `~/myCode/myViamFile` to match the path to your file on your computer:

* Python: `python ~/myCode/myViamFile.py`
* Go: `go run ~/myCode/myViamFile.py`

## Next Steps

You can also use the Viam SDKs to create custom components and provide additional functionality to a robot.
See [Extend Viam](../extend/modular-resources/) for more information.
