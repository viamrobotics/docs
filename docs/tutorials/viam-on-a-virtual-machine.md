---
title: "How to setup Viam-Server on a Linux virtual machine hosted on Windows"
linkTitle: "Viam-server on a Linux VM on Windows"
weight: 120
type: "docs"
description: "This tutorial provides instructions to install and configure the viam-server on virtual machine hosted on Windows."
tags: ["mock", "simulation", "virtual machine", "Windows"]
---

**Objective**: Setup and configure viam-server and a mock robot in a linux virtual machine (VM) hosted on Windows.

## What you’ll need for this tutorial

* A laptop or desktop running Windows 10 or 11.
* *Python 3.9+.
* A code editor of your choice.

## Introduction

Since Viam-server only operates in linux and macOS environments, a virtual machine running a supported OS is the only way for Windows users to natively operate Viam from a Windows PC.

Using a linux virtual machine provides Windows users with a means to use Viam to configure and operate robots.

This tutorial will demonstrate the steps to install and configure Virtual Box, its extension pack, and an Ubuntu virtual machine to operate with Viam.

### Requirements

#### Windows software

* VirtualBox
* VirtualBox Extension Pack
* SSH Terminal software (e.g., Putty, TeraTerm, etc.)

{{% alert title="Note" color="note"%}}
VMare may be a viable option for hosting VMs for use with Viam.
However, VMware has not been tested (15 Dec 2022).
{{% /alert %}}

## Setup the Windows PC

### Install VirtualBox and the VirtualBox Extension Pack

Download and install VirtualBox and the VirtualBox Extension Pack from <a href="https://www.virtualbox.org/wiki/Downloads"  target="_blank">Virtual Box</a>[^vbox].

^[vbox]:VirtualBox and the VirtualBox Extension Pack download page: <a href="https://www.virtualbox.org/wiki/Downloads" target="_blank">https://www.virtualbox.org/wiki/Downloads</a>

### Download and install the VM image

Download the Ubuntu image: Ubuntu 22.04 LTS, "Jammy Jellyfish," from <a href="https://www.linuxvmimages.com/images/ubuntu-2204/ ">
LinuxVMImages.com</a>[^ubuimage]

[^ubimage]:Ubuntu 22.04 LTS, "Jammy Jellyfish," virtual image from Linuxvmimages: <<a href="https://www.linuxvmimages.com/images/ubuntu-2204/">ht<span></span>tps://www.linuxvmimages.com/images/ubuntu-2204/</a>

Once the download (Ubuntu_22.04_VB.7z) is complete, use 7-zip to extract the image file.
Next, double-click the image file (<file>Ubuntu_22.04_VB_LinuxVMImages.COM.vbox</file>) to add the image to VirtualBox.

#### Virtual machine image configuration

On the Oracle Virtual Machine Manager, configure the following settings for the VM image.
Ensure that you've selected the Ubuntu image (or the image you chose to use) before continuing:

{{< figure src="../img/viam-on-vm/vm-config.png" width="400px" alt="Oracle VM VirtualBox Manager with the Ubuntu image selected." title="Oracle VM VirtualBox Manager." >}}

{{% alert title="Note" color="note"%}}
The virtual machine must be powered off to change its configuration.
{{% /alert %}}

1. Navigate to: Settings > General > Advanced, then set **Shared Clipboard** and **Drag'n'Drop** to "Bidirectional" for ease of use.

1. Navigate to: Settings > System > Motherboard.
In this tutorial, we operated the VM with 4GB of the available memory.
Allocate at least 4GB to the VM.

1. Navigate to: Settings > USB, select (check) **Enable USB Controller**, and then select a USB controller.
The Laptop in this tutorial uses the laptop's USB 3.0 xHCI Controller.
Choose the most current USB revision for your image.

Verify that the image launches by clicking **Start** on the WM VirtualBox Manager's toolbar with the Ubuntu image selected:

#### Packages in VM images

Virtual machines contain the most common packages for their OS as determined by the VM image creator.
Therefore, a VM image obtained from _any_ source might not contain all of the packages required by Viam.

#### Required packages not in the image

Login to the Ubuntu VM using the provided credentials to complete the steps in this section.

* Ubuntu_22.04_VB_LinuxVMImages VM Credentials
  * username: ubuntu
  * password: ubuntu
  * Root account password: ubuntu

{{< alert title="Note" color="note" >}}
Perform an <file>apt update</file> to update the package list and an <file>apt upgrade</file> to update all packages to the latest revision before checking that the VM is current.
{{< /alert >}}

The VM image for this tutorial does not contain three packages required by Viam.
Add these packages to the VM:

* curl - The installation procedure requires curl.<br>
<file>sudo apt install curl</file>

* libfuse2 - Viam-server requires libfuse2.
If your VM image uses FUSE3, libfuse2 is most likely _not_ installed and you must install libfuse2.<br>
<file>sudo apt-get install libfuse2</file>

* pip - The installation procedure requires pip.<br>
<file>sudo apt install python3-pip</file>

