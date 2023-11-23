---
title: "Build a Mock Robot"
linkTitle: "Mock Robot"
type: "docs"
description: "Create a mock robot using just your personal computer to try using Viam without any robotic hardware."
webmSrc: "/tutorials/build-a-mock-robot/mock-robot.webm"
mp4Src: "/tutorials/build-a-mock-robot/mock-robot.mp4"
images: ["/tutorials/build-a-mock-robot/mock-robot.gif"]
videoAlt: "A mock arm's joint positions from the control tab of the Viam app."
aliases:
  - "/tutorials/build-a-mock-robot/"
  - "/tutorials/how-to-build-a-mock-robot/"
tags: ["mock", "simulation"]
authors: []
languages: ["python", "go"]
viamresources: ["board", "arm", "motor"]
level: "Beginner"
date: "2022-10-11"
# updated: ""
cost: "0"
---

In this tutorial you will build a mock robot to learn how to configure robots with Viam.
You do not need any hardware to do this tutorial.

Follow this tutorial to set up and control a robot with a `fake` [arm](/components/arm/fake/), [board](/components/board/), and [motor](/components/motor/), and an additional mock {{< glossary_tooltip term_id="part" text="sub-part" >}} with a [motor](/components/motor/).
These `fake` components interact with Viam like real hardware but do not physically exist.

## Set up a mock robot

You'll need the following hardware and software for this tutorial:

