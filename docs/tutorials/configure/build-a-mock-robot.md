---
title: "Build a Mock Robot"
linkTitle: "Mock Robot"
weight: 41
type: "docs"
description: "Create a mock robot using just your personal computer to try using Viam without any robotic hardware."
webmSrc: "/tutorials/img/build-a-mock-robot/mock-robot.webm"
mp4Src: "/tutorials/img/build-a-mock-robot/mock-robot.mp4"
images: ["/tutorials/img/build-a-mock-robot/mock-robot.gif"]
videoAlt: "A mock arm's joint positions from the control tab of the Viam app."
aliases:
    - "/tutorials/build-a-mock-robot/"
    - "/tutorials/how-to-build-a-mock-robot/"
tags: ["mock", "simulation"]
authors: []
languages: [ "python", "go" ]
viamresources: [ "board", "arm", "motor" ]
level: "Beginner"
date: "11 October 2022"
cost: "0"
---

This tutorial will show you how to build a mock robot using just your personal laptop so you can:

- Learn how to [configure](../../../manage/configuration/) robots with Viam.
- Try using [Viam](/viam/) without any robotic hardware.

Most Viam [components](../../../components/) have a _fake_ model that you can use for testing.
These fake components interact with Viam like real hardware but do not actually exist.

In this tutorial, you will set up, control, and program a mock robotic arm and a mock sub-part with a motor using fake components.

## Requirements

You'll need the following hardware and software for this tutorial:

