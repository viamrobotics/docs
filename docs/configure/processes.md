---
title: "Configure a managed process"
linkTitle: "Managed Processes"
weight: 50
type: "docs"
description: "Configure a process to run a program when your machine is online."
tags: ["processes"]
aliases:
  - /build/configure/processes/
date: "2022-01-01"
updated: "2024-11-01"
---

To run a program or control code when your machine is online, configure a _{{< glossary_tooltip term_id="process" text="process" >}}_.
The process is managed by `viam-server`.
You can configure processes to run once upon startup or indefinitely.

{{< alert title="In this page" color="note" >}}
{{% toc %}}
{{< /alert >}}

## Configure a process

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Process**.

In the process configuration panel, configure the attributes for your process:

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------- |
| Executable (`name`) | string  | **Required** | The command you want to execute when your machine connects to the server. On many operating systems, you can find the executable path of commands by running `which <command-name>`. |
| Arguments (`args`) | string[]  | Optional | Arguments to follow the command. |
| Working directory (`cwd`) | string  | Optional | Where you want the process to execute. Defaults to the directory where `viam-server` executes. |
| `username` (not available in builder mode) | string | Optional | Example: `"username": "ubuntu"`. |
| `env` (not available in builder mode) | Map<string, string> | Optional | Environment variables for the process. Example: `"environment": { "SVC_API_KEY":"VALUE" }`. |
| Logging (`log`) | boolean | Optional | Toggle logging of errors and other messages on or off. <br>Default: `false`. |
| Execute once (`one_shot`) | boolean | Optional     | Toggle whether to execute the command just once or keep running the process indefinitely.<ul><li>If `true`, the process executes once at `viam-server` startup. Until the process completes, `viam-server` startup is blocked and the machine appears offline in the [Viam app](https://app.viam.com). This machine should only be used for quick processes.</li><li>If `false`, the process continues to run and is restarted if the process crashes or is killed. The process does not block `viam-server`.</li></ul> Default: `false`. |

Click **Save** in the upper right corner of the screen.

### Example

The following example executes the command `python3 my_cool_script.py` in your <file>/home/myName/project/</file> directory every time a machine boots, and restarts the process if it stops running.

{{< tabs >}}
{{% tab name="Builder mode" %}}

![The CONFIGURE tab with a process called run-my-code configured. The executable is python3, the argument is my_cool_script.py, and the working directory is /home/myName/project. Logging is turned on and execute once is turned off.](/build/configure/process-fancy.png)

{{% /tab %}}
{{% tab name="JSON" %}}

```json
"processes": [
    {
      "id": "run-my-code",
      "log": true,
      "name": "python3",
      "args": [
        "my_cool_script.py"
      ],
      "cwd": "/home/myName/project/"
    }
  ]
```

{{% /tab %}}
{{< /tabs >}}

## Set up dependencies

If you are configuring a process that requires dependencies, such as the Viam SDKs, you must install those dependencies so `viam-server` has access to them.

For Python scripts, we recommend you install dependencies into the folder that contains the code you want to execute:

```sh {class="command-line" data-prompt="$"}
sudo apt install -y python3-pip
pip3 install --target=machine viam-sdk <other-required-dependencies>
```
