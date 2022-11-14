---
title: "Using Our SDKs for a Client Application"
linkTitle: "SDKs as Client"
weight: 99
type: "docs"
description: "An introduction to Viam's SDKs and how to use them to access and control your robot."
---

Viam offers SDKs in popular languages which wrap the viam-server [gRPC](https://grpc.io/) APIs and streamline connection, authentication, and encryption against a server.
Using the SDK, you will be able to quickly write code to control and automate your robot(s).

Viam-server exposes gRPC [APIs for robot controls](https://github.com/viamrobotics/api).
It also supports [WebRTC](https://webrtcforthecurious.com/) connectivity and authentication over those APIs.

SDKs make it easier to interface with the robot without calling the gRPC API directly.

<img src="../img/SDK-as-client/image1.png" alt ="Example diagram showing how a client connects to a robot with Viam. Diagram shows a client as a computer sending commands to a robot. Robot 1 then communicates with other robotic parts over gRPC and WebRTC and communicating that information back to the client." width="100%"><br>

## Viam's Client SDK Libraries

Viam's Client SDKs support several ways to connect and control your robots, with many new ways to connect coming soon.

- [Python SDK](https://python.viam.dev/)

- [Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme)

## Quick Start Examples

{{% alert title="Note" color="note" %}}

Before you get started, ensure that you:

- Go to [app.viam.com](https://app.viam.com/).

- Create a new robot.

- Go to the **SETUP** tab and follow the instructions there.

- Install either the [Go](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme) or [Python](https://python.viam.dev/) SDK on your computer.

{{% /alert %}}

{{% alert title="Tip" color="tip" %}}

You can find more examples of Viam's SDKs on the [Python SDK example GitHub repository](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/server/v1) or the [Golang SDK example GitHub repository](https://github.com/viamrobotics/rdk/tree/main/examples).

{{% /alert %}}

### How to connect to your robot with Viam

The easiest way to get started writing an application with Viam, is to navigate to the [robot page on the Viam app](https://app.viam.com/robots), select the **Connect** tab, and copy the boilerplate code from the section labeled **Python SDK** or **Golang SDK**. These code snippets imports all the necessary libraries and sets up a connection with the Viam app in the cloud.

The SDK connect script should look something like this:

{{< tabs >}}
{{% tab name="Python" %}}

```python
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

```go
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

### How to get an image from a camera with Viam

This reads a single image from a [camera](https://docs.viam.com/components/camera/) called "camera0" on the robot.

Assumption: A camera called "camera0" is configured as a component of your robot.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.camera import Camera

robot = await connect() # refer to connect code above
camera = Camera.from_robot(robot, "camera0")
image = await camera.get_image()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
"go.viam.com/rdk/components/camera"
)

// grab the camera from the robot
cameraName := "camera0" // make sure to use the same name as in the json/APP
cam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// gets the stream from a camera
camStream, err := cam.Stream(context.Background())

// gets an image from the camera stream
img, release, err := camStream.Next(context.Background())
defer release()
```

{{% /tab %}}
{{< /tabs >}}

### How to use a motor with Viam

This sends power commands to [motors](https://docs.viam.com/components/motor/) on the robot.

Assumption: Motors called "motor1" and "motor2" are configured as components of your robot.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.motor import Motor

robot = await connect() # refer to connect code above
motor1 = Motor.from_robot(robot, "motor1")
motor2 = Motor.from_robot(robot, "motor2")

# power motor1 at 100% for 3 seconds
await motor1.set_power(1)
await asyncio.sleep(3)
await motor1.stop()   

# run motor2 at 1000 rpm for 200 rotations
await motor2.go_for(1000, 200)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
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

// run motor2 at 1000 RPM for 200 rotations
m2.GoFor(context.Background(), 1000, 200, nil)
```

{{% /tab %}}
{{< /tabs >}}

### How to use a sensor with Viam

This example code reads values from a [sensor](https://docs.viam.com/components/sensor/) (an ultrasonic sensor in this example) connected to a robot.

Assumption: A sensor called "ultra1" is configured as a component of your robot.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.sensor import Sensor
robot = await connect()
sensor = Sensor.from_robot(robot, "ultra1")
distance = await sensor.get_readings()["distance"]
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
"go.viam.com/rdk/components/sensor"
)

ultra, err := sensor.FromRobot(robot, "ultra1")
distance, err := ultra.Readings(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

### How use the Viam vision service

The following code gets the robot's [vision service](https://python.viam.dev/autoapi/viam/services/vision/index.html?highlight=vision#module-viam.services.vision) and then runs a detection model on an image to get a list of detections from the image.

Assumption: A camera called "camera0" and a vision service called "detector_1" are configured as a component and a service on your robot.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.vision import VisionServiceClient
                                                                   
robot = await connect()
vision = VisionServiceClient.from_robot(robot)
detections = await vision.get_detections_from_camera("camera_0", "detector_1")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
"go.viam.com/rdk/services/vision"
)

// gets Viam's vision service to add a TF-Lite model for person detection
visionSrv, err := vision.FirstFromRobot(r)

// get detection bounding boxes
detections, err := visionSrv.Detections(context.Background(), img, "find_objects")
```

{{% /tab %}}
{{< /tabs >}}
