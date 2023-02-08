---
title: "How to Make an LED Blink with a Raspberry Pi and the Viam SDK"
linkTitle: "Blink an LED with a Pi and the SDK"
weight: 40
type: "docs"
description: "Intro to hardware programming using the Viam SDK to make an LED blink."
tags: ["board", "raspberry pi", "sdk"]
# SME: Joe Karlsson
---
In this post, you will be introduced to the basics of programming hardware by using either the [Viam Python SDK](https://python.viam.dev/) or the [Viam Golang SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme) to make an LED blink.
This will allow you to write code to make an LED connected to the GPIO of a Raspberry Pi blink on and off.
This tutorial is a good introduction to [Python](https://www.python.org/) or [Go](https://go.dev/) programming languages, and developing custom software for robots.

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-sdk/image3.gif" alt="A GIF of the completed project showing a blinking blue LED connected to a Raspberry Pi with jumper cables." width="100%"><br>

{{% alert title="Note" color="note" %}}
This is part 2 of Viam's Intro to Robotics series.
If you haven't completed [Part 1](/tutorials/pi/make-an-led-blink-with-the-viam-app/), be sure to go back and complete that before starting on this tutorial.
You should have already set up [your Raspberry Pi](/installation/prepare/rpi-setup), [set up `viam-server`](/installation/install), built your circuit, and [connected your robot to the Viam app](/installation/install/linux-install/) before proceeding.
{{% /alert %}}

For reference, the circuit you are building for this tutorial looks like this:

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-sdk/image1.png" alt="Circuit diagram showing a Raspberry Pi with a red connector running out of GPIO pin 8 to a 100-ohm* resistor*. The resistor is connected to the long lead of a red LED bulb. Finally, a blue connector connects the short lead of the LED to the ground connection on pin 6 of the Raspberry Pi GPIO pins." width="100%"><br>

## What you'll need for this guide

You will need the following hardware, tools, and software to complete this project:

### Hardware

<ol>
    <li><a href="https://a.co/d/5Tn67G3" target="_blank">Raspberry Pi 3 or 4</a></li>
<ol type="a">
<li>Refer to the [Viam Raspberry Pi Setup Guide](/installation/prepare/rpi-setup) to setup your Pi.</li>
<li>You must also enable SSH on your Pi.</li>
</ol>
    <li><a href="https://amzn.to/2Q4Z5Ta" target="_blank">Solderless breadboard</a></li>
    <li><a href="http://amzn.to/2qVhd4y" target="_blank">Jumper wires for easy hookup</a></li>
    <li><a href="http://amzn.to/2Dmainw" target="_blank">Resistor pack </a>You will be using a 100 Ohm resistor, which is the resistor with brown-black-brown bands</li>
    <li><a href="http://amzn.to/2Ex2v5q" target="_blank">LED</a></li>
</ol>

[Click to view the Component URL Listing](#components-url-list)

### Software

- [Golang](https://go.dev/dl/) or [Python 3.9+](https://www.python.org/downloads/)
- [viam-server](/installation/install/linux-install/)
- [Viam Python SDK](https://python.viam.dev/) or [Viam Golang SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme)

### How to install a Viam SDK

In this step, you are going to install either the [Viam Python SDK](https://python.viam.dev/) (Software Development Kit) or the [Viam Golang SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme) on your local computer.
Use which ever programming language you are most comfortable with.

{{% alert title="Note" color="note" %}}

Refer to the appropriate SDK documentation for SDK installation instructions.

- [Viam Python SDK](https://python.viam.dev/)
- [Viam Golang SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme)

{{% /alert %}}

### How to connect your robot to the Viam SDK

The easiest way to get started writing an application with Viam is to navigate to the [robot page on the Viam App](https://app.viam.com/robots), select the **CODE SAMPLE** tab, and copy the boilerplate code from the section labeled **Python SDK** or **Golang SDK**.
These code snippets import all the necessary libraries and set up a connection with the Viam app in the cloud.
Next, paste that boilerplate code from the **CODE SAMPLE** tab of the Viam app into a file named <file>blink.py</file> or <file>blink.go</file> file in your code editor, and save your file.

You can now run the code.
Doing so will ensure that the Viam SDK is properly installed and that the `viam-server` instance on your robot is live.

You can run your code by typing the following into the terminal:

{{< tabs >}}
{{% tab name="Python" %}}

```bash
python3 blink.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
go run blink.go
```

{{% /tab %}}
{{< /tabs >}}

If you successfully configured your robot and it is able to connect to the Viam app, you should see something like this printed to the terminal after running your program.
What you see here is a list of the various resources, components, and services that have been configured to your robot in the Viam app.

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-sdk/image4.png" alt="A screenshot from the Visual Studio Code command line that prints the output of print(robot.resource_names) when your Raspberry Pi has correctly connected and initialized with the Viam app. The output is an array of resources that have been pulled from the Viam app. Some of these are the Vision Service, Data Manager, and Board." width="500"><br>

{{% alert title="Tip" color="tip" %}}
If you have any issues whatsoever getting the Viam SDK set up or getting your code to run on your computer, the best way to get help is over on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw).
There, you will find a friendly developer community of people learning how to make robots using Viam.
{{% /alert %}}

### How to make an LED Blink with the Viam SDKs

The first thing you need to do is import the [Board component](/components/board/) from the Viam SDK.
This component represents a physical general-purpose board that contains GPIO pins.
We will need this component in order to interact with the GPIO pins on our Raspberry Pi.

{{< tabs >}}
{{% tab name="Python" %}}

At the top of your <file>blink.py</file> file, add the following to the import statement without removing any of the other imports

```python
from viam.components.board import Board
```

{{% /tab %}}
{{% tab name="Go" %}}

In <file>blink.go</file>, and inside the `import` block at the top of the file, add the following to the import statements without removing any of the other imports:

```go {class="line-numbers linkable-line-numbers"}
import (
  "fmt"
  "time"
  "go.viam.com/rdk/components/board"
)
```

{{% /tab %}}
{{< /tabs >}}

Next, you will need to initialize the Raspberry Pi board, and you will need to tell Viam which GPIO pin your LED is on.
At the bottom of the <code>main()</code> function, paste the following:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Initialize the board and the LED on pin 8
local = Board.from_robot(robot, 'local')
led = await local.gpio_pin_by_name('8')
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Initialize the board
myBoard, err := board.FromRobot(robot, "myBoard")
if err != nil {
    logger.Fatalf("could not get board: %v", err)
}

// Initialize the board's GPIO pin and name it "led"
led, err := myBoard.GPIOPinByName("8")
if err != nil {
    logger.Fatalf("could not get led: %v", err)
}
```

{{% /tab %}}
{{< /tabs >}}

Now that we have our board, and LED initialized, let's create an infinite loop that will blink the LED on and off.
Within the `main` function, you can add the code to create an infinite loop, you can remove the line to close out the connection to your robot, since the infinite loop will never hit that line.
Your completed `main` function should look like this:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    # Initialize the board and the LED on pin 8
    local = Board.from_robot(robot, 'local')
    led = await local.gpio_pin_by_name('8')

    # Create an infinite loop that will blink the LED on and off
    while (True):
        # When True, sets the LED pin to high/on.
        await led.set(True)
        print('LED is on')
        await asyncio.sleep(1)

        # When False, sets the pin to low/off.
        await led.set(False)
        print('LED is off')
        await asyncio.sleep(1)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
func main() {
  logger := golog.NewDevelopmentLogger("client")
  robot, err := client.New(
      context.Background(),
      "[ADD YOUR ROBOT ADDRESS HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP]",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "[PLEASE ADD YOUR SECRET HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP]",
      })),
  )
  if err != nil {
      logger.Fatal(err)
  }
  defer robot.Close(context.Background())
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Initialize the board
  myBoard, err := board.FromRobot(robot, "myBoard")
  if err != nil {
    logger.Fatalf("could not get board: %v", err)
  }
  // Initialize the board's GPIO pin and name it "led"
  led, err := myBoard.GPIOPinByName("8")
  if err != nil {
    logger.Fatalf("could not get led: %v", err)
  }

  //   Infinite loop that will blink the LED on and off.
  for {
    // When True, sets the LED pin to high/on.
    err = led.Set(context.Background(), true, nil)
    if err != nil {
      logger.Fatalf("could not set led to on: %v", err)
    }
    fmt.Println("LED is on")
    time.Sleep(1 * time.Second)

    // When False, sets the pin to low/off.
    err = led.Set(context.Background(), false, nil)
    if err != nil {
      logger.Fatalf("could not set led to off: %v", err)
    }
    fmt.Println("LED is off")
    time.Sleep(1 * time.Second)
  }
}
```

{{% /tab %}}
{{< /tabs >}}

You can run your code again by typing the following into the terminal:

{{< tabs >}}
{{% tab name="Python" %}}

```bash
python3 blink.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
go run blink.go
```

{{% /tab %}}
{{< /tabs >}}

And, if all goes well, you should see your LED blinking on and off again every second!

![A GIF of the completed project showing a hand hitting enter on the keyboard, then the blue LED starts to blink and the text "LED is on," and "LED is off" is printed out to the terminal onscreen.](../../img/make-an-led-blink-with-a-raspberry-pi-and-sdk/image6.gif)

You can exit this program by pressing **CTRL + C** in your terminal window.

If you get an error, you can check your code against my complete code here:

**Completed code**: <a href="https://github.com/viam-labs/LED-Blink" target="_blank">ht<span></span>tps://github.com/viam-labs/LED-Blink</a>

{{% alert title="Tip" color="tip" %}}
If you have any issues whatsoever getting the Viam SDK set up or getting your code to run on your Raspberry Pi, the best way to get help is over on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw).
There, you will find a friendly developer community of people learning how to make robots using Viam.
{{% /alert %}}

## Summary

In this tutorial, you learned the basics of controlling your robot using the Viam SDK by writing a short program in either Go or Python that makes an LED on your Raspberry Pi blink on and off.

If you are looking for some projects that would be a great next step in your journey of learning about how to build robots, check out one of following [Tutorial List](..).

If you want to connect with other developers learning how to build robots, or if you have any issues whatsoever getting Viam set up, let us know on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw), and we will be happy to help you get up and running.

## Components URL List

<ul>
    <li>Raspberry Pi 3 or 4: <a href="https://a.co/d/5Tn67G3" target="_blank">ht<span></span>tps://a.co/d/5Tn67G3</a></li>
    <li>Solderless breadboard: <a href="https://amzn.to/2Q4Z5Ta" target="_blank">ht<span></span>tps://amzn.to/2Q4Z5Ta</a></li>
    <li>Jumper wires for easy hookup: <a href="http://amzn.to/2qVhd4y" target="_blank">ht<span></span>tp://amzn.to/2qVhd4y</a></li>
    <li>Resistor pack: <a href="http://amzn.to/2Dmainw" target="_blank">ht<span></span>tp://amzn.to/2Dmainw</a></li>
    <li>Red LED: <a href="http://amzn.to/2Ex2v5q" target="_blank">ht<span></span>tp://amzn.to/2Ex2v5q</a></li>
</ul>
