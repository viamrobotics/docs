---
title: "Control a Robot Dog with a Custom Viam Base Component"
linkTitle: "Custom Quadruped Base"
type: "docs"
tags:
  ["sdk", "extending viam", "components", "base", "python", "modular resources"]
description: "Integrate a custom base component with the Viam Python SDK."
videos:
  [
    "/tutorials/custom-base-dog/base-control-dog.webm",
    "/tutorials/custom-base-dog/base-control-dog.mp4",
  ]
videoAlt: "A quadrupedal robot comprised of small servos, black laser cut acrylic, and with ultrasonic sensors for eyes, walks forward, backward, and turns from side to side on a desk. Next to it is a laptop with the machine's Control tab"
images: ["/tutorials/custom-base-dog/base-control-dog.gif"]
aliases:
  - /tutorials/custom-base-dog/
authors: ["Jessamy Taylor"]
languages: ["python"]
viamresources: ["base", "camera", "custom"]
platformarea: ["registry"]
level: "Intermediate"
date: "2023-05-15"
updated: "2024-05-07"
cost: 190
# SMEs: James Otting, Eric Daniels
---

<!-- LEARNING GOAL:
After following this tutorial, you will know about Viam's modules and be able to identify if you need to create your own modular resource for your base, as well as how to create and use that resource.

Consider if can be merged with intermode rover one to create more generalized guidance.
 -->

The [base component type](/operate/reference/components/base/) is useful for controlling mobile robots because it gives users intuitive steering controls to use in code as well as from the machine's **CONTROL** tab.

Viam natively supports a wheeled base model, but if you have a quadruped or other form of base that requires a different underlying implementation, you can create a custom component as a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}.

This tutorial demonstrates how to add a custom base using [this robot dog kit and its open source code](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi) as an example.

<div class="alignleft">
  {{<gif webm_src="/tutorials/custom-base-dog/base-control-dog.webm" mp4_src="/tutorials/custom-base-dog/base-control-dog.mp4" alt="A quadrupedal robot comprised of small servos, black laser cut acrylic, and with ultrasonic sensors for eyes, walks forward, backward, and turns from side to side on a desk. Next to it is a laptop with the machine's control tab." max-width="400px">}}
</div>

By the end of the tutorial, you will be able to drive this dog around using the Viam base methods: `MoveStraight`, `Spin`, `SetPower`, `SetVelocity`, and `Stop`.
You will also be able to use the machine's **CONTROL** tab to remotely drive the dog around using your keyboard while viewing the camera feed.
You’ll learn to implement a custom component type in Viam, and you’ll be equipped to implement other sorts of custom components in the future for whatever robots you dream up.

## Code used in this tutorial

