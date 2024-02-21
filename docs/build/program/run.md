---
title: "Run SDK Code"
linkTitle: "Run Code"
weight: 50
type: "docs"
description: "Execute the logic you've written to control your machine or fleet."
images: ["/services/icons/sdk.svg"]
tags: ["client", "sdk", "application", "sdk", "fleet", "program"]
aliases:
  - /program/run/
---

After saving your [code sample](/build/program/#hello-world-the-code-sample-tab) and adding control logic with [Viam's SDKs](/build/program/apis/), run your program to control your Viam-connected machine.

### Authentication

{{< readfile "/static/include/program/authenticate.md" >}}

## Run code remotely

You can remotely control your machine from anywhere in the world.
If your machine and your personal computer are both connected to the Internet, you can run code to control your machine remotely from your personal computer.

{{<imgproc src="/build/program/remotely.png" resize="800x" declaredimensions=true alt="A client connecting remotely to a machine">}}

This method is convenient for most use cases because your machine and your personal computer do not have to be connected to the same WAN/LAN to issue control commands.
When you run code on one computer, creating a client [session](/build/program/apis/sessions/), the code running on that computer sends instructions to your machine's `viam-server` instance over the Internet.

After editing your code to include your machine's [authentication credentials](#authentication), run a command to execute the program in the terminal of a computer with the appropriate programming language and [Viam SDK](/sdks/) installed:

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

As long as that computer is able to establish a network connection with the machine's computer, your control logic will be executed on the machine.

If the internet becomes unavailable to the machine or to your computer but a local network is available, your code will continue to run as described in the next section:

## Run code on local network

Your machines do not need to be connected to the Internet for you to be able to run code.
As long as your machine is connected to the same LAN or WAN network as the device running the code, you can connect to it and run code.

When you use the connection code from the [code sample tab](/build/program/#hello-world-the-code-sample-tab), that code establishes a [client session](/build/program/apis/sessions/) that automatically uses the [most efficient route](/build/program/connectivity/) to send commands to your machine.
That means that when the device your code runs on is on the same network as your machine, even if internet is available, the connection will choose the most efficient route and connect over LAN or WAN.
If you subsequently lose internet connectivity, but stay connected to LAN or WAN, the connection will thus remain.

## Run code on-machine

You can run SDK code directly on your machine.
If you run [PID control loops](https://en.wikipedia.org/wiki/PID_controller) or your machines have intermittent or no network connectivity, you can ensure lags in communication do not interfere with the machine's performance by running the control code on the same board that is running `viam-server`.
Running everything on one machine is also convenient if you have a machine (for example, an air quality sensor) that runs all the time, and you don't want to have to connect to it from a separate computer constantly.

{{<imgproc src="/build/program/on-robot.png" resize="800x" declaredimensions=true alt="A client running on a machine">}}

The script you run on-machine is the same as the script you [run remotely](#run-code-remotely) or on a local network.
When the connection code from the [code sample tab](/build/program/#hello-world-the-code-sample-tab) executes, it creates a [client session](/build/program/apis/sessions/) connected to your machine using the [most efficient route](/build/program/connectivity/).
Because the code is running on the same machine as `viam-server`, the favored route for commands is automatically over localhost.

Install the appropriate programming language and [Viam SDK](/sdks/) on your machine and run a command to execute the program in the terminal of that machine instead of from a separate computer:

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

### Run code automatically as a process

If you want to run your code on-machine automatically when your machine boots, you can configure your machine to run your code as a _{{< glossary_tooltip term_id="process" text="process" >}}_.
You can configure the process to run once on boot, or continuously.

Find information on how to configure a process in [Processes](/build/configure/processes/).
