---
title: "Run SDK Code"
linkTitle: "Run Code"
weight: 50
type: "docs"
description: "Execute the logic you've written to control your robot or fleet."
images: ["/services/icons/sdk.svg"]
tags: ["client", "sdk", "application", "sdk", "fleet", "program"]
---

After saving your [code sample](/program/#hello-world-the-code-sample-tab) and adding control logic with [Viam's SDKs](/program/apis/), run your program to control your Viam-connected robot.

### Authentication

{{< readfile "/static/include/program/authenticate.md" >}}

## Run Code Remotely

Most of the time, as long as both you and your robot are connected to the internet, you will want to run code to control your robot remotely.

{{<imgproc src="/program/remotely.png" resize="800x" declaredimensions=true alt="A client connecting remotely to a robot">}}

The advantage of this method is that your robot and your computer do not have to be connected to the same WAN/LAN to issue control commands.
You can remotely control your robot with any application you implement from anywhere in the world.
For example, you can run code on your personal computer, creating a client [session](/program/apis/sessions/), where the code running on that computer sends instructions to your robot's `viam-server` instance over the internet.

After editing your code to include your robot's [authentication credentials](#authentication), run a command to execute the program in the terminal of a machine with the appropriate programming language and Viam SDK installed:

{{< tabs >}}
{{% tab name="Python" %}}

```sh {class="command-line" data-prompt="$"}
python3 ~/myCode/myViamFile.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {class="command-line" data-prompt="$"}
go run ~/myCode/myViamFile.go
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

For an example, see [this execution demo.](https://github.com/viamrobotics/viam-typescript-sdk/tree/main/examples/vanilla)

{{% /tab %}}
{{% tab name="C++" %}}

For information on running C++ code see [the instructions on GitHub](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

{{% /tab %}}
{{% tab name="Flutter" %}}

```sh {class="command-line" data-prompt="$"}
flutter run <DART_FILE>
```

{{% /tab %}}
{{< /tabs >}}

This is useful because as long as that computer is able to establish a network connection with the robot's computer, your control logic will be executed on the robot.

## Run Code On-Robot

In case you run [PID control loops](https://en.wikipedia.org/wiki/PID_controller) or your robots have intermittent network connectivity, you can ensure this does not interfere with the code's execution, by running the control code on the same board that is running `viam-server`.

{{<imgproc src="/program/on-robot.png" resize="800x" declaredimensions=true alt="A client running on a robot">}}

When connecting to a robot using the connection code from the [code sample tab](/program/#hello-world-the-code-sample-tab), a [client session](/program/apis/sessions/) automatically uses the [most efficient route](/program/connectivity/) to connect to your robot, which means the favored route for commands will be over localhost.

## Run code automatically

If you want to run your code automatically when your robot boots, you can configure Viam to run your code as a [process](/manage/configuration/#processes).

To be able to run your code from your board, you need to install the relevant SDK as well as other required dependencies:

{{< tabs >}}
{{% tab name="Python" %}}

1. [`ssh` into your board](/installation/prepare/rpi-setup/#connect-with-ssh) and install `pip`:

   ```sh {class="command-line" data-prompt="$"}
   sudo apt install python3-pip
   ```

2. Create a folder `robot` inside your home directory:

   ```sh {class="command-line" data-prompt="$"}
   mkdir robot
   ```

3. Then install the Viam Python SDK (and other dependencies if required) **into that folder**:

   ```sh {class="command-line" data-prompt="$"}
   pip3 install --target=robot viam-sdk <other-required-dependencies>
   ```

4. Add your code to your new folder:

   ```sh {class="command-line" data-prompt="$"}
   scp main.py user@host.local:/home/myboard/robot/main.py
   ```

{{% /tab %}}
{{< /tabs >}}

Now navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Processes** subtab and navigate to the **Create process** menu.

Enter `main` as the process name and click **Create process**.

{{< tabs >}}
{{% tab name="Python" %}}

In the new process panel, enter `python3` as the executable, `main.py` as the argument, and the working directory of your board Pi as `/home/myboard/robot`.
Click on **Add argument**.

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

Now your robot will start its code automatically once booted.
