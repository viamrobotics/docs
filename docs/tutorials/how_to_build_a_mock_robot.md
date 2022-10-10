---
title: "How To Build a Mock Robot"
linkTitle: "How To Build a Mock Robot"
weight: 55
type: "docs"
description: "Instructions for creating a mock robot using just your personal computer so you can try using Viam without any robotic hardware."
---

## Introduction

In this post, we will show you how to build a mock robot using just your personal computer so you can try using Viam without any robotic hardware.
This is a great way to learn how to build robots the Viam way.
In this tutorial, you will have set up, controlled, and programmed a mock robotic arm using fake components.

## What is the Viam way to build a robot?

Viam provides an open-source robot architecture that turns complex functionality into simple APIs, with an integrated cloud service to orchestrate production deployments.
This allows you to configure a robot in minutes, and operate it from anywhere through any common software language such as [Python](https://python.viam.dev/).
The Viam platform manages, secures, and connects any robot.

Most Viam components come with a fake model that can be useful when testing.
These are fake components that interact with the Viam software like real robotics components, but of course, do not exist as real-world hardware.
We will be using these fake components to build out a mock robot and explore how to use Viam.

## What you'll need for this guide

-   A laptop or desktop running Linux or macOS.

-   [Python3](https://www.python.org/download/releases/3.0/)

-   [Pip](https://pip.pypa.io/en/stable/#)

-   [Viam Server](https://github.com/viamrobotics/rdk)

-   [Viam Python SDK](https://python.viam.dev/)

-   Have a code editor of your choice ready.

-   If you are running macOS, ensure you have [Homebrew](https://brew.sh/) installed and up to date on your Mac.

## How to set up a mock robot

### Set up your account on the Viam app

The first thing you need to do is set up your account on the Viam App. Steps on how to do this can be found in the [Adding your robot on the Viam app](https://docs.viam.com/getting-started/installation/#adding-your-pi-on-the-viam-app) section of the Viam documentation.

{{% alert title=\"Note\" color=\"tip\" %}}
Be sure to choose the correct system architecture at the top of the Setup tab; most Linux laptops and desktops will use x86_64.
{{% /alert %}}

### How to install Viam Server on your development machine

Before you proceed with building your mock robot, you are going to need to install Viam server on your development machine.

-   If you are installing on a Linux-based computer, you can follow along with the [Installing Viam Server on Linux Systems](https://docs.viam.com/getting-started/linux-install/) guide in the Viam documentation.

-   If you are installing on a computer running macOS you will need to:

     -   Set up your robot's Viam config on your Mac. You can find the **SECRET** and **ADDRESS** information on the **CONNECT* tab of your robot on the Viam App.

    ```bash
    curl -H "Secret: <insert secret>" "<insert address>" -o "$HOMEBREW_PREFIX/etc/viam.json"
    ```

     -   Install Viam via Homebrew

    ```bash
    brew install --HEAD viam-server
    ```

     -   Await connection. You should see that your robot is live on your robot's page from the Viam app.

## How to configure your mock robot in the Viam app

Now that you have set up Viam server on your development machine, let's get back to setting up your mock robot in the Viam app.
First, go to the Viam app at [app.viam.com](https://app.viam.com/) on your web browser, navigate to the robot running the server you set up, and select the **CONFIG** tab.

![A screenshot from the Viam app showing the CONFIG tab from the mock robot.](../img/how_to_build_a_mock_robot/image4.png)

For this tutorial, we will show you how to set up a mock robot with a fake board, arm, and motor.

For each component, you will need to create a new component.
For the component **Type**, select **board/arm/motor**.
Then you can name them whatever you like (You will need to reference these names later once we connect to your mock robot with the Python SDK).
For each **Model**, select **fake**, then click **new component**.

Once the board, arm, and motor components have been created, you will need to add the fake board as a dependency of the arm and the motor using the **Depends On** field.
This is because robot parts can depend on other components to work.
In this instance, your mock arm and motor will be connected and controlled by the fake board.

{{% alert title="Tip" color="tip" %}}
Feel free to add any other components to your mock robot that you want to test out, like a motor or a servo.
Just be sure that for any additional components you add, you are using the **fake** model for each.
{{% /alert %}}

## Controlling your mock robot using the Viam App

When you add the fake board and arm components to your robot, the Viam app automatically generates tabs for your board and arm under the **CONTROL** tab.

![Screenshot from the Viam app showing the CONTROL tab with the fake board, arm, and motor components.](../img/how_to_build_a_mock_robot/image3.png)

If you were configuring a real robotic arm and motor, you would be able to control it from this section of the app.
You could do things like control the direction and speed of the motor, and change the joint positions of your robotic arm.
However, since we are building a mock robot using fake components, you will only see the robot's reported positions and speeds change from the UI.
You will not be able to see your robot move in the physical world.

Next, you will need to configure your mock robotic arm with the Viam Python SDK so you can write custom logic to control the mock robot.

## Controlling your mock robot using the Viam Python SDK

### How to install the Viam Python SDK

In this step, you are going to install the [Viam Python SDK](https://python.viam.dev/) (Software Development Kit).
This allows you to write programs in the Python programming language to operate robots using [Viam](http://www.viam.com/).

You can find instructions for [installing the Viam Python SDK](https://python.viam.dev/) in the documentation.

{{% alert title="Tip" color="tip" %}}
If you have any issues whatsoever getting the Viam Python SDK set up or getting your code to run on your computer, the best way to get help is over on the [Viam Community Slack](http://viamrobotics.slack.com).
There, you will find a friendly developer community of people learning how to make robots using Viam.
{{% /alert %}}

### How to connect to your mock robot with the Viam Python SDK

The easiest way to get started writing a Python application with Viam is to navigate to the [robot page on the Viam App](https://app.viam.com/robots), select the **CONNECT** tab, and copy the boilerplate code from the section labeled **Python SDK**.
This code snippet imports all the necessary libraries and sets up a connection with the Viam App in the cloud.

Next, paste that boilerplate code from the **CONNECT** tab of the Viam app into a file named index.py file in your code editor, and save your file.

You can now run the code.
Doing so will ensure that the Python SDK is properly installed, that the viam-server instance on your robot is alive, and that the computer running the program is able to connect to that instance.

You can run your code by typing the following into the terminal:

```bash
python3 index.py
```

If you successfully configured your robot and it is able to connect to the Viam app you should see something like this printed to the terminal after running your program.
What you see here is a list of the various resources (Like components, and services) that have been configured to your robot in the Viam app.

![A screenshot from the Visual Studio Code command line that prints the output of print(robot.resource_names) when your Raspberry Pi has correctly connected and initialized with the Viam App.The output is an array of resources that have been pulled from the Viam App. Some of these are the Vision Service, Data Manager, and Board.](../img/how_to_build_a_mock_robot/image1.png)

### How to control your mock robot with Python

Next, you will be writing some code in Python to control and move your mock robotic arm.
We are going to write a program that will move the mock robotic arm into a new random position every second.
You will be able to verify that your mock robotic arm is working by checking that the joint positions of the fake arm in the **CONTROL** tab of the Viam app are changing.

The first thing you need to do is import the [arm component](https://python.viam.dev/autoapi/viam/components/arm/client/index.html) from the Viam Python SDK, and the [random](https://docs.python.org/3/library/random.html) and [async.io](https://docs.python.org/3/library/asyncio.html) libraries.

At the top of your index.py file, paste the following:

```python
from viam.components.arm import ArmClient, JointPositions
import random
import asyncio
```

Next, you will need to initialize your fake robotic arm.
In the main function, paste the following, while ensuring that the name of your fake arm matches the name of your arm in your config file.

```python
arm = ArmClient.from_robot(robot=robot, name='my_main_arm')
```

Now that your mock arm has been initialized, you can write some code to control it.

```python
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

You can run this code by invoking this function located below your arm initialization in main. Your main function, should look like this:

```python
async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    arm = ArmClient.from_robot(robot=robot, name='my_main_arm')
    await randomMovement(arm)

    await robot.close()
```

Now when you run this code, you should see the new mock arm positions listed in the command line, if you open the **CONTROL** tab of your mock robot, you should see the robot's arm positions changing in real-time along with the code on your development machine.

![Gif of a terminal window on the right with "python3 index.py" being run, then a list of four values is printed each second to the terminal. On the left side, is the mock arm from the CONTROL tab of the Viam app. As the joint positions are updated in the terminal from the left, you can see that the joint positions are updated in realtime on the Viam app.](../img/how_to_build_a_mock_robot/image2.gif)

## Next Steps

In this tutorial, we showed you how to set up a mock robot so that you can learn more about how to set up robots with Viam.
You set up a mock robot in the Viam app using fake components, set up a local development environment and wrote some code using the Viam Python SDK so that you can see how to control robots with code and the Viam app.

If you're ready to get started with building robots with real hardware components, you should pick up a Raspberry Pi and try building one of Viam's introductory robots on the [tutorials page in our documentation](https://docs.viam.com/tutorials/).

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, be sure that you head over to the [Viam Community Slack](http://viamrobotics.slack.com).