- A laptop or desktop running Linux or macOS
- [Go](https://go.dev/doc/install) or [Python 3.9+](https://www.python.org/downloads/)
- A code editor of your choice

## Set up a mock robot

### Make an account on the Viam app

The first thing you need to do is set up your account on the Viam app.
Go to [app.viam.com](https://app.viam.com) and sign up for a free account.

### Configure your mock robot

Now you'll [configure your robot](/manage/configuration/) to represent your robot's hardware.
If you were using actual hardware, this file would tell your code what hardware is attached to it and how to communicate with it.

Since this is an imaginary robot, you will use `fake` components so that the Viam software ([`viam-server`](../../../viam/#get-started)) doesn't try and fail to connect to physical hardware.

1. Go to [app.viam.com](https://app.viam.com/).
2. Create a new [robot](../../../manage/fleet/robots/).
3. Go to the new robot's **Config** tab.
4. Configure a [fake board component](../../../components/board/fake/):

    - Create a new component called `myBoard` with **Type** `board` and **Model** `fake`.
    Click **Create component**.

5. Configure a [fake arm component](../../../components/arm/fake/):

    - Create a new component called `myArm` with **Type** `arm` and **Model** `fake`.
    Click **Create component**.
    - Make your fake arm act like a [UR5e](https://www.universal-robots.com/products/ur5-robot/) by adding the following attribute:

      ```json
      {
          "arm-model": "ur5e"
      }
      ```

    The config panel should look like this:

    ![A fake arm being configured in Builder mode in the Viam app config tab.](../../img/build-a-mock-robot/create-arm.png)
    - Click **Save config**.

6. Configure a [fake motor component](../../../components/motor/fake/):

   - Create a new component called `myMotor` with **Type** `motor` and **Model** `fake`.
     Click **Create component**.
   - Most motors are wired to a board which sends them signals.
   Even though your motor is fake, make it more realistic by assigning it a `board`.
   Select `myBoard` from the **board** drop-down.

7. Click **Save config**.

You will need to reference the component names later when you connect to your mock robot with code.

### Install and start `viam-server` on your computer

Before you proceed with controlling your mock robot, you need to install `viam-server`.

{{< tabs >}}
{{% tab name=macOS %}}

Follow the steps outlined on the **Setup** tab of the Viam app to install `viam-server` on your computer and start `viam-server` from a terminal window.

{{% /tab %}}
{{% tab name=Linux %}}

Follow the steps outlined on the **Setup** tab of the Viam app to install `viam-server` on your computer.

The **Setup** tab steps set it up as a system service which means that `viam-server` will automatically start every time you boot your computer.
This is convenient if the computer running `viam-server` is a dedicated part of a robot, but it is less practical if you are installing `viam-server` on your everyday laptop or desktop.

To disable `viam-server` from starting automatically on boot, run the following command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo systemctl disable viam-server
```

Then start `viam-server`:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo ./viam-server -config /etc/viam.json
```

{{% /tab %}}
{{< /tabs >}}

Find more information on running `viam-server` in the [installation guide](../../../installation/manage/).

## Control your mock robot using the Viam app

When you add components to your robot, the Viam app automatically generates a UI for them under the **Control** tab.

![Screenshot from the Viam app showing the Control tab with the fake arm, and motor components.](../../img/build-a-mock-robot/control-tab.png)

You can use the **Control** tab UI to send commands to your robot.
For example, you can control the direction and speed of your motor, or change the joint positions of your robotic arm.
You can also see the robot's reported positions and speeds change.
With real physical components, you would not only be able to control and see your robot's readings on this tab, but you would also see your robot move in the physical world.

Next, install a Viam SDK (software development kit) so you can write custom logic to control the mock robot.

## Control your mock robot using a Viam SDK

### Install a Viam SDK

In this step, you will install either the [Viam Python SDK](https://python.viam.dev/) or the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk).
Use which ever programming language you are most comfortable with.

Refer to the appropriate SDK documentation for SDK installation instructions:

- [Viam Python SDK](https://python.viam.dev/)
- [Viam Go SDK](https://github.com/viamrobotics/rdk/tree/main/robot/client)

### Connect to your mock robot with your code

The easiest way to get started writing an application with Viam's SDKs is to use the boilerplate code on the **Code sample** tab.

Navigate to your [robot's page on the Viam app](https://app.viam.com/robots), select the **Code sample** tab, select your SDK language (**Python** or **Golang**), and copy the boilerplate code.

{{% snippet "show-secret.md" %}}

This code snippet imports all the necessary libraries, is pre-populated with your robot credentials, and sets up a connection with the Viam app in the cloud.
Next, paste that boilerplate code into a file named <file>index.py</file> or <file>index.go</file> in your code editor, and save your file locally.

You can now run the code.
Doing so verifies that the Viam SDK is properly installed, that the `viam-server` instance on your robot is live, and that the computer running the program is able to connect to that instance.

Run your code by entering the following in a new terminal on your computer:

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
What you see here is a list of the various _{{< glossary_tooltip term_id="resource" text="resources" >}}_ that have been configured on your robot in the Viam app.

![Command line output from running python3 index.py when your Raspberry Pi has correctly connected and initialized with the Viam app. The output is an array of resources that have been pulled from the Viam app. The list includes the Motion Service, arm component, data manager, board component and motor component. There is also a list of arm position and orientation values.](../../img/build-a-mock-robot/resource-output.png)

### Control your mock robot

Now it's time to write code to control and move your mock robotic arm.
Through the following steps, you will write a program that moves the mock robotic arm to a new random position every second.
You will be able to verify that your mock robotic arm is working by watching its joint positions change in the **Control** tab of the Viam app while your code runs.

At the top of your <file>index.py</file> file, paste the following:

{{< tabs >}}
{{% tab name="Python" %}}

First, import the [arm component](https://python.viam.dev/autoapi/viam/components/arm/client/index.html) from the Viam Python SDK, and the [random](https://docs.python.org/3/library/random.html) and [async.io](https://docs.python.org/3/library/asyncio.html) libraries.

```python {class="line-numbers linkable-line-numbers"}
from viam.components.arm import ArmClient, JointPositions
import random
import asyncio
```

{{% /tab %}}
{{% tab name="Go" %}}

First, import the [arm component](https://github.com/viamrobotics/rdk/blob/main/components/arm/client.go) from the Viam Go SDK, and the [random](https://pkg.go.dev/math/rand) and [time](https://pkg.go.dev/time) libraries.

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

Next, you need to initialize your fake robotic arm.
In the main function, paste the following.
Make sure that the name of your fake arm matches the arm named in your config file.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
arm = ArmClient.from_robot(robot=robot, name='myArm')
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "myArm")
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
# Gets a random position for each servo on the arm that is within the safe range of motion of the arm.
# Returns a new array of safe joint positions.
def getRandoms():
    return [random.randint(-90, 90),
    random.randint(-120, -45),
    random.randint(-45, 45),
    random.randint(-45, 45),
    random.randint(-45, 45)]

# Moves the arm to a new random position every second
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

// Moves the arm to a new random position every second
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

You can run this code by invoking this function below your arm initialization in main.
Your main function should look like this:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    arm = ArmClient.from_robot(robot=robot, name='myArm')
    await randomMovement(arm)

    await robot.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
func main() {
  // Connect to the robot...
  myArm, err := arm.FromRobot(robot, "myArm")
  if err != nil {
    logger.Fatalf("cannot get arm: %v", err)
  }
  randomMovement(context.Background(), myArm)
}
```

{{% /tab %}}
{{< /tabs >}}

Now when you run this code, you should see the new mock arm positions listed in the command line.
Open the **Control** tab of your mock robot to see the robot's arm positions changing in real-time along with the code on your development machine.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="/tutorials/img/build-a-mock-robot/joint-changes.webm" mp4_src="/tutorials/img/build-a-mock-robot/joint-changes.mp4" alt="A terminal window with 'python3 index.py' being run, then a list of four values is printed each second to the terminal. On the left side is the mock arm from the Control tab of the Viam app. As the joint positions are updated in the terminal from the left, you can see that the joint positions are updated in realtime on the Viam app.">}}
</div>

## Create a mock sub-part

Now that you have your mock robotic arm working, add a mock sub-part to your robot.

### What is a part?

A _{{< glossary_tooltip term_id="robot" text="robot" >}}_ in Viam consists of one or more computers combined into one logical unit.
The bounds of a robot are usually pretty clear, but can be subjective.
However, it's possible with Viam to create a robot that is made up of multiple computers.
Each of these computer-controlled units is referred to as a _{{< glossary_tooltip term_id="part" text="part" >}}_.
Most simple robots will have only one part, but they can have as many parts as needed.

Parts are organized in a tree, with one of them being the _main_ part, and the others being _sub-parts_.
You can access any sub-part either directly, or through any part above it in the tree.
Each part runs a single `viam-server` instance.

## Configure a sub-part in the Viam app

You will be creating a mock sub-part to control a motor.
This could be anything, but imagine for the purpose of this tutorial that this motor controls a conveyor belt in front of your mock arm on an assembly line.

On your robot's page on the Viam app, click on the dropdown next to the main part, name your part and click **Add new**.

![Screenshot of the Viam app with a dropdown below the main part. 'SubPart' is written in the textbox.](../../img/build-a-mock-robot/part-menu.png)

Navigate to your new sub-part's **Config** tab and create a new motor using the **fake** model.
Name it `"motor2"`.

![The config tab of the sub-part. A new motor component called motor2 is being created.](../../img/build-a-mock-robot/sub-part-motor.png)

Click **Create component** and then **Save config**.

### Start a new instance of `viam-server` for your mock sub-part

Every part needs to run an instance of `viam-server`.
Typically, a sub-part would represent a separate computer running `viam-server`.
For this tutorial since you are using only one computer, you will need to bind the sub-part to a new port so you can run two servers on your machine at the same time.
The following instructions use port `8081`, but you can use any open port you want.

1. Go to the **Config** tab and then go to the **Auth/Network** subtab.
2. Under **Network** click **Add bind address**.
3. In the **Host** field type `localhost`.
4. In the **Port** field type `8081`.
5. Click **Save config**.

### Run a second instance of `viam-server` for your sub-part

In the upper right corner of the **Setup** tab, click **Copy viam-server config**.

![The Setup tab of the sub-part's robot page showing the 'Copy viam-server config' button highlighted by a red box.](../../img/build-a-mock-robot/copy-config.png)

On your local machine, create a new file called <file>viam-sub-part.json</file>, then paste the contents of your server config into that file and save.
From a new terminal window, navigate to the directory where you saved the config file, and run the following command to create a new instance of `viam-server` using this configuration.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam-server -config viam-sub-part.json
```

Now that you have two instances of `viam-server` running on your local machine, you should be able to see both your main robot arm and your new mock sub motor listed on your main robot's **Control** tab.

![Screenshot of the Viam app's Control tab for the main part that lists the main arm, and the sub part motor component.](../../img/build-a-mock-robot/control-all.png)

## Control a sub-part using the Viam SDK

Now that you have your mock sub-part connected as a remote to your main mock robot, you can control all of your sub-part's components and services with Viam's SDKs.
In fact, if you run your Python or Go script again, and you review the output of `print(robot.resource_names)`, you will see that your sub-part's motor will now be listed as an available resource for you to use.

In your main function, you need to instantiate your mock sub motor.
Be sure that your motor's name matches the one that you have listed in your robot's resource names.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
motor = Motor.from_robot(robot=robot, name='SubPart:motor2')
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myMotor, err := motor.FromRobot(robot, "motor2")
if err != nil {
  logger.Fatalf("cannot get motor: %v", err)
}
```

{{% /tab %}}
{{< /tabs >}}

Write a function that toggles your sub-part's motor on and off every second:

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
    arm = Arm.from_robot(robot=robot, name='myArm')
    motor = Motor.from_robot(robot=robot, name='SubPart:motor2')
    await toggleMotor(motor)
    # await randomMovement(arm)
    await robot.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
func main() {
  // Connect to the robot...
  myMotor, err := motor.FromRobot(robot, "motor2")
    if err != nil {
    logger.Fatalf("cannot get motor: %v", err)
  }
  toggleMotor(context.Background(), myMotor)

  myArm, err := arm.FromRobot(robot, "myArm")
  if err != nil {
    logger.Fatalf("cannot get arm: %v", err)
  }
  randomMovement(context.Background(), myArm)
}
```

{{% /tab %}}
{{< /tabs >}}

When you run this code, you will see your mock sub motor toggling between running and idle in real time from the Viam app!

{{<gif webm_src="/tutorials/img/build-a-mock-robot/go-start-demo.webm" mp4_src="/tutorials/img/build-a-mock-robot/go-start-demo.mp4" alt="Code runs and prints resource list">}}

## Next steps

In this tutorial, we showed you how to set up a mock robot with a sub-part so that you can learn more about using fake components, setting up a local development environment, and writing code using a Viam SDK.

If you're ready to get started with building robots with real hardware components, pick up a [board](/components/board/) and try building one of Viam's [introductory robots](/tutorials/#your-first-robots).

{{< snippet "social.md" >}}
