---
title: "Build a Mock Robot"
linkTitle: "Build a Mock Robot"
weight: 41
type: "docs"
description: "Create a mock robot using just your personal computer to try using Viam without any robotic hardware."
webmSrc: "/tutorials/img/build-a-mock-robot/mock-robot.webm"
mp4Src: "/tutorials/img/build-a-mock-robot/mock-robot.mp4"
images: ["/tutorials/img/build-a-mock-robot/mock-robot.gif"]
videoAlt: "A mock arm's joint positions from the control tab of the Viam app."
aliases:
    - /tutorials/build-a-mock-robot/
tags: ["mock", "simulation"]
---

## Introduction

In this post, we will show you how to build a mock robot using just your personal laptop so you can try using Viam without any robotic hardware.
This is a great way to learn how to build robots [the Viam way](/viam).

Most Viam components come with a _fake_ model that can be useful when testing.
These fake components interact with Viam like real hardware, but of course, do not actually exist.
We will be using these fake components to build out a mock robot and explore how to use Viam.

In this tutorial, you will set up, control, and program a mock robotic arm and a mock sub-part with a motor using fake components.

## What you'll need for this guide

- A laptop or desktop running Linux or macOS.
- [Go](https://go.dev/doc/install) or [Python 3.9+](https://www.python.org/downloads/).
- A code editor of your choice.
- If you are running macOS, ensure you have [Homebrew](https://brew.sh/) installed and up to date on your Mac.

## How to set up a mock robot

### Set up your account on the Viam app

The first thing you need to do is set up your account on the Viam app.
Go to [app.viam.com](https://app.viam.com) and sign up.

### Configure your mock robot

1. Go to [app.viam.com](https://app.viam.com/).
2. Create a new robot.
3. Go to the **config** tab.
4. Configure the arm:

   - Create a new component called `myArm` with **Type** `arm` and **Model** `fake`.
   - Add the following attribute:

      ```json
      {
          "arm-model": "ur5e"
      }
      ```

5. Configure the motor:

   - Create a new component called `myMotor` with **Type** `motor` and **Model** `fake`.

6. Save the configuration.

You will need to reference both component names later when you connect to your mock robot with the Python SDK.

### How to install `viam-server` on your computer

Before you proceed with controlling your mock robot, you are going to need to install `viam-server` on your development machine.

Follow the steps outlined on the **setup** tab of the Viam app in order to install `viam-server` on your local computer.

## Controlling your mock robot using the Viam app

When you add the fake motor and arm components to your robot, the Viam app automatically generates a UI for your motor and arm under the **control** tab.

<img src="../../img/build-a-mock-robot/image3.png" alt="Screenshot from the Viam app showing the CONTROL tab with the fake arm, and motor components." width="100%">

If you were configuring a real motor and arm, you would be able to control it from this section of the app.
You could do things like control the direction and speed of the motor, and change the joint positions of your robotic arm.
However, since we are building a mock robot using fake components, you will only see the robot's reported positions and speeds change from the UI.
You will not be able to see your robot move in the physical world.

Next, you will install a Viam SDK so you can write custom logic to control the mock robot.

## Controlling your mock robot using a Viam SDK

### How to install a Viam SDK

In this step, you are going to install either the [Viam Python SDK](https://python.viam.dev/) (Software Development Kit) or the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk). Use which ever programming language you are most comfortable with.

{{% alert title="Note" color="note" %}}

Refer to the appropriate SDK documentation for SDK installation instructions.

- [Viam Python SDK](https://python.viam.dev/)
- [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk)

{{% /alert %}}

{{% alert title="Tip" color="tip" %}}
{{< snippet "social.md" >}}
There, you will find a friendly developer community of people learning how to make robots using Viam.
{{% /alert %}}

### How to connect to your mock robot with the Viam SDK

The easiest way to get started writing an application with Viam is to navigate to the [robot page on the Viam app](https://app.viam.com/robots), select the **code sample** tab, and copy the boilerplate code from the section labeled **Python SDK** or **Go SDK**.
These code snippets import all the necessary libraries and set up a connection with the Viam app in the cloud.
Next, paste that boilerplate code from the **code sample** tab of the Viam app into a file named <file>index.py</file> or <file>index.go </file>file in your code editor, and save your file.

{{< readfile "/static/include/snippet/secret-share.md" >}}

You can now run the code.
Doing so verifies that the Viam SDK is properly installed, that the `viam-server` instance on your robot is live, and that the computer running the program is able to connect to that instance.

You can run your code by typing the following into the terminal:

{{< tabs >}}
{{% tab name="Python" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python3 index.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go run index.go
```

{{% /tab %}}
{{< /tabs >}}

If you successfully configured your robot and it is able to connect to the Viam app you should see something like this printed to the terminal after running your program.
What you see here is a list of the various resources (Like components, and services) that have been configured to your robot in the Viam app.

<img src="../../img/build-a-mock-robot/image1.png" alt="A screenshot from the Visual Studio Code command line that prints the output of print(robot.resource_names) when your Raspberry Pi has correctly connected and initialized with the Viam app. The output is an array of resources that have been pulled from the Viam app. Some of these are the Vision Service, Data Manager, and Board." width="100%">

### How to control your mock robot

Next, you will be writing some code to control and move your mock robotic arm.
We are going to write a program that will move the mock robotic arm into a new random position every second.
You will be able to verify that your mock robotic arm is working by checking that the joint positions of the fake arm in the **control** tab of the Viam app are changing.

At the top of your <file>index.py</file> file, paste the following:

{{< tabs >}}
{{% tab name="Python" %}}

The first thing you need to do is import the [arm component](https://python.viam.dev/autoapi/viam/components/arm/client/index.html) from the Viam Python SDK, and the [random](https://docs.python.org/3/library/random.html) and [async.io](https://docs.python.org/3/library/asyncio.html) libraries.

```python {class="line-numbers linkable-line-numbers"}
from viam.components.arm import ArmClient, JointPositions
import random
import asyncio
```

{{% /tab %}}
{{% tab name="Go" %}}

The first thing you need to do is import the [arm component](https://github.com/viamrobotics/rdk/blob/main/components/arm/client.go) from the Viam Go SDK, and the [random](https://pkg.go.dev/math/rand) and [time](https://pkg.go.dev/time) libraries.

```go {class="line-numbers linkable-line-numbers"}
import (
  "fmt"
  "math/rand"
  "time"
  componentpb "go.viam.com/api/component/arm/v1"
  "go.viam.com/rdk/components/arm"
)
```

{{% /tab %}}
{{< /tabs >}}

Next, you will need to initialize your fake robotic arm.
In the main function, paste the following, while ensuring that the name of your fake arm matches the arm named in your config file.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
arm = ArmClient.from_robot(robot=robot, name='my_main_arm')
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_main_arm")
if err != nil {
    logger.Fatalf("cannot get arm: %v", err)
}
```

{{% /tab %}}
{{< /tabs >}}

Now that your mock arm has been initialized, you can write some code to control it.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Gets a random position for each servo on the arm that is within the safe range of motion of the arm. Returns a new array of safe joint positions.
def getRandoms():
    return [random.randint(-90, 90),
    random.randint(-120, -45),
    random.randint(-45, 45),
    random.randint(-45, 45),
    random.randint(-45, 45)]

# Moves the arm into a new random position every second
async def randomMovement(arm: ArmClient):
    while (True):
        randomPositions = getRandoms()
        newRandomArmJointPositions = JointPositions(values=randomPositions)
        await arm.move_to_joint_positions(newRandomArmJointPositions)
        print(await arm.get_joint_positions())
        await asyncio.sleep(1)
    return
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Returns an array of random floats between two numbers
func getRandoms(min, max float64) []float64 {
    res := make([]float64, 5)
    for i := range res {
        res[i] = min + rand.Float64() * (max - min)
    }
    return res
}

// Moves the arm into a new random position every second
func randomMovement (ctx context.Context, a arm.Arm ) {
  for {
    randomPositions := getRandoms(-90, 90)
    newRandomArmJointPositions := &componentpb.JointPositions{Values: randomPositions}
    a.MoveToJointPositions(ctx, newRandomArmJointPositions, nil)
    fmt.Println(a.JointPositions(ctx, nil))
    time.Sleep(1 * time.Second)
  }
}
```

{{% /tab %}}
{{< /tabs >}}

You can run this code by invoking this function located below your arm initialization in main.
Your main function, should look like this:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    arm = ArmClient.from_robot(robot=robot, name='my_main_arm')
    await randomMovement(arm)

    await robot.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
func main() {
  // Connect to the robot...
  myArm, err := arm.FromRobot(robot, "my_main_arm")
  if err != nil {
    logger.Fatalf("cannot get arm: %v", err)
  }
  randomMovement(context.Background(), myArm)
}
```

{{% /tab %}}
{{< /tabs >}}

Now when you run this code, you should see the new mock arm positions listed in the command line, if you open the **control** tab of your mock robot, you should see the robot's arm positions changing in real-time along with the code on your development machine.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="../../img/build-a-mock-robot/image2.webm" mp4_src="../../img/build-a-mock-robot/image2.mp4" alt="A terminal window with 'python3 index.py' being run, then a list of four values is printed each second to the terminal. On the left side, is the mock arm from the CONTROL tab of the Viam app. As the joint positions are updated in the terminal from the left, you can see that the joint positions are updated in realtime on the Viam app.">}}
</div>

## How to create a mock sub-part

Now that you have your mock robotic arm working, let's add a mock sub-part to your robot.

### What is a part?

A _robot_ in Viam is one or more computers combined into one logical robot.
The bounds of a robot are usually pretty clear, but can be subjective.
However, it's possible with Viam to create a robot that is made up of multiple computers.
Each of these computer-controlled units is referred to as a _part_.
Most simple robots will have only one part, but can have as many parts as needed.

Parts are organized in a tree, with one of them being the _main_ part, and the others being _sub-parts_.
You can access any sub-part either directly, or through any part above it in the tree.
Each part runs a single `viam-server` instance.

## How to configure a sub-part in the Viam app

On your robot's page on the Viam app, click on the dropdown next to the main part, name your part and click **Add new**.

<img src="../../img/build-a-mock-robot/image5.png" alt="Screenshot of the Viam app with a dropdown below the main part. 'SubPart' is written in the textbox." width="100%">

You will be creating a mock independent computer-controlled sub-part with a motor.
This could be anything, but let's say for the purpose of this tutorial that this motor controls a conveyor belt in front of our mock arm on an assembly line.

Navigate to your new part's **config** page and create a new motor using the **fake** model.

### How to add your sub-part as a remote

Connecting your sub-part as a remote from your main robot will allow you to control your sub-parts all from one place inside of your main robot.

From the **code sample** tab of your sub-part:

- Copy the **Config as Remote Part**.
- Navigate back to the **config** and then the **Remotes** tab of your main robot
- Paste your sub-part's configuration.

<img src="../../img/build-a-mock-robot/image8.png" alt="Screenshot from the Viam app showing the CONFIG > REMOTES with the sub-part's remote config file pasted in." width="80%">

### How to start a new instance of `viam-server` for your mock sub-part

Since every part needs to run an instance of `viam-server`, you will need to bind the sub-part to a new port so we can run two servers on your machine at the same time.
We are using port `8081`, but you can use any open port you want.

You can do this by going to **config** and then going to the **Auth/Network** tab.
Here, you will paste the following:

```json {class="line-numbers linkable-line-numbers"}
{
    "bind_address": "localhost:8081"
}
```

Be sure to save before continuing.

### How to run a second instance of `viam-server` for your sub-part

In the upper right corner of the **setup** tab, click **Copy viam-server config**.

<img src="../../img/build-a-mock-robot/image9.png" alt="Screenshot from the Viam app showing the 'Copy Viam-Server Config' button highlighted by a red box.">

On your local machine, create a new file called <file>viam-sub-part.json</file>, then paste the contents of your server config into that file and save.
From the terminal, navigate to the directory where you saved the config file, and run this command to create a new instance of `viam-server` using this configuration.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam-server -config viam-sub-part.json
```

If you have two instances of `viam-server` running on your local machine, you should be able to see both your main robot arm and your new mock sub motor listed on your main robots **control** tab.

![Screenshot of the Viam app's Control tab for the main part that lists the main arm, and the sub motor part.](../../img/build-a-mock-robot/image6.png)

## How to control a sub-part using the Viam SDK

Now that you have your mock sub-part connected as a remote to your main mock robot, you will be able to control all of your sub-part's components and services with Viam's Python SDK.
In fact, if you run your Python script again, and you review the output of `print(robot.resource_names)`, you will see that your sub-part's motor will now be listed as an available resource for you to use.

{{< tabs >}}
{{% tab name="Python" %}}

To control your sub-part's motor, you will need to import the [Motor Client](https://python.viam.dev/autoapi/viam/components/motor/client/index.html).
Paste this at the top of your file:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.motor import MotorClient
```

{{% /tab %}}
{{% tab name="Go" %}}

To control your sub-part's motor, you will need to import the [Motor Client](https://github.com/viamrobotics/rdk/blob/main/components/motor/client.go). Paste this at the top of your file:

```go {class="line-numbers linkable-line-numbers"}
import (
  "go.viam.com/rdk/components/motor"
)
```

{{% /tab %}}
{{< /tabs >}}

Now in your main function, you will need to instantiate your mock sub motor.
Be sure that your motor's name matches the one that you have listed in your robot's resource names.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
motor = MotorClient.from_robot(robot=robot, name='sub-part:my_sub_motor')
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myMotor, err := motor.FromRobot(robot, "my_sub_motor")
if err != nil {
  logger.Fatalf("cannot get motor: %v", err)
}
```

{{% /tab %}}
{{< /tabs >}}

Let's write a function that toggles your mock sub motor on and off every second.
You can do that with this function.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Toggles the motor on and off every second
async def toggleMotor(motor: MotorClient):
    while (True):
        await motor.set_power(1)
        print("go")
        await asyncio.sleep(1)
        await motor.stop()
        print("stop")
        await asyncio.sleep(1)
    return
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Toggles the motor on and off every second
func toggleMotor (ctx context.Context, m motor.Motor) {
  for {
    m.SetPower(ctx, 1, nil)
    fmt.Println("go")
    time.Sleep(1 * time.Second)
    m.Stop(ctx, nil)
    fmt.Println("stop")
    time.Sleep(1 * time.Second)
  }
}
```

{{% /tab %}}
{{< /tabs >}}

And now, you must invoke your new function.
Your main function should look similar to this snippet:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
async def main():
    robot = await connect()
    print('Resources:')
    print(robot.resource_names)
    arm = ArmClient.from_robot(robot=robot, name='my_main_arm')
    motor = MotorClient.from_robot(robot=robot, name='sub-part:my_sub_motor')
    await toggleMotor(motor)
    # await randomMovement(arm)
    await robot.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
func main() {
  // Connect to the robot...
  myMotor, err := motor.FromRobot(robot, "my_sub_motor")
    if err != nil {
    logger.Fatalf("cannot get motor: %v", err)
  }
  toggleMotor(context.Background(), myMotor)

  myArm, err := arm.FromRobot(robot, "my_main_arm")
  if err != nil {
    logger.Fatalf("cannot get arm: %v", err)
  }
  randomMovement(context.Background(), myArm)
}
```

{{% /tab %}}
{{< /tabs >}}

When you run this code, you will see your mock sub motor toggling between running and idle in real time from the Viam app!

{{<video webm_src="../../img/build-a-mock-robot/go-start-demo.webm" mp4_src="../../img/build-a-mock-robot/go-start-demo.mp4" alt="Code runs and prints resource list">}}

## Next Steps

In this tutorial, we showed you how to set up a mock robot with a sub-part so that you can learn more about using fake components, setting up a local development environment, and writing code using a Viam SDK.

If you're ready to get started with building robots with real hardware components, you should pick up a Raspberry Pi and try building one of Viam's introductory robots on the [tutorials page in our documentation](/tutorials/).

{{< snippet "social.md" >}}
