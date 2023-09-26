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

You must authenticate yourself to the robot using the robot's location secret.
However, the app hides the robot location secret from the sample by default for your security.

To copy the robot location secret, select **Include Secret** on the **Code sample** tab of your robot's page on the [Viam app](https://app.viam.com).
Paste it into your environment variables or directly into your code.

You must also include the robot's remote address, like `12345.somerobot-main.viam.cloud`, as an external or public address to connect to your robot.
The code sample includes this address at default.
You can find it at the top of the robot's **Control** tab.

{{% snippet "secret-share.md" %}}

## Run Code Remotely

Most of the time, as long as both you and your robot are connected to the internet, you will want to run code to control your robot remotely.
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
go run ~/myCode/myViamFile.py
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

When connecting to a robot using the connection code from the [code sample tab](/program/#hello-world-the-code-sample-tab), a [client session](/program/apis/sessions/) automatically uses the [most efficient route](/program/connectivity/) to connect to your robot, which means the favored route for commands will be over localhost.