- A computer running Linux or macOS
- [Go](https://go.dev/doc/install) or [Python 3.9+](https://www.python.org/downloads/)

If you don't already have a Viam account, sign up for one on [the Viam app](https://app.viam.com).
Create a new robot in the organization and location of your choice.
Go to this robot's **Setup** tab.

### Install and start `viam-server` on your computer

Before you proceed with configuring and controlling your robot, install `viam-server`.
Follow the steps outlined for your computer's architecture on the **Setup** tab of the [Viam app](https://app.viam.com) to [install `viam-server`](/installation/) on your computer as a system service.

### Configure your mock robot

[Configure your mock robot](/manage/configuration/) to represent a physical machine with robotic board, arm, and motor hardware.

If you were using physical hardware, this process would provide `viam-server` with information about what hardware is attached to it and how to communicate with it.
For this robot, you configure `viam-server` to use `fake` components that emulate physical hardware.

1. Navigate to the **Config** tab of your mock robot's page in [the Viam app](https://app.viam.com).
2. Configure a [fake board component](/components/board/fake/):

   - Click on the **Components** subtab and click **Create component**.
   - Select the `board` type, then select the `fake` model.
   - Enter the name `myBoard` for your board and click **Create**.

3. Configure a [fake arm component](/components/arm/fake/):

   - Click **Create component**.
   - Select the `arm` type, then select the `fake` model.
   - Enter the name `myArm` for your board and click **Create**.
   - Make your fake arm act like a [UR5e](https://www.universal-robots.com/products/ur5-robot/) by adding the following attribute:

   ```json
   {
     "arm-model": "ur5e"
   }
   ```

   The config panel should look like this:

   ![A fake arm being configured in Builder mode in the Viam app config tab.](/tutorials/build-a-mock-robot/create-arm.png)

   - Click **Save config**.

4. Configure a [fake motor component](/components/motor/fake/):

   - Click **Create component**.
   - Select the `motor` type, then select the `fake` model.
   - Enter the name `myMotor` for your board and click **Create**.
   - Most motors are wired to a board which sends them signals.
     Even though your motor is fake, make it more realistic by assigning it a `board`.
     Select `myBoard` from the **board** dropdown.

5. Click **Save config**.

You will need to reference the component names later when you connect to your mock robot with code.

## Control your mock robot using the Viam app

When you add components to your robot, the Viam app automatically generates a UI for them under the [**Control** tab](/manage/fleet/robots/#control):

{{< imgproc src="/tutorials/build-a-mock-robot/control-tab.png" alt="The Control tab with the fake arm, and motor components." resize="400x" >}}

You can use the **Control** tab UI to send commands to your robot.

For example, you can control the direction and speed of your motor, or change the joint positions of your robotic arm.
You can also see the robot's reported positions and speeds change.
With real physical components, you would not only be able to control and see your robot's readings on this tab, but you would also see your robot move in the physical world.

## Control your mock robot using a Viam SDK

### Install a Viam SDK

Install a Viam SDK (software development kit) so you can write custom logic to control the mock robot.
Use the programming language you are most comfortable with.

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

```sh {class="command-line" data-prompt="$"}
python3 index.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {class="command-line" data-prompt="$"}
go run index.go
```

{{% /tab %}}
{{< /tabs >}}

If you successfully configured your robot and it is able to connect to the Viam app you should see the program print a list of the various _{{< glossary_tooltip term_id="resource" text="resources" >}}_ that have been configured on your robot in the Viam app:

![Command line output from running python3 index.py when your Raspberry Pi has correctly connected and initialized with the Viam app. The output is an array of resources that have been pulled from the Viam app. The list includes the motion service, arm component, data manager, board component and motor component. There is also a list of arm position and orientation values.](/tutorials/build-a-mock-robot/resource-output.png)

### Control your mock robot

Now, write a program that moves the mock robotic arm to a new random position every second.

{{< tabs >}}
{{% tab name="Python" %}}

First, import the [arm component](https://python.viam.dev/autoapi/viam/components/arm/client/index.html) from the Viam Python SDK, and the [random](https://docs.python.org/3/library/random.html) and [async.io](https://docs.python.org/3/library/asyncio.html) libraries.

At the top of your <file>index.py</file> file, paste the following:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.arm import ArmClient, JointPositions
import random
import asyncio
```

{{% /tab %}}
{{% tab name="Go" %}}

At the top of your <file>index.go</file> file, paste the following:

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
# Gets a random position for each servo on the arm that is within the safe
# range of motion of the arm. Returns a new array of safe joint positions.
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

Verify that your mock robotic arm is working in the **Control** tab of the [Viam app](https://app.viam.com).
Watch the robotic arm's [`JointPositions()`](/components/arm/#jointpositions) changing in real-time along with the code on your development machine.

<div class="td-max-width-on-larger-screens">
  {{<gif webm_src="/tutorials/build-a-mock-robot/joint-changes.webm" mp4_src="/tutorials/build-a-mock-robot/joint-changes.mp4" alt="A terminal window with 'python3 index.py' being run, then a list of four values is printed each second to the terminal. On the left side is the mock arm from the Control tab of the Viam app. As the joint positions are updated in the terminal from the left, you can see that the joint positions are updated in realtime on the Viam app.">}}
</div>

## Configure your robot's mock sub-part

Now that you have your `fake` robotic arm, board, and motor working, add a `fake` motor sub-part to your robot.
Imagine for the purpose of this tutorial that the `fake` motor we are adding controls a conveyor belt in front of your mock arm on an assembly line.

### What is a sub-part?

Usually, when building a {{< glossary_tooltip term_id="robot" text="robot" >}}, you pick out a [single-board computer](/components/board/) like the [Jetson Nano](/components/board/jetson/) or [Raspberry Pi](/components/board/pi/).
You follow the instructions in the **Setup** tab to install `viam-server` on your [board](/components/board/), and you start operating your robot with that computer, adding the [components](/components/) and [services](/services/) you want to use to that `viam-server` instance.

By utilizing {{< glossary_tooltip term_id="part" text="parts" >}}, you can expand upon this, chaining multiple computers together to build a complex robot with Viam:

- Each individual computer-controlled unit of a robot is called a “{{< glossary_tooltip term_id="part" text="part" >}}” in Viam.
- Typically, simple robots have just one part, but you can have as many parts as your project requires.
- Parts are organized in a tree, with one of them being the _main_ part, and the others being _sub-parts_.
- You can access any sub-part either directly, or through any part above it in the tree.
- Each part runs a single `viam-server` instance.

### Add a new sub-part in the Viam app

On your robot's page on the Viam app, click on the dropdown next to the main part, name your part and click **Add new**.

![Screenshot of the Viam app with a dropdown below the main part. 'sub-part' is written in the textbox.](/tutorials/build-a-mock-robot/part-menu.png)

Navigate to your new sub-part's **Config** tab and create a new motor:

Click **Create component** in the lower-left corner of the page.
Select type `motor` and model `fake`.
Enter `motor2` as the name and click **Create**.

{{< imgproc src="/tutorials/build-a-mock-robot/sub-part-motor.png" alt="The config tab of the sub-part. A new fake motor component called motor2 is being created." resize="400x" >}}

Click **Save config**.

### Start a new instance of `viam-server` for your mock sub-part

Every sub-part of a robot needs to run an instance of `viam-server`.
Since you are using only one computer, you need to bind the sub-part to a new port so you can run two servers on your machine at the same time.

The following instructions use port `8081`, but you can use any open port you want.

1. Go to the **Config** tab and then go to the **Auth/Network** subtab.
2. Under **Network** click **Add bind address**.
3. In the **Host** field type `localhost`.
4. In the **Port** field type `8081`.
5. Click **Save config**.

### Run a second instance of `viam-server` for your sub-part

In the upper right corner of the **Setup** tab, click **Copy viam-server config**.

![The Setup tab of the sub-part's robot page showing the 'Copy viam-server config' button highlighted by a red box.](/tutorials/build-a-mock-robot/copy-config.png)

On your local machine, create a new file called <file>viam-sub-part.json</file>, then paste the contents of your server config into that file and save.
From a new terminal window, navigate to the directory where you saved the config file, and run the following command to create a new instance of `viam-server` using this configuration.

```sh {class="command-line" data-prompt="$"}
viam-server -config viam-sub-part.json
```

Now that you have two instances of `viam-server` running on your local machine, you should be able to see both your main robot arm and your new mock sub motor listed on your main robot's **Control** tab.

![Screenshot of the Viam app's Control tab for the main part that lists the main arm, and the sub part motor component.](/tutorials/build-a-mock-robot/control-all.png)

To test that your motor sub-part has been added to your robot, run your Python or Go script again.
Review the output of your program that prints the robot's resources to see your sub-part's motor's `name` listed.

## Control a sub-part using the Viam SDK

Now that you have your mock sub-part connected as a remote to your main mock robot, you can control all of your sub-part's components and services with Viam's SDKs.

In your main function, you need to instantiate your mock sub motor.
Make sure your motor's name matches the one that you configured for it.

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

Now, invoke your new function in `main()`.
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

Run this code to see your mock sub-part's motor toggling between running and idle in real time from the Viam app!

{{<gif webm_src="/tutorials/build-a-mock-robot/go-start-demo.webm" mp4_src="/tutorials/build-a-mock-robot/go-start-demo.mp4" alt="Code runs and prints resource list">}}

## Next steps

In this tutorial, we showed you how to set up a mock robot with a sub-part so that you can learn more about using fake components, setting up a local development environment, and writing code using a Viam SDK.

If you're ready to get started with building robots with real hardware components, pick up a [board](/components/board/) and try following another [tutorial](/tutorials/).
