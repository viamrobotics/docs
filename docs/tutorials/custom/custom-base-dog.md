---
title: "Control a Robot Dog with a Custom Viam Base Component"
linkTitle: "Custom Quadruped Base"
weight: 55
type: "docs"
tags: ["sdk", "extending viam", "components", "base", "python"]
description: "Integrate a custom base component with the Viam Python SDK."
webmSrc: "/tutorials/img/custom-base-dog/base-control-dog.webm"
mp4Src: "/tutorials/img/custom-base-dog/base-control-dog.mp4"
videoAlt: "A quadrupedal robot comprised of small servos, black laser cut acrylic, and with ultrasonic sensors for eyes, walks forward, backward, and turns from side to side on a desk. Next to it is a laptop with the robot's Control tab on the Viam app open in a browser window."
images: ["/tutorials/img/custom-base-dog/base-control-dog.gif"]
aliases:
    - /tutorials/custom-base-dog/
# SMEs: James Otting, Eric Daniels
# Author: Jessamy Taylor
---

The [base component type](/components/base/) is useful for controlling mobile robots because it gives users intuitive steering controls to use in code as well as from the [Viam app](https://app.viam.com/) remote control interface.

Viam natively supports a wheeled base model, but if you have a quadruped or other form of rover that isn't compatible with the wheeled model, you have two options:

1. Use Viam's Go SDK to [create a custom component as a modular resource](/extend/modular-resources/).
2. Use another Viam SDK (for example, the Python SDK) to [create a custom resource server](/extend/custom-components-remotes/).

This tutorial demonstrates option two, using [this robot dog kit and its open source code](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi) as an example.

<div class="alignleft">
  {{<gif webm_src="../../img/custom-base-dog/base-control-dog.webm" mp4_src="../../img/custom-base-dog/base-control-dog.mp4" alt="A quadrupedal robot comprised of small servos, black laser cut acrylic, and with ultrasonic sensors for eyes, walks forward, backward, and turns from side to side on a desk. Next to it is a laptop with the robot's Control tab on the Viam app open in a browser window." max-width="400px">}}
</div>

By the end of the tutorial, you will be able to drive this dog around using the Viam base methods: `MoveStraight`, `Spin`, `SetPower`, `SetVelocity`, and `Stop`.
You will also be able to use the **Control** tab in the Viam app to remotely drive the dog around using your keyboard while viewing the camera feed.
You’ll learn to implement a custom component type in Viam, and you’ll be equipped to implement other sorts of custom components in the future for whatever robots you dream up.

## Code used in this tutorial

- [Robot Dog Base Code on GitHub](https://github.com/viam-labs/robot-dog-base)

- [Freenove Robot Dog Kit for Raspberry Pi Code on GitHub](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/tree/master/Code)

## Hardware requirements

- [Freenove Robot Dog Kit for Raspberry Pi](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi)
  - Currently (24 January 2023) [available on Amazon](https://www.amazon.com/gp/product/B08C254F73/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
  - Significant assembly is required.
  Follow Freenove hardware assembly instructions before starting this tutorial.
- Raspberry Pi 4B

## Raspberry Pi setup

Freenove documentation includes Raspberry Pi setup instructions but we recommend the following steps to make sure the Pi is set up for this tutorial:

1. Follow the steps in our [Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/) to install Raspberry Pi OS Lite (64 bit).

{{% alert title=Note color="note" %}}

If you choose to install the full Raspberry Pi OS (64 bit) including the desktop environment and recommended software (as Freenove instructs in Chapter 0 of their tutorial), that will also work.

{{% /alert %}}

1. [Install `viam-server` and connect your robot to the Viam app](/installation#install-viam-server).

2. SSH into the Pi to complete the following steps.

3. Install pip and then git:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    sudo apt install pip
    ```

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    sudo apt install git
    ```

4. Navigate to the directory on the Pi where you'd like to install the Freenove robot dog code (for example `/home/fido/`).
Get the code by running the following command:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    git clone https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi
    ```

{{% alert title="Note" color="note" %}}

This tutorial uses `/home/fido/` as an example home directory in various example filepaths and code snippets.
If the name of the directory where you store and run your code is different, be sure to use the correct filepath when running these commands.

{{% /alert %}}

6. Check which version of Python you have installed on the Pi:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    python --version
    ```

    If it isn’t Python 3.8 or later, install an updated version of Python and double-check that you're running the latest Raspberry Pi OS.

7. Install the [Viam Python SDK](https://python.viam.dev/):

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    pip install viam-sdk
    ```

8. Enable I<sup>2</sup>C per [the instructions in the Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/#enable-communication-protocols).

9. Alter the I<sup>2</sup>C baud rate according to [Chapter 1, Step 2 in the Freenove instructions](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/blob/master/Tutorial.pdf) (page 40 as of January 24, 2023).

10. Install smbus so that the servo code works:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    sudo apt-get install python3-smbus
    ```

11. Follow Chapter 1, Step 3 (page 42 as of January 24, 2023) of the Freenove tutorial to complete the software installation:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    cd /home/fido/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code
    sudo python setup.py
    ```

12. Restart the Raspberry Pi:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    sudo reboot
    ```

## Hardware setup

Follow the Freenove hardware assembly instructions, including servo setup (all of Chapters 2 and 3, and the section of Chapter 4 about calibration) before proceeding.

## Check connection between the robot dog server and the midlayer

Before proceeding with the custom component implementation, follow the instructions in this section to test the connection between the Freenove server running on your robot dog and the code running on your development machine (laptop or desktop).
This way, you can isolate any client-server connection problems if you encounter one.

### Create a connection test file

In a convenient directory on your development machine, create a Python file and open it in your favorite IDE.
We named ours "dog_test.py" and opened it in Visual Studio Code.

Paste the following code snippet into the file you created:

```python {class="line-numbers linkable-line-numbers"}
# dog_test.py is for testing the connection

import socket, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("PASTE DOG IP ADDRESS HERE", 5001))

cmd = "CMD_MOVE_FORWARD#8"
s.send(cmd.encode("utf-8"))
time.sleep(8)
cmd = "CMD_MOVE_STOP"
s.send(cmd.encode("utf-8"))
cmd = "CMD_RELAX"
s.send(cmd.encode("utf-8"))
```

Save the file.

### Find IP address

Go to the [robot page](https://app.viam.com/robots) for your robot dog that you created when installing `viam-server` on the Pi.

In the banner towards the top of the page, the IP address of the robot dog Pi is displayed under **ips**.
Copy the IP to your clipboard.
Inside <file>dog_test.py</file>, replace `PASTE DOG IP ADDRESS HERE` with the copied IP.
Save the file.

### Test the connection

Place the robot dog on a flat, open surface where it has room to take a few steps.

Now you are ready to run the connection test file.

Open two terminal windows on your development machine: one for the robot dog Pi and one for the development machine.

In one terminal, SSH into the Pi using the username and hostname you set up when imaging the Pi, for example:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
ssh fido@robotdog.local
```

Navigate to the <file>/home/fido/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code/Server</file> directory.

Start the robot dog server by running:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo python main.py -tn
```

In the other terminal window, navigate to the directory on your development machine where you saved <file>dog_test.py</file>.
Run the connection test file with the following command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python dog_test.py
```

If the dog walks forward for a few seconds and then stops, the connection works and you can successfully send commands to the robot dog server.
Continue on to implement the base.

If the robot dog did not respond, double check your IP address, make sure the robot dog server is still running, and make sure the robot has adequate power.
You can also try turning the robot off and on again, and then retrying the process.

## Implement the custom base code

From the Raspberry Pi terminal, create a directory inside the home directory to hold your custom code files:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
mkdir RobotDog
```

### Define the custom base interface

To create a custom base model, you need to subclass the base component type.
In other words, you need a script that defines what each base component method (for example `set_power`) makes the robot dog do.

Take a look at [<file>my_robot_dog.py</file>](https://github.com/viam-labs/robot-dog-base/blob/main/my_robot_dog.py).
It creates a "RobotDog" model of the base component type, and defines the `set_power`, `stop`, `is_moving`, and `do` methods by specifying which corresponding commands to send to the Freenove dog server when each of these methods is called.
For example, the `stop` method sends a command (`CMD_MOVE_STOP#8`) to the robot dog server to stop the dog from moving:

```python
    async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self.is_stopped = True

        command = "CMD_MOVE_STOP#8\n"
        self.send_data(command)
```

Feel free to tweak the specific contents of each of these method definitions, and add support for other base methods like `spin`.
You can [read about the base API here](/components/base/#api).

Save [<file>my_robot_dog.py</file>](https://github.com/viam-labs/robot-dog-base/blob/main/my_robot_dog.py) into the <file>RobotDog</file> directory you created.

### Register the custom component

Now that you defined the methods for the custom component, you need to make your custom component available to any robots trying to connect to it.

Save [<file>python_server.py</file>](https://github.com/viam-labs/robot-dog-base/blob/main/python_server.py) into the <file>RobotDog</file> directory.
The <file>python_server.py</file> file creates an RPC server that forwards {{< glossary_tooltip term_id="grpc" text="gRPC" >}} requests from `viam-server` (or elsewhere) to the custom component.

## Configure the custom component server as a remote

You need to tell your robot how to access the custom component server you created.
This is accomplished by configuring the custom component server as a *remote*.

Back over on the [Viam app](https://app.viam.com), go to your robot's **Config** tab.
Click the **Remotes** sub-tab.
Name your remote "my-custom-base" and click **Create Remote**.
In the **Address** field put `localhost: 9090`.
Click **Save Config** at the bottom of the page.

![Screenshot of the Viam app CONFIG tab with the Remotes sub-tab open, showing my-custom-base configured as a remote.](../../img/custom-base-dog/remote-config.png)

{{% alert title="Note" color="note" %}}

When you call srv.serve(), the default host and port is localhost:9090.
If you want to use a different host or port, pass it as a parameter to the serve function.

{{% /alert %}}

## Configure the components

Now that the custom base code is set up, you need to configure all your hardware components.
Navigate to the **Components** sub-tab of the **Config** tab.

### Configure the base

In the **Create Component** field, give your base a name.
We called ours "quadruped".
In the **Type** drop-down select `base`.
In the **Model** field, type in "RobotDog".
Click **Create Component**.

You don't need to add any attributes to the base component.

Click **Save Config**.

### Configure the camera

Configure the ribbon camera on the dog as a `webcam` following our [webcam documentation](/components/camera/webcam).

## Start the servers

To operate the dog, you need to start the two servers in order:

- First, the Freenove robot dog server (which you saved as <file>/home/fido/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code/Server/main.py</file>).
- Then, the custom component server (<file>/home/fido/RobotDog/python-server.py</file>).
  This one must be started second because it sends requests to the Freenove dog server, so it will throw errors if it can't find that server when it tries to start.

<!---

# ADD THIS BACK IN AFTER APP-1227 IS DONE. TEST IT FIRST.

You have two options for starting the servers: automatic or manual.

### Option 1: Configure processes to automatically start the servers on boot

Click the **Processes** sub-tab of the **Config** tab.

Create a new process and give it a name (for example "1st").
Once configured, this process will start the Freenove robot dog server so it is ready to receive commands from the custom component server.
Fill out the config panel as follows:

- **Working Directory**: `/home/fido/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code/Server` (changing "/home/fido" to the name of your home directory where you downloaded the Freenove code)
- **Logging**: Toggle to the on position so you can view logs for this server process
- **Arguments**: `main.py -tn` so that the Freenove server starts without launching their GUI
- **Command**: `python main.py`

Create a second process to start the custom component server.
Configure it like this:

- **Working Directory**: `/home/fido/RobotDog` (changing "/home/fido" to the correct path)
- **Logging**: Toggle to the on position so you can view logs for this server process
- **Arguments**: python_server.py
- **Command**: `python`

Click **Save Config** at the bottom of the window.

![Screenshot of the Processes sub-tab of the Config tab, showing two processes configured as detailed above.](../../img/custom-base-dog/process-config.png)

{{% expand "Click to see what the processes config will look like in Raw JSON mode." %}}

```json
"processes": [
    {
      "log": true,
      "name": "python",
      "id": "1st",
      "cwd": "/home/fido/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code/Server",
      "args": [
        "main.py",
        -tn"
      ]
    },
    {
      "args": "python_server.py",
      "id": "2nd",
      "log": true,
      "name": "python",
      "cwd": "/home/fido/RobotDog"
    }
  ]
```

{{% /expand %}}

{{% alert title="Note" color="note" %}}

We added a 5 second time delay to the [<file>python_server.py</file>](https://github.com/viam-labs/robot-dog-base/blob/main/python_server.py#L15) code so that even though these two processes will start simultaneously, there will be time for the Freenove server to start up before the custom component server starts sending requests to it.

{{% /alert %}}

### Option 2: Start the processes manually from the command line

If you prefer, you can start the processes manually from command terminals on the Pi.

--->

From the <file>home/fido/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code/Server/</file> directory start the Freenove robot dog server:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo python main.py -tn
```

Then, open another terminal, SSH to the Pi, and navigate to the directory where you saved your custom Viam component code (for example, <file>/home/fido/RobotDog/</file>).
Start the custom component server by running:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python python_server.py
```

## Driving the robot from the Viam app

Navigate to the **Control** tab.

Click the **my-custom-base:my-robot-dog** component panel to expand it and reveal the controls.

![Screenshot of the Control tab with the custom base card expanded to reveal arrow control buttons.](../../img/custom-base-dog/control-tab.png)

1. Enable the camera stream from the **Select Cameras** drop-down.
2. Toggle the **Keyboard Disabled** switch to **Keyboard Enabled** to use the WASD keys on your keyboard.
3. Use the **W**, **A**, **S** and **D** buttons to make the robot walk forward, turn left, walk backward or turn right.

{{% alert title="Note" color="note" %}}

Depending on the speed of your server connection, you may need to hold down the base control button/key for a second or two before anything happens.

{{% /alert %}}

## Troubleshooting

- If your servos aren't moving as expected or at all, try turning the whole robot off for a while to let them cool down.

- Make sure the robot's batteries have adequate charge.
If you have otherwise unexplained connection errors, try powering things off and charging the batteries for a while before attempting to SSH to the Pi again.

- If certain sensors or servos aren't being found by the software, turn off the robot and make sure all wires are fully connected before turning it back on.

- If you want to send commands directly to the dog server instead of running <file>my_robot_dog.py</file> (which may be helpful for debugging specific commands, especially if you're adding your own functionality and need to calibrate servo speeds/positions) you can do the following:

  1. Install Netcat if it isn't already installed:

      ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      sudo apt install netcat
      ```

  2. Connect directly to the robot dog by running the following command (replacing <DOG IP ADDRESS> with the correct IP address, for example `nc 10.0.0.123`) from the command line while SSHed into the Pi:

      ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      nc <DOG IP ADDRESS> 5001
      ```

  3. You can now type commands ([see the list of available commands here](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/blob/master/Code/Client/Command.py)) and hit enter to send them to the Freenove robot dog server.
    For example:

      ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      CMD_TURN_LEFT#30
      CMD_STOP
      ```

## Next steps

In this tutorial you learned how to implement a custom component model and control it using the Viam app.
You learned about configuring remotes and processes.
You drove the robot dog around using the Viam **Control** tab.

To add more functionality, try defining more of the base API methods for this model.
You could also use the Viam [Vision Service](/services/vision/) with the robot dog's [camera component](/components/camera/).
For example, you could write code to tell the robot dog to [move towards a colored target](/tutorials/services/color-detection-scuttle/) or to [follow a colored line](/tutorials/services/webcam-line-follower-robot/), similarly to how these tasks are done with wheeled bases in the tutorials linked here.

{{< snippet "social.md" >}}
