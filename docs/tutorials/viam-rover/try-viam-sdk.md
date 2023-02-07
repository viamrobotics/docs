---
title: "Drive the Viam Rover with the Viam SDK"
linkTitle: "Drive with the SDK"
weight: 40
type: "docs"
description: "Try Viam by using the Viam SDK to make your Viam Rover move in a square."
tags: ["base", "viam rover", "try viam", "sdk"]
---
The Viam SDKs allow you to write code in either Python or Golang to control a [Viam Rover](https://app.viam.com/try).
You can follow this tutorial with a [rented Viam Rover](https://app.viam.com/try) or with [your own Viam Rover](/try-viam/rover-resources/).

<img src="../../img/try-viam-sdk/image1.gif" alt="Overhead view of the Viam Rover showing it as it drives in a square." width="100%"><br>

{{< alert title="Tip" color="tip" >}}
You can also directly see the [complete code for the tutorial](#complete-code).
{{< /alert >}}

## Install a Viam SDK

Install either the [Viam Python SDK](https://python.viam.dev/) or the [Viam Golang SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme) on your local computer.

{{< alert title="Tip" color="tip" >}}
If you are [renting your rover](https://app.viam.com/try), we recommend that you get the Viam SDK set up before your reservation starts.
This way, you can maximize the amount of time you have using the Viam Rover.

If you are running out of time during your rental, you can [extend your rover rental](/try-viam/try-viam-tutorial/#extending-time) as long as there are no other reservations.
{{< /alert >}}

## Connect to your Viam Rover

The easiest way to get started writing an application with Viam is to navigate to the [robot page on the Viam App](https://app.viam.com/robots), select the **CODE SAMPLE** tab, and copy the boilerplate code from the section labeled **Python** or **Golang**.

These code snippets import all the necessary libraries and set up a connection with the Viam app in the cloud.

Next, create a file named <file>square.py</file> or <file>square.go</file> and paste the boilerplate code from the **CODE SAMPLE** tab of the Viam app into your file.
Then, save your file.

Run the code to verify that the Viam SDK is properly installed and that the `viam-server` instance on your robot is live.

You can run your code by typing the following into your terminal:

{{< tabs >}}
{{% tab name="Python" %}}

```bash
python3 square.py
```

{{% /tab %}}
{{% tab name="Go" %}}

If using Golang, you need to initialize your project, and install the necessary libraries before running the program.

```bash
go mod init square
go mod tidy
go run square.go
```

{{% /tab %}}
{{< /tabs >}}

If you successfully configured your robot and it is able to connect to the Viam app, the program you ran prints the names of your rover's resources to the terminal.
These are the components and services that the roobot is configured with in the Viam app.

<img src="../../img/try-viam-sdk/image3.png" alt="The output of the program is an array of resources that have been pulled from the Viam app. Some of these are the Vision Service, Data Manager, and Board." width="100%"><br>

{{% alert title="Tip" color="tip" %}}

If you are [renting your rover](https://app.viam.com/try), and your reservation ends before you have completed this tutorial, change the connection information (the robot address and the payload) to connect to your new rover and continue.

{{% /alert %}}

## Drive your rover in a square

Now that you have connected the rover to Viam with the SDK, you can start writing code to control the Viam Rover.
The following code moves the Viam Rover in a square:

{{< tabs >}}
{{% tab name="Python" %}}

The first thing you need to do is import the [base component](https://python.viam.dev/autoapi/viam/components/base/index.html#module-viam.components.base).
The base is responsible for controlling the motors attached to the base of the rover.
Add the following line of code to your imports:

```python
from viam.components.base import Base
```

Next, you need to initialize your Viam Rover base.

In the main function, after you connect, paste the code from line 5.
By default, the base name is `viam_base`.
If you have changed the base name, update the name in your code.

Your main function should look like this:

```python {class="line-numbers linkable-line-numbers" data-line="5"}
async def main():
    robot = await connect()

    # Get the base component from the Viam Rover
    roverBase = Base.from_robot(robot, 'viam_base')

    await robot.close()
```

Now that your Viam Rover base is initialized, you can write code to drive it in a square.
Paste this snippet above your `main()` function:

```python
async def moveInSquare(base):
    for _ in range(4):
        # moves the Viam Rover forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        print("move straight")
        # spins the Viam Rover 90 degrees at 100 degrees per second
        await base.spin(velocity=100, angle=90)
        print("spin 90 degrees")
```

Invoke the `moveInSquare()` function in your main function after initializing your base.

Your main function should now look like this:

```python {class="line-numbers linkable-line-numbers" data-line="8"}
async def main():
    robot = await connect()

    # Get the base component from the Viam Rover
    roverBase = Base.from_robot(robot, 'viam_base')

    # Move the Viam Rover in a square
    await moveInSquare(roverBase)

    await robot.close()
```

{{% /tab %}}
{{% tab name="Golang" %}}

The first thing you need to do is import the [base component](https://pkg.go.dev/go.viam.com/rdk@v0.2.4/components/base#Base).
The base is responsible for controlling the motors attached to the base of the rover.
Add the following line of code to your imports before:

```go {class="line-numbers linkable-line-numbers" data-line="3"}
import (
    // Be sure to keep all of the other imported libraries
    "go.viam.com/rdk/components/base"
)
```

Next, you need to initialize your Viam Rover base.

In the main function, after you connect, paste the code from lines 19-22.
By default, the base name is `viam_base`.
If you have changed the base name, update the name in your code.

Your main function should look like this:

```go {class="line-numbers linkable-line-numbers" data-line="19-22"}
func main() {
    logger := golog.NewDevelopmentLogger("client")
    robot, err := client.New(
        context.Background(),
        "ADDRESS_FROM_VIAM_APP",
        logger,
        client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
            Type: utils.CredentialsTypeRobotLocationSecret,
            Payload: "SECRET_FROM_VIAM_APP",
        })),
    )
    if err != nil {
        logger.Fatal(err)
    }

    defer robot.Close(context.Background())

    // Get the base from the Viam Rover
    roverBase, err := base.FromRobot(robot, "viam_base")
    if err != nil {
        ogger.Fatalf("cannot get base: %v", err)
    }
}
```

Now that your Viam Rover base has been initialized, you can write code to drive it in a square.
Paste this snippet above your `main()` function:

```go
func moveInSquare(ctx context.Context, base base.Base, logger golog.Logger) {
    for i := 0; i < 4; i++ {
        // moves the Viam Rover forward 600mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        logger.Info("move straight")
        // spins the Viam Rover 90 degrees at 100 degrees per second
        base.Spin(ctx, 90, 100.0, nil)
        logger.Info("spin 90 degrees")
  }
}
```

Invoke the `moveInSquare()` function in your main function after initializing your base.

Your main function should now look like this:

```go {class="line-numbers linkable-line-numbers" data-line="10"}
func main() {
    // Connect rover to Viam...
    // Get the base from the Viam Rover
    roverBase, err := base.FromRobot(robot, "viam_base")
    if err != nil {
        logger.Fatalf("cannot get base: %v", err)
    }

    // Move the Viam Rover in a square
    moveInSquare(context.Background(), roverBase, logger)
}
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Tip" color="tip" >}}
If you are [renting your rover](https://app.viam.com/try), go to the **CONTROL** tab, and make sure you can monitor the camera feed from your rover.
{{< /alert >}}

When you run your code, your robot moves in a square.

<img src="../../img/try-viam-sdk/image2.gif" alt="Overhead view of the Viam Rover showing it as it drives in a square on the left, and on the right, a terminal window shows the output of running the square function as the rover moves in a square." width="100%"><br>

## Complete Code

This is the complete code for the tutorial:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.components.base import Base
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='SECRET_FROM_VIAM_APP')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('ADDRESS_FROM_VIAM_APP', opts)

async def moveInSquare(base):
    for _ in range(4):
        # moves the Viam Rover forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        print("move straight")
        # spins the Viam Rover 90 degrees at 100 degrees per second
        await base.spin(velocity=100, angle=90)
        print("spin 90 degrees")

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    roverBase = Base.from_robot(robot, 'viam_base')

    # Move the Viam Rover in a square
    await moveInSquare(roverBase)

    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Golang" %}}

```go {class="line-numbers linkable-line-numbers"}
package main

import (
    "context"

    "github.com/edaniels/golog"
    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
    "go.viam.com/utils/rpc"
)

func moveInSquare(ctx context.Context, base base.Base, logger golog.Logger) {
    for i := 0; i < 4; i++ {
        // moves the Viam Rover forward 600mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        logger.Info("move straight")
        // spins the Viam Rover 90 degrees at 100 degrees per second
        base.Spin(ctx, 90, 100.0, nil)
        logger.Info("spin 90 degrees")
    }
}

func main() {
    logger := golog.NewDevelopmentLogger("client")
    robot, err := client.New(
        context.Background(),
        "ADDRESS_FROM_VIAM_APP",
        logger,
        client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
            Type:    utils.CredentialsTypeRobotLocationSecret,
            Payload: "SECRET_FROM_VIAM_APP",
        })),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer robot.Close(context.Background())

    // Get the base from the Viam Rover
    roverBase, err := base.FromRobot(robot, "viam_base")
    if err != nil {
        logger.Fatalf("cannot get base: %v", err)
    }

    moveInSquare(context.Background(), roverBase, logger)
}
```

{{% /tab %}}
{{< /tabs >}}

## Next Steps

If you're ready for more, try making your rover move in different ways.
Can you make it move in a circle?
A figure-eight?
You could also write some code to control the other components on the Viam Rover, like the [camera](/components/camera/), or the rover's [motors](/components/motor/).

Or [add color detection to your Rover](/tutorials/viam-rover/try-viam-color-detection/).

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, be sure to head over to the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw).
