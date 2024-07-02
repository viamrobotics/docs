---
title: "Configure a Process to Run on Your Machine"
linkTitle: "Automatic Processes"
weight: 50
type: "docs"
description: "Configure a process to automatically run a command such as a script automatically when your machine boots."
tags: ["processes"]
---

To automatically run a specified command when your machine boots, configure a _{{< glossary_tooltip term_id="process" text="process" >}}_.
A process can be any command, for example one that executes a binary or a script.
You can configure a process to run once when the machine first starts, or to run continuously alongside `viam-server`.

## Set up dependencies for Viam SDK code run as a process

If you are configuring a process to run a script that does not use Viam SDKs, skip this section and continue to [Configure a process](#configure-a-process).
Due to the way processes are designed for stability, if you are configuring a process to run a [Viam SDK](/sdks/) script, you need to install the relevant SDK as well as other required dependencies in a specific way on your SBC:

{{< tabs >}}
{{% tab name="Python" %}}

1. [`ssh` into your board](/get-started/prepare/rpi-setup/#connect-with-ssh) and install `pip`:

   ```sh {class="command-line" data-prompt="$"}
   sudo apt install python3-pip
   ```

2. Create a folder inside your home directory to hold your code.
   These example steps use the folder name `robot`:

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

## Configure a process

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine {{< glossary_tooltip term_id="part" text="part" >}} in the left-hand menu and select **Process**.
Your process is automatically created with a name (`id` in JSON) like **process-1** and a card matching that name on the **CONFIGURE** tab.
Navigate to that card.

Then fill in the following fields:

<!-- prettier-ignore -->
| Attribute (Builder Mode) | Attribute (JSON) | Type    | Required? | Description |
| ------------------------ | ---------------- | ------- | --------- | ----------- |
| Executable               | `name`               | string  | **Required** | The command you want to execute when your machine connects to the server. |
| Arguments                | `args`               | string  | Optional     | Arguments to follow the command. |
| Working directory        | `cwd`                | string  | Optional     | Where you want the process to execute. Defaults to the directory where `viam-server` executes. |
| Logging                  | `log`                | boolean | Optional     | Toggle logging of errors and other messages on or off. Default: `false`. |
| Execute once             | `one_shot`           | boolean | Optional     | Toggle whether to execute the command just once or keep running the process indefinitely.<ul><li>If true, the process executes once at `viam-server` startup. Until the process completes, `viam-server` startup is blocked and the robot appears offline in the [Viam app](https://app.viam.com), so this should only be used for quick processes.</li><li>If false, the process continues to run. If the process crashes, it automatically restarts. It does not block `viam-server`. Default: `false`.</li></ul> |

Click **Save** in the upper right corner of the screen to save your config.

### Example

The following example configuration executes the command `python3 my_cool_script.py` in your <file>/home/myName/project/</file> directory every time your machine boots, and keeps it executing indefinitely.

![The CONFIGURE tab with a process called run-my-code configured. The executable is python3, the argument is my_cool_script.py, and the working directory is /home/myName/project. Logging is turned on and execute once is turned off.](/build/configure/process-fancy.png)

The corresponding JSON looks like this:

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