{{% alert title="Info" color="tip" %}}
The missing packages were identified through trial and error during installation.
If you decide to use a different virtual machine or image, and the installation script fails, determine whether the errors are the result of a missing package or library and if so, retry the script after installing them.
{{% /alert %}}

## Setup in the Viam app

### Setup an account on the Viam app

If you do not already have an account on the Viam app, go to app.viam.com and sign up.
Please refer to [Getting Started with the Viam App](https://docs.viam.com/getting-started/app-usage/) for complete details.

You will need to create an Organization, a Location, and then add a robot.

### Install the viam-server and Viam app config

For this section, you will perform steps listed on the [Robots](https://app.viam.com/robots) page in the VM's terminal window.

Having logged in to your account, click the robot you created in the previous section to access its configuration and follow these steps to continue.

1. Click **SETUP**.
1. Set **Mode** to "Linux."
1. Set **Architecture** to "X86_64."
1. Perform Step 1, "Download Viam app config to your computer."
Click **COPY** on Step 1, then paste into the terminal window and press **Enter**.
This step downloads the viam-server configuration file used by your robot to connect to app.viam.com.
1. Perform Step 2, "Download and install viam-server"
Click **COPY** on Step 2, then paste into the terminal window and press **Enter**.
This step downloads and installs the most recent stable viam-server AppImage package.

If the configuration is correct, then the app displays a connection confirmation beneath Step 3 after a short wait, :

{{< figure src="../img/viam-on-vm/successful-connection.png" width="400px" alt="Successful connection message." title="Successful connection message." >}}

## Create a mock robot

This section adds a fake motor and arm in the same manner as the [How to Build a Mock Robot](../tutorials/build-a-mock-robot/) tutorial.
When you add the fake motor and arm component to your robot, the Viam app automatically generates a UI for the motor and arm under the **CONTROL** tab.

{{< figure src="../img/viam-on-vm/vm-bot-created.png" width="800px" alt="The GUI interface for your mock robot displays configuration pane a pane for each fake component and a pane for the DoCommand and for Operations & Sessions." title="The GUI interface for your mock robot." >}}

Perform these steps on your robot's **CONFIG** tab in the Viam-app:

1. Navigate to the **CONFIG** tab.
1. Create a fake arm component
    1. Navigate to the **Create a Component** pane at the bottom of the page.
    1. Enter the desired name for the arm component.
    1. Select "arm" from the **Type** drop-down.
    1. Select "fake" from the **Model** drop-down.
1. Create a Fake Motor Component
    1. Navigate to the **Create a Component** pane at the bottom of the page.
    1. Enter the desired name for the motor component.
    1. Select "motor" from the **Type** drop-down.
    1. Select "fake" from the **Model** drop-down.  
1. Click **Save Config**.

{{% alert title="Caution" color="caution" %}}  
Do not share your robot secret or robot address publicly. Sharing this information compromises your system security by allowing unauthorized access to your computer.
{{% /alert %}}

### Control the mock robot arm

While connected to the robot, you can verify the operation of the fake arm from the **CONTROL** tab or through code, which would allow you to control and observe to positioning of the arm component in the terminal and in the GUI.

#### Using the GUI

In the GUI, you can click **Modify All** to change the X, Y, and Z positions for joints in the arm. 

### Using the SDK

Alternatively, you can programmatically perform random changes and observe the returned positional value changes in the terminal, as well as on the **CONTROL** tab using either the Python SDK or the GO SDK.

The next section describes the process for Python.

#### Creating the arm control code

Paste the boilerplate code from the CODE SAMPLE tab of the Viam app into a file named <file>arm-move.py</file> or into your code editor.
<file>arm_move.py</file> imports the arm component from the Viam Python SDK and imports the random and async.io libraries.
The code from the CODE SAMPLE tab can only connect your robot to the viam app.

At the top of your <file>arm_move.py</file> file, paste the following lines:

``` python
from viam.components.arm import ArmClient, JointPositions
import random
import asyncio
```

Next, insert the following lines after: <code>from viam.rpc.dial import Credentials, DialOptions</code>:

```python
arm = ArmClient.from_robot(robot=robot, name='my_main_arm')

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

Save the file.
These lines generate the random movements we will use to test the robot.

In the VM's terminal window, run the following command:

``` bash
python3 arm-move.py
```

{{< figure src="../img/viam-on-vm/observing-arm-changes.gif" width="800px" alt="The CONTROL tab and a terminal window displaying arm geometry changes generated by arm-move.py." title="The CONTROL tab and a terminal window displaying arm geometry changes generated by arm-move.py." >}}

## Next Steps

In this tutorial, you learned how to create a mock robot using fake components on a Linux virtual machine a Windows host.

If you're ready to get started with building robots with real hardware components, you should pick up a Raspberry Pi and try building one of Viam's introductory robots on the [tutorials page in our documentation](https://docs.viam.com/tutorials/).

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, be sure that you head over to the [Viam Community Slack](http://viamrobotics.slack.com).
