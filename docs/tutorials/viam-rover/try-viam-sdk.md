---
title: "Drive the Viam Rover with the Viam SDK"
linkTitle: "Drive with the SDK"
weight: 40
type: "docs"
description: "Try Viam by using the Viam SDK to make your Viam Rover move in a square."
tags: ["base", "viam rover", "try viam", "sdk"]
---

Hopefully you have had a chance to play around with the Viam Rover using the [Try Viam](https://app.viam.com/try) feature, and now you are ready to control your rover with code!
In this tutorial, we will introduce you to the Viam SDK (software development kit) so that you can write code in either Python or Golang to make your [Viam Rover](https://app.viam.com/try) move in a square.
This is a great way to get a feel for what it's like to write code to control your robots using Viam.

<img src="../../img/try-viam-sdk/image1.gif" alt="Overhead view of the Viam rover showing it as it drives in a square." width="100%"><br>

## How to install a Viam SDK

In this step, you are going to install either the [Viam Python SDK](https://python.viam.dev/) or the [Viam Golang SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme) on your local computer.
We recommend that you get the Viam SDK set up before your reservation starts.
This way, you can maximize the amount of time you have using the Viam Rover.

Use whichever programming language you are most comfortable with.

{{% alert title="Note" color="note" %}}

Refer to the appropriate SDK documentation for SDK installation instructions.

- [Viam Python SDK](https://python.viam.dev/)
- [Viam Golang SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme)

{{% /alert %}}

## How to connect your Viam Rover to the Viam SDK

The easiest way to get started writing an application with Viam is to navigate to the [robot page on the Viam App](https://app.viam.com/robots), select the **CODE SAMPLE** tab, and copy the boilerplate code from the section labeled **Python** or **Golang**.

These code snippets import all the necessary libraries and set up a connection with the Viam app in the cloud.

Next, paste the boilerplate code from the **CODE SAMPLE** tab of the Viam app into a file named <file>square.py</file> or <file>square.go</file> file in your code editor, and save your file.

Now run the code to verify that the Viam SDK is properly installed and that the `viam-server` instance on your robot is live.

You can run your code by typing the following into the terminal:

{{< tabs >}}
{{% tab name="Python" %}}

```bash
python3 square.py
```

{{% /tab %}}
{{% tab name="Go" %}}

If using Golang, you will need to initialize your project, and install the necessary libraries.

```bash
go mod init square
go mod tidy
go run square.go
```

{{% /tab %}}
{{< /tabs >}}

If you successfully configured your robot and it is able to connect to the Viam app, you should see something like this printed to the terminal after running your program.
What you see here is a list of the various resources, components, and services that have been configured to your robot in the Viam app.

<img src="../../img/try-viam-sdk/image3.png" alt="A screenshot from the terminal that prints the output of print(robot.resource_names) when your Viam Rover has correctly connected and initialized with the Viam app. The output is an array of resources that have been pulled from the Viam app. Some of these are the Vision Service, Data Manager, and Board." width="100%"><br>

{{% alert title="Tip" color="tip" %}}

If you have any issues whatsoever getting the Viam SDK set up or getting your code to run on your computer, the best way to get help is over on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw).
There you will find a friendly developer community of people learning how to make robots using Viam.

{{% /alert %}}

## How to make your rover drive in a square using the Viam SDK

Now that you have connected the rover to Viam with the SDK, we can start writing code to control the Viam Rover.
You are going to write a program that will move the Viam rover in a square.

{{< tabs >}}
{{% tab name="Python" %}}

The first thing you need to do is import the [base component](https://python.viam.dev/autoapi/viam/components/base/index.html#module-viam.components.base).
The base is responsible for controlling the motors attached to the base of the rover.

```python
from viam.components.base import Base
```

{{% /tab %}}
{{% tab name="Golang" %}}

The first thing you need to do is import the [base component](https://pkg.go.dev/go.viam.com/rdk@v0.2.4/components/base#Base) from the Viam Golang SDK.
The base is responsible for controlling the motors attached to the base of the rover.

```go
import (
    // Be sure to keep all of the other imported libraries
    "go.viam.com/rdk/components/base"
)
```

{{% /tab %}}
{{< /tabs >}}

Next, you will need to initialize your Viam Rover base.

In the main function, after you connect, paste the following, while ensuring that the name matches the name of the Viam Rover base.
By default, the base name is `viam_base`.
Your main function should look like this:

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def main():
  robot = await connect()

  print('Resources:')
  print(robot.resource_names)

  # Get the base component from the Viam Rover
  roverBase = Base.from_robot(robot, 'viam_base')

  await robot.close()
```

{{% /tab %}}
{{% tab name="Golang" %}}

```go
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
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Get the base from the Viam rover
  roverBase, err := base.FromRobot(robot, "viam_base")
  if err != nil {
    logger.Fatalf("cannot get base: %v", err)
  }
}
```

{{% /tab %}}
{{< /tabs >}}

Now that your Viam Rover base has been initialized, you can write code to drive it in a square.
Paste this snippet above your `main()` function:

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def moveInSquare(base):
  for _ in range(4):
    # moves the Viam Rover forward 500mm at 500mm/s
    await base.move_straight(velocity=500, distance=500)
    # spins the Viam Rover 90 degrees at 100 degrees per second
    await base.spin(velocity=100, angle=90)
```

{{% /tab %}}
{{% tab name="Golang" %}}

```go
func moveInSquare(ctx context.Context, base base.Base) {
  for i:=0; i<4; i++ {
    // moves the Viam Rover forward 600mm at 500mm/s
    base.MoveStraight(ctx, 600, 500.0, nil)
    // spins the Viam Rover 90 degrees at 100 degrees per second
    base.Spin(ctx, 90, 100.0, nil)
  }
}
```

{{% /tab %}}
{{< /tabs >}}

You can run this code by invoking the `moveInSquare()` function below where you initialized your base.
Your main function should now look like this:

{{< tabs >}}
{{% tab name="Python" %}}

```python
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

```go
func main() {
  // Connect rover to Viam...
  // Get the base from the Viam rover
  roverBase, err := base.FromRobot(robot, "viam_base")
  if err != nil {
    logger.Fatalf("cannot get base: %v", err)
  }

  // Move the Viam Rover in a square
  moveInSquare(context.Background(), roverBase)
}
```

{{% /tab %}}
{{< /tabs >}}

Now, go to the **CONTROL** tab, and make sure you can monitor the camera feed from your rover.
When you run your code, you should be able to see your robot move in a square.

<img src="../../img/try-viam-sdk/image2.gif" alt="Overhead view of the Viam rover showing it as it drives in a square on the left, and on the right, a terminal window shows the output of running the square function as the rover moves in a square." width="100%"><br>

## Next Steps

In this tutorial, we showed you how to set up the Viam SDK so that you can control the Viam Rover remotely.

If you're ready for more, try making your rover move in different ways.
Can you make it move in a circle?
A figure-eight?
You could also write some code to control the other components on the Viam Rover, like the [camera](/components/camera/), or the rover's [motors](/components/motor/).
You could also control Viam's services, by adding [data management](/services/data-management/) to collect data in real time or [vision services](/services/vision/) to add color detection to your Rover.
If you are ready to start building your own robots with Viam, you should pick up a Raspberry Pi and try building one of Viam's introductory robots on the [tutorials page in our documentation](/tutorials/).

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, be sure that you head over to the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw).
