---
title: "Make an LED Blink with a Raspberry Pi and Viam Python SDK"
linkTitle: "Blink an LED with a Pi and the SDK"
weight: 88
type: "docs"
description: "Intro to hardware programming using the Viam Python SDK to make an LED blink."
---
## Intro

In this post, you will be introduced to the basics of programming hardware by using the [Viam Python SDK](https://python.viam.dev/) to make an LED blink. This will allow you to write Python code to make an LED connected to the GPIO of a Raspberry Pi blink. This tutorial is a good introduction to Python programming, and developing code for hardware like robots and IoT devices.

![A GIF of the completed project showing a blinking blue LED connected to a Raspberry Pi with jumper cables.](../img/how-to-make-an-led-blink-with-a-raspberry-pi-and-python/image3.gif)


{{% alert title="Note" color="note" %}}  
This is part 2 of Viam's Intro to Robotics series. If you haven't completed [Part 1](../how-to-make-an-led-blink-with-a-raspberry-pi-using-viam/), be sure to go back and complete that before starting on this tutorial. I will be assuming that you have already set up [your Raspberry Pi](https://docs.viam.com/getting-started/installation/), [set up Viam Server](https://docs.viam.com/getting-started/installation/#installing-viam-server), built your circuit, and [connected your robot to the Viam App](https://docs.viam.com/getting-started/installation/#adding-your-pi-on-the-viam-app) before proceeding.

{{% /alert %}}

For reference, the circuit you are building for this tutorial looks like this:

![Circuit diagram showing a Raspberry Pi with a red connector running out of GPIO pin 8 to a 100-ohm* resistor*. The resistor is connected to the long lead of a red LED bulb. Finally, a blue connector connects the short lead of the LED to the ground connection on pin 6 of the Raspberry Pi GPIO pins.](../img/how-to-make-an-led-blink-with-a-raspberry-pi-and-python/image1.png)

{{% alert title="Tip" color="tip" %}}  
If you have any issues whatsoever getting Viam set up on your Raspberry Pi, let us know on the [Viam Community Slack](https://viamrobotics.slack.com), and we will be happy to help you get up and running.

{{% /alert %}}

## What you'll need for this guide

You will need the following hardware, tools, and software to complete this project:

### Hardware

[Click to view the Component URL Listing](#components-url-list)

<ol>
<li><a href="https://a.co/d/5Tn67G3" target="_blank">Raspberry Pi 3 or 4</a></li>
  
<ol type="a">

<li>Refer to the <a href="https://docs.viam.com/getting-started/installation" target="_blank">Viam Raspberry Pi Setup Guide </a> to setup your Pi.</li>

<li>Be sure that you have <a href="https://docs.viam.com/getting-started/installation/#installing-viam-server" target="_blank">set up Viam Server on your Raspberry Pi</a> as well.</li>

<li>Be sure that you are <a href="https://docs.viam.com/getting-started/installation/#installing-raspian-on-the-raspberry-pi">running Raspbian on your Pi.</a></li>

<li>You must also enable SSH on your Pi.</li>
</ol>
<li><a href="https://amzn.to/2Q4Z5Ta" target="_blank">Solderless breadboard</a></li>
<li><a href="http://amzn.to/2qVhd4y" target="_blank">Jumper wires for easy hookup</a></li>
<li><a href="http://amzn.to/2Dmainw" target="_blank">Resistor pack </a></li>
<OL type="a">
<li>You will be using a 100 Ohm resistor, which is the resistor with brown-black-brown bands</li>
</OL>
<li><a href="http://amzn.to/2Ex2v5q" target="_blank">Blue LED</a></li>
<li><a href="http://amzn.to/2qWurxS" target="_blank">Multimeter (optional)</a></li></ol>

### Software:

-   <a href="https://www.python.org/download/releases/3.0/" target="_blank">Python3</a>[^p3]

- <a href="https://pip.pypa.io/en/stable/#" target="_blank">Pip</a>[^pip]</a>
-   Viam Server: <a href="https://github.com/viamrobotics/rdk/tree/0c550c246739b87b4d5a9e8d96d2b6fdb3948e2b" target="_blank">ht<span></span>tps://github.com/viamrobotics/rdk/tree/0c550c246739b87b4d5a9e8d96d2b6fdb3948e2b</a>

[^pip]:Package Installer for Python (pip): <a href="https://pip.pypa.io/en/stable/#" target="_blank">ht<span></span>tps://pip.pypa.io/en/stable/#</a>

[^p3]: Python 3: <a href="https://www.python.org/download/releases/3.0/" target="_blank">ht<span></span>tps://www.python.org/download/releases/3.0/</a>

-   [Viam Python SDK](https://python.viam.dev/)

-   Install <a href="https://code.visualstudio.com/" target="_blank">Visual Studio Code</a>[^vsc] or <a href="https://code.visualstudio.com/insiders/" target="_blank">Visual Studio Code Insiders</a>[^vsci] on your development machine (not your Raspberry Pi).

[^vsc]:Visual Studio Code: <a href="https://code.visualstudio.com/" target="_blank">ht<span></span>tps://code.visualstudio.com/</a>
[^vsci]:Visual Studio Code Insiders: <a href="https://code.visualstudio.com/insiders/" target="_blank">ht<span></span>tps://code.visualstudio.com/insiders/</a>

## How to install the Viam Python SDK on your Raspberry Pi

If you followed along with the first part of this tutorial, you should be able to connect and control an LED on your robot remotely from the Viam App. Now, you will need to install the [Viam Python SDK](https://python.viam.dev/) on your Raspberry Pi. The SDK will allow you to automate your robot with more advanced logic, instead of just manually controlling components through the app.

You can find instructions for [installing the Viam Python SDK](https://python.viam.dev/) in the documentation, but we will break this down further for you here.

### How to SSH into a Raspberry Pi

What is SSH and why do we need to use it? The acronym SSH stands for *Secure Shell*. The SSH protocol was designed as a secure alternative to unsecured remote machines, like our Raspberry Pi. Basically, it allows you to access the command line of your Raspberry Pi from another machine so we can install software and run code remotely.

First, you will need to make sure your Raspberry Pi is plugged in, turned on, and connected to your network. I usually wait a minute or two after turning it on before I attempt to connect to my Pi.

{{% alert title="Note" color="note" %}}  
Make sure your Raspberry Pi and the computer you are using to SSH into your Raspberry Pi are connected to the same network.
{{% /alert %}}

Next, launch your terminal (on Mac and Linux) and replace the user and hostname with the user and hostname you configured when you set up your Pi. On Windows, you can use an SSH client such as <a href="https://itsfoss.com/putty-linux/" target="_blank">Putty</a>[^putty].


[^putty]:Putty: <a href="https://itsfoss.com/putty-linux" target="_blank">ht<span></span>tps://itsfoss.com/putty-linux</a>


```bash
ssh <username>@<hostname>.local
```

Default username and password on Raspberry Pi's are

-   username: pi

-   password: raspberry
-   
{{< alert title="Caution" color="caution" >}}  
It's bad practice to keep the default username and passwords since they make it easy for hackers to get access to your Pi. In the past, a malware infected thousands of Raspberry Pi devices that were using the default username and password.

See <a href="https://www.zdnet.com/article/linux-malware-enslaves-raspberry-pi-to-mine-cryptocurrency/" target="_blank">ht<span></span>tps://www.zdnet.com/article/linux-malware-enslaves-raspberry-pi-to-mine-cryptocurrency/</a>
{{< /alert >}}

[^malware]: ZD Net Article on Raspberry Pi Malware: <a href="https://www.zdnet.com/article/linux-malware-enslaves-raspberry-pi-to-mine-cryptocurrency/" target="_blank">ht<span></span>tps://www.zdnet.com/article/linux-malware-enslaves-raspberry-pi-to-mine-cryptocurrency/</a>

If you can't remember your user and hostname, you can also find out the IP address by other means like checking the network devices list on your router/modem.

You'll see a warning the first time you connect to your Pi via SSH, type **yes,** and press enter.

Next, type in your password and press enter.

On successful login, you'll be presented with the terminal of your Raspberry Pi. Now you can run any commands on your Raspberry Pi through this terminal remotely (within the current network) without having to access your Raspberry Pi physically.

### Installing pip on a Raspberry Pi
<a href="https://pip.pypa.io/en/stable/#" target="_blank">Package Installer for Python, aka, pip</a>[^pip] is the <a href="https://packaging.python.org/guides/tool-recommendations/" target="_blank"> official package installer for Python</a>[^pysoftrec].
You can use it to install packages from the <a href="https://pypi.org/" target="_blank">Python Package Index</a>[^pypack] and other indexes, such as the Viam Python SDK package. You can install pip by typing the following command into the terminal:

[^pypack]:Python Package Index: <a href="https://pypi.org/" target="_blank">ht<span></span>tps://pypi.org/</a>

[^pysoftrec]: Python Tool Recommendations<a href="https://packaging.python.org/guides/tool-recommendations/" target="_blank">ht<span></span>tps://packaging.python.org/guides/tool-recommendations/</a>[^pysoftrec]

```bash
sudo apt-get install python3-pip
```

### How to install the Viam Python SDK on a Raspberry Pi

In this step, you are going to install the [Viam Python SDK](https://python.viam.dev/) (Software Development Kit). This allows you to write programs in the Python programming language to create robots using [Viam](http://www.viam.com/).

To install the Viam Python SDK on your Raspberry Pi, you must run the following command in your terminal:

```bash
pip install viam-sdk
```

You can now close your terminal that is SSHed into your Raspberry Pi. With Viam, you can code robots from any machine without needing to be on the machine!

### How to initialize and connect your robot to the Viam App

Now that you have connected remotely to our Raspberry Pi and installed the Viam Python SDK on your Raspberry Pi, we can *finally* start writing some code.

On your local machine (not your Raspberry Pi), open up a new terminal window and type the following command to create a new file called, blink.py:

```bash
touch blink.py
```
Open up a code editor, like VS Code, you should now see a file in your explorer window called blink.py. Click on that file to open it in the code editor.

![A screenshot from Visual Studio Code that shows the file explorer. A red box is highlighting the new blink.py file located in the root directory.](../img/how-to-make-an-led-blink-with-a-raspberry-pi-and-python/image5.png)

Now, the easiest way to get started writing a Python application with Viam, is to navigate to the [robot page on the Viam App](https://app.viam.com/robots), select the **Connect** tab, and copy the boilerplate code from the section labeled **Python SDK**. This code snippet imports all the necessary libraries and sets up a connection with the Viam App in the cloud.

The Python SDK connect script should look something like this:

```python
  import asyncio
  
  from viam.robot.client import RobotClient
  from viam.rpc.dial import Credentials, DialOptions
  
  async def connect():
  creds = Credentials(
  type='robot-location-secret',
  payload='PLEASE ADD YOUR SECRET HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP')
  opts = RobotClient.Options(
  refresh_interval=0,
  dial_options=DialOptions(credentials=creds)
  )
  return await RobotClient.at_address('ADD YOUR ROBOT ADDRESS HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP', opts)
  
  async def main():
  robot = await connect()
  
  print('Resources:')
  print(robot.resource_names)
  
  await robot.close()
  
  if __name__ == '__main__':
  asyncio.run(main())
```

Next, paste that boilerplate code into your <file>blink.py</file> file in VS Code, and save your file.

{{% alert title="Tip" color="tip" %}}  
Your payload and address information will be different in your example, make sure that if you copy this code snippet, you copy and paste your credentials here.
{{% /alert %}}
You can now run the code. Doing so will ensure that the Python SDK is properly installed, that the viam-server instance on your robot is alive, and that the computer running the program is able to connect to that instance.

You can run your code by typing the following into the terminal:

```bash
python3 blink.py
```

If you successfully configured your robot and it is able to connect to the Viam App, you should see something like this printed to the terminal after running your program. What you see here is a list of the various resources, components, and services that have been configured to your robot in the Viam App.

![A screenshot from the Visual Studio Code command line that prints the output of print(robot.resource_names) when your Raspberry Pi has correctly connected and initialized with the Viam App. The output is an array of resources that have been pulled from the Viam App. Some of these are the Vision Service, Data Manager, and Board.](../img/how-to-make-an-led-blink-with-a-raspberry-pi-and-python/image4.png)

### How to write Python code to make an LED Blink

The first thing you need to do is import the [Board component](../../components/board/) from the Viam Python SDK. This component represents a physical general purpose board that contains GPIO pins. We will need this component in order to interact with the GPIO pins on our Raspberry Pi.

At the top of your blink.py file, paste the following:

```python
from viam.components.board import Board
```

Next, you will need to initialize the Raspberry Pi board, and you will need to tell Viam which GPIO pin your LED is on. Inside the `main()` function, and after the `print(robot.resource_names)`, paste the following:

```python
local = Board.from_robot(robot, 'local')

led = await local.gpio_pin_by_name('8')
```

Now that we have our board, and LED initialized, let's create an infinite loop that will blink the LED on and off. Directly after the code you pasted above, paste the following snippet:

```python
while (True):
    # When True, sets the LED pin to high or on.
    await led.set(True)
    print('LED is on')

    await asyncio.sleep(1)

    # When False, sets the pin to low or off.
    await led.set(False)
    print('LED is off')

    await asyncio.sleep(1)
```

You can run your code again by typing the following into the terminal:

```bash
python3 blink.py
```

And, if all goes well, you should see your LED blinking on and off again every second!

![A GIF of the completed project showing a hand hitting enter on the keyboard, then the blue LED starts to blink and the text "LED is on," and "LED is off" is printed out to the terminal onscreen.](../img/how-to-make-an-led-blink-with-a-raspberry-pi-and-python/image6.gif)

You can exit this program by click **CTRL + C** in your terminal window.

If you get an error, you can check your code against my complete code here:

**Completed code**: <a href="https://github.com/viamrobotics/LED-Blink" target="_blank">ht<span></span>tps://github.com/viamrobotics/LED-Blink</a>


{{% alert title="Tip" color="tip" %}}  
If you have any issues whatsoever getting the Viam Python SDK set up or getting your code to run on your Raspberry Pi, the best way to get help is over on the [Viam Community Slack](http://viamrobotics.slack.com). There, you will find a friendly developer community of people learning how to make robots using Viam.
{{% /alert %}}
![A GIF of the completed project showing a blinking blue LED connected to a Raspberry Pi with jumper cables.](../img/how-to-make-an-led-blink-with-a-raspberry-pi-and-python/image2.gif)

## Summary

In this tutorial, you learned how to remotely connect to a Raspberry Pi using SSH, you set up a Viam development environment on your Raspberry Pi, and learned the basics of controlling your robot using the Viam Python SDK.

If you are looking for some projects that would be a great next step in your journey of learning about how to build robots, I would recommend that you check out the following tutorials:

-  [Tutorial List](/tutorials/)

If you want to connect with other developers learning how to build robots, or if you have any issues whatsoever getting Viam set up, let us know on the [Viam Community Slack](http://viamrobotics.slack.com), and we will be happy to help you get up and running.

## Components URL List

<UL>
<li>Raspberry Pi 3 or 4: <a href="https://a.co/d/5Tn67G3" target="_blank">ht<span></span>tps://a.co/d/5Tn67G3</a></li>
<li>Solderless breadboard: <a href="https://amzn.to/2Q4Z5Ta" target="_blank">ht<span></span>tps://amzn.to/2Q4Z5Ta</a></li>
<li>Jumper wires for easy hookup: <a href="http://amzn.to/2qVhd4y" target="_blank">ht<span></span>tp://amzn.to/2qVhd4y</a></li>
<li>Resistor pack: <a href="http://amzn.to/2Dmainw" target="_blank">ht<span></span>tp://amzn.to/2Dmainw</a></li>
<li>Blue LED: <a href="http://amzn.to/2Ex2v5q" target="_blank">ht<span></span>tp://amzn.to/2Ex2v5q</a></li>
<li>Multimeter (optional): <a href="http://amzn.to/2qWurxS" target="_blank">ht<span></span>tp://amzn.to/2qWurxS</a></li>
</UL>