- [Module Generator](https://github.com/viam-labs/generator-viam-module)
- [Robot Dog Base Code on GitHub](https://github.com/viam-labs/robot-dog-module)
- [Freenove Robot Dog Kit for Raspberry Pi Code on GitHub](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/tree/master/Code)

## Hardware requirements

- [Freenove Robot Dog Kit for Raspberry Pi](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi)
  - Currently (05 July 2023) [available on Amazon](https://www.amazon.com/gp/product/B08C254F73/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
  - Significant assembly is required.
    Follow Freenove hardware assembly instructions before starting this tutorial.
- Raspberry Pi 4B

## Raspberry Pi setup

Freenove documentation includes Raspberry Pi setup instructions but we recommend the following steps to make sure the Pi is set up for this tutorial:

Follow the steps in our [Raspberry Pi Setup Guide](/operate/reference/prepare/rpi-setup/) to install Raspberry Pi OS.

{{% alert title=Note color="note" %}}

If you choose to install the full Raspberry Pi OS (64 bit) including the desktop environment and recommended software (as Freenove instructs in Chapter 0 of their tutorial), that will also work.

{{% /alert %}}

{{% snippet "setup.md" %}}

1.  SSH into the Pi to complete the following steps.

1.  Install pip and then git:

    ```sh {class="command-line" data-prompt="$"}
    sudo apt install pip
    ```

    ```sh {class="command-line" data-prompt="$"}
    sudo apt install git
    ```

1.  Navigate to the directory on the Pi where you'd like to install the Freenove robot dog code (for example `/home/fido/`).
    Get the code by running the following command:

    ```sh {class="command-line" data-prompt="$"}
    git clone https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi
    ```

    {{% alert title="Important" color="note" %}}

This tutorial uses `/home/fido/` as an example home directory in various example filepaths and code snippets.
If the name of the directory where you store and run your code is different, be sure to use the correct filepath when running these commands.

    {{% /alert %}}

1. Check which version of Python you have installed on the Pi:

   ```sh {class="command-line" data-prompt="$"}
   python --version
   ```

   If it isn’t Python 3.8 or later, install an updated version of Python and double-check that you're running the latest Raspberry Pi OS.

1. Install the [Viam Python SDK](https://python.viam.dev/):

   ```sh {class="command-line" data-prompt="$"}
   pip install viam-sdk
   ```

1. Enable I<sup>2</sup>C per [the instructions in the Raspberry Pi Setup Guide](/operate/reference/prepare/rpi-setup/#enable-communication-protocols).

1. Alter the I<sup>2</sup>C baud rate according to [Chapter 1, Step 2 in the Freenove instructions](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/blob/master/Tutorial.pdf) (page 40 as of January 24, 2023).

1. Install smbus so that the servo code works:

   ```sh {class="command-line" data-prompt="$"}
   sudo apt-get install python3-smbus
   ```

1. Follow Chapter 1, Step 3 (page 42 as of January 24, 2023) of the Freenove tutorial to complete the software installation:

   ```sh {class="command-line" data-prompt="$"}
   cd /home/fido/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code
   sudo python setup.py
   ```

1. Restart the Raspberry Pi:

   ```sh {class="command-line" data-prompt="$"}
   sudo reboot
   ```

## Hardware setup

Follow the Freenove hardware assembly instructions, including servo setup (all of Chapters 2 and 3, and the section of Chapter 4 about calibration) before proceeding.

## Check connection between the robot dog server and the midlayer

Before proceeding with the custom component implementation, follow the instructions in this section to test the connection between the Freenove server running on your robot dog and the code running on your development machine (laptop or desktop).
This way, you can isolate any client-server connection problems if they exist.

### Create a connection test file

In a convenient directory on your development machine, create a Python file and open it in your favorite IDE.
We named ours <file>dog_test.py</file> and opened it in Visual Studio Code.

Paste the following code snippet into the file you created:

```python {class="line-numbers linkable-line-numbers"}
# dog_test.py is for testing the connection
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("PASTE DOG IP ADDRESS HERE", 5001))

cmd = "CMD_MOVE_FORWARD#15"
s.send(cmd.encode("utf-8"))
time.sleep(7)
cmd = "CMD_MOVE_STOP"
s.send(cmd.encode("utf-8"))
cmd = "CMD_RELAX"
s.send(cmd.encode("utf-8"))
```

Save the file.

### Find IP address

Go to the [machine page](https://app.viam.com/robots) for your robot dog that you created when installing `viam-server` on the Pi.

Open the part status dropdown in the top left of the page.
If your machine is connected to the app, this should say **Live**.
The IP address of the robot dog Pi is displayed under **IPs**.
Click the copy icon to copy the IP address to your clipboard.
Inside <file>dog_test.py</file>, replace `PASTE DOG IP ADDRESS HERE` with the copied IP.
Save the file.

### Test the connection

Place the robot dog on a flat, open surface where it has room to take a few steps.
Make sure it is powered on.

Now you are ready to run the connection test file.

Open two terminal windows on your development machine: one for the robot dog Pi and one for the development machine.

In one terminal, SSH into the Pi using the username and hostname you set up when imaging the Pi, for example:

```sh {class="command-line" data-prompt="$"}
ssh fido@robotdog.local
```

Navigate to the <file>/home/fido/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code/Server</file> directory.

Start the robot dog server by running:

```sh {class="command-line" data-prompt="$"}
sudo python main.py -tn
```

In the other terminal window, navigate to the directory on your development machine where you saved <file>dog_test.py</file>.
Run the connection test file with the following command:

```sh {class="command-line" data-prompt="$"}
python dog_test.py
```

If the dog walks forward for a few seconds and then stops, the connection works and you can successfully send commands to the robot dog server.
Continue on to implement the base.

If the robot dog did not respond, double check your IP address, make sure the robot dog server is still running, and make sure the robot has adequate power.
You can also try turning the robot off and on again, and then retrying the process.

## Implement the custom base code

Now that the Freenove server is set up, you will follow the [process for creating modular resources](/operate/get-started/other-hardware/create-module/).

### Prerequisites

{{< expand "Install the Viam CLI and authenticate" >}}
Install the Viam CLI and authenticate to Viam, from the same machine that you intend to upload your module from.

{{< readfile "/static/include/how-to/install-cli.md" >}}

Authenticate your CLI session with Viam using one of the following options:

{{< readfile "/static/include/how-to/auth-cli.md" >}}
{{< /expand >}}

### Create the module files

The CLI module generator generates the files for your modular resource.

1. Run the following command in your terminal:

   ```sh {class="command-line" data-prompt="$"}
   viam module generate
   ```

2. Follow the prompts, selecting the following options:

   - Module name: `base`
   - Language: `Python`
   - Visibility: `Private`
   - Namespace/Organization ID:
     - Navigate to your organization settings through the menu in upper right corner of the page.
       Find the **Public namespace** (or create one if you haven't already) and copy that string.
       In the example snippets below, the namespace is `viamlabs`.
   - Resource to add to the module (API): `Base Component`.
   - Model name: `robotdog`
   - Enable cloud build: `No`
   - Register module: `Yes`

   It's a good idea to use the same names, aside from the namespace.
   That way your code will match the example code.

   You can use a different model name, module namespace, and module name, but you need to use the existing API triplet `rdk:component:base` in order for your custom base to work properly as a base.

3. Hit your Enter key and the generator will generate a folder called <file>robotdog</file> containing stub files for your modular base component.

Look inside the <file>src</file> subdirectory which now contains <file>main.py</file>.
<file>main.py</file> is the file that defines the behavior of your custom base.
This is the file you will modify in the next steps.

### Connect the module to the Freenove server

When you send a command to the robot using the Viam [base API](/dev/reference/apis/components/base/#api), you need a way to pass the corresponding command to the Freenove dog server.
In your code, establish a socket and then create a `send_data` helper method to send the command from `viam-server` to the Freenove server.

Start by importing socket:

```python
import socket
```

Then add `ip_address` and `port` attributes to your custom base so you can configure the correct connection details in your machine's config later.
Modify the `validate` and `reconfigure` methods to use these attributes, and define the `send_data` method.
The code below shows what the top of your class definition should look like.

```python {class="line-numbers linkable-line-numbers"}
class robotdog(Base, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("viamlabs", "base"), "robotdog")

    # Class parameters
    ip_address: str
    port: int

    # Constructor
    @classmethod
    def new(cls,
            config: ComponentConfig,
            dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        # Here we validate config, ensuring that an IP address was provided
        ip_address = config.attributes.fields["ip_address"].string_value
        if ip_address == "":
            raise ValueError("No IP address provided")

        port = config.attributes.fields["port"].number_value
        # Per the Freenove code, 5001 is for sending/receiving instructions.
        # Port 8001 is used for video.
        if port == "":
            port = 5001
        return

    # Define a way to send commands to the robot dog server
    def send_data(self, data):
        try:
            self.client_socket.send(data.encode("utf-8"))
        except Exception as e:
            LOGGER.error(e)

    # Handles attribute reconfiguration
    def reconfigure(self,
                    config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]):
        # Here we initialize the resource instance
        ip_address = config.attributes.fields["ip_address"].string_value
        port = config.attributes.fields["port"].number_value
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip_address, port))
        return
```

### Define the custom base interface

To create a custom base model, you need a script that defines what each base component method (for example `set_power`) makes the robot dog do.

Open your newly created <file>robotdog.py</file> file.
It contains stubs of all the [base API methods](/dev/reference/apis/components/base/#api), but you need to modify these method definitions to actually send commands to the robot dog.

Take a look at [<file>robotdog.py</file>](https://github.com/viam-labs/robot-dog-module/blob/main/robotdog/src/robotdog.py).

It defines each method by specifying which corresponding commands to send to the Freenove dog server when the method is called.
For example, the `stop` method sends a command (`CMD_MOVE_STOP#8`) to the robot dog server to stop the dog from moving:

```python
async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
    self.is_stopped = True

    command = "CMD_MOVE_STOP#8\n"
    self.send_data(command)
```

Copy and paste that code into your <file>robotdog.py</file> file.
Feel free to tweak the specific contents of each of the [base method definitions](/dev/reference/apis/components/base/#api) to do things like make the dog move faster.
Don't forget to save.

### Make your module executable

Now that you defined the methods for the custom component, you need to set up an [executable file](https://en.wikipedia.org/wiki/Executable) to run your custom component module.
You can find more information in [Create a module](/operate/get-started/other-hardware/create-module/).
Since the command line tool already created a <file>run.sh</file> for you, all you need to do is make that shell script executable by running this command from your <file>robotdog</file> directory:

```sh {class="command-line" data-prompt="$"}
sudo chmod +x run.sh
```

## Configure the module on your robot

You need to tell your robot how to access the module you created.

Navigate to your machine's **CONFIGURE** tab.
Click the **+** (Create) button next to your main part in the left-hand menu and select **Local module**, then **Local module**.
Name your module `my-custom-base`.
Enter the path (for example, `/home/fido/robotdog/run.sh`) to your module's executable file in the **Executable path** field.
Click **Save** at the top right of the page to save your config.

![Config tab with the Modules subtab open, showing my-custom-base configured.](/tutorials/custom-base-dog/module-config.png)

## Configure the components

Now that the custom base code is set up, you need to configure all your hardware components.

### Configure the camera

Configure the ribbon camera on the dog as a `webcam` following our [webcam documentation](/operate/reference/components/camera/webcam/).

Click **Save**.

### Configure the base

Now, add the local base component from the local module.
Click the **+** (Create) button next to your main part in the left-hand menu and select **Local module**, then **Local component**.
Select `base` as the **Type**.
Name your component `quadruped`.
For the colon-delimited triplet, select or enter `viamlabs:base:robotdog`.

Then, in the configuration panel that appears for the local base, copy and paste the follow attributes:

```json
{
  "ip_address": "<HOSTNAME>.local",
  "port": 5001
}
```

Edit the `ip_address` attribute to match your machine's hostname, replacing `<HOSTNAME>` with your Pi's hostname (for example, `"ip_address": "robotdog.local"`).
If this doesn't work, you can instead try using the IP address of the machine where the module is running, for example, `"ip_address": "10.0.0.123"`.

If you are using a port other than `5001`, edit the `port` attribute.
`5001` is the default port for sending and receiving instructions to and from the Freenove server.

Click **Save**.

Your local component configuration should look similar to the following:

![CONFIGURE tab, showing the attributes editor of the `quadruped` local base component.](/tutorials/custom-base-dog/quadruped-config.png)

## Start the Freenove server

To operate the dog, you need to start the Freenove robot dog server (which you saved as <file>/home/fido/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code/Server/main.py</file>).
You can do this manually by SSHing into the Pi and running the following command from the <file>home/fido/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code/Server/</file> directory:

```sh {class="command-line" data-prompt="$"}
sudo python main.py -tn
```

Alternatively you can add this command to your module's `run.sh` file.
That way the Freenove robot dog server will start running when the module starts.

{{% alert title="Tip" color="tip" %}}

{{% /alert %}}

## Driving the robot with Viam

Navigate to the **CONTROL** tab.

Click the **quadruped** component panel to expand it and reveal the controls.

![Screenshot of the CONTROL tab with the custom base card expanded to reveal arrow control buttons.](/tutorials/custom-base-dog/control-tab.png)

1. Enable the camera stream from the **Select Cameras** dropdown.
2. Toggle the **Keyboard Disabled** switch to **Keyboard Enabled** to use the WASD keys on your keyboard.
3. Use the **W**, **A**, **S** and **D** buttons to make the robot walk forward, turn left, walk backward or turn right.

{{% alert title="Tip" color="tip" %}}

Depending on the speed of your server connection, you may need to hold down the base control button/key for a second or two before anything happens.

{{% /alert %}}

## Troubleshooting

- If your servos aren't moving as expected or at all, try turning the whole robot off for a while to let them cool down.

- Make sure the machine's batteries have adequate charge.
  If you have otherwise unexplained connection errors, try powering things off and charging the batteries for a while before attempting to SSH to the Pi again.

- If certain sensors or servos aren't being found by the software, turn off the robot and make sure all wires are fully connected before turning it back on.

- If you want to send commands directly to the dog server instead of running <file>robotdog.py</file> (which may be helpful for debugging specific commands, especially if you're adding your own functionality and need to calibrate servo speeds/positions) you can do the following:

  1. Install Netcat if it isn't already installed:

     ```sh {class="command-line" data-prompt="$"}
     sudo apt install netcat
     ```

  2. Connect directly to the robot dog by running the following command (replacing <DOG IP ADDRESS> with the correct IP address, for example `nc 10.0.0.123`) from the command line while SSHed into the Pi:

     ```sh {class="command-line" data-prompt="$"}
     nc <DOG IP ADDRESS> 5001
     ```

  3. You can now type commands ([list of available commands](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/blob/master/Code/Client/Command.py)) and hit enter to send them to the Freenove robot dog server.
     For example:

     ```sh {class="command-line" data-prompt="$"}
     CMD_TURN_LEFT#30
     CMD_STOP
     ```

## Next steps

In this tutorial you learned how to implement a custom component model and control it.
You learned about configuring modules and processes.
You drove the robot dog around using the Viam **CONTROL** tab.

To add more functionality, try using the generic `do_command` method to add different behaviors to your robot dog.
You could also use the Viam [vision service](/operate/reference/services/vision/) with the robot dog's [camera component](/operate/reference/components/camera/).
For example, you could write code to tell the robot dog to [move towards a colored target](/tutorials/services/color-detection-scuttle/) or to [follow a colored line](/tutorials/services/webcam-line-follower-robot/), similarly to how these tasks are done with wheeled bases in the tutorials linked here.
