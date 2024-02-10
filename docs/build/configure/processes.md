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

## Configure a process

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).

Click on the **Processes** subtab and navigate to the **Create process** menu.

Give the process a **Name** (`id` in raw JSON) (an identifier of your choice) and click **Create process**.

Then fill in the following fields:

<!-- prettier-ignore -->
| Attribute (Builder Mode) | Attribute (Raw JSON) | Type    | Inclusion    | Description |
| ------------------------ | -------------------- | ------- | ------------ | ----------- |
| Executable               | `name`               | string  | **Required** | The command you want to execute when your machine connects to the server. |
| Arguments                | `args`               | string  | Optional     | Arguments to follow the command. |
| Working directory        | `cwd`                | string  | Optional     | Where you want the process to execute. Defaults to the directory where `viam-server` executes. |
| Logging                  | `log`                | boolean | Optional     | Toggle logging of errors and other messages on or off. Default: `false`. |
| Execute once             | `one_shot`           | boolean | Optional     | Toggle whether to execute the command just once or keep running the process indefinitely.<ul><li>If true, the process executes once at `viam-server` startup. Until the process completes, `viam-server` startup is blocked and the robot appears offline in the [Viam app](https://app.viam.com), so this should only be used for quick processes.</li><li>If false, the process continues to run. If the process crashes, it automatically restarts. It does not block `viam-server`. Default: `false`.</li></ul> |

### Example

The following example configuration executes the command `python3 my_cool_script.py` in your <file>/home/myName/project/</file> directory every time your machine boots, and keeps it executing indefinitely.

![The PROCESSES subtab of the CONFIG tab with a process called run-my-code configured. The executable is python3, the argument is my_cool_script.py, and the working directory is /home/myName/project. Logging is turned on and execute once is turned off.](/build/configure/process-fancy.png)

The corresponding raw JSON looks like this:

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
