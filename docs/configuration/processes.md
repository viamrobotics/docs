---
title: "Processes"
linkTitle: "Processes"
weight: 35
type: "docs"
no_list: true
description: "Processes automatically run specified scripts when the robot boots."
tags: ["manage", "processes"]
---

To automatically run a specified script when the robot boots, configure a *process*.

Start by giving the process a **Name** (`id` in raw JSON) (an identifier of your choice) and clicking **Create Process**.

Then fill in the following fields:

- **Executable** (`name`): The command you want to execute when your robot connects to the server.
- **Arguments** (`args`): Optional arguments to follow the command.
- **Working Directory** (`cwd`): Where you want the process to execute.
  An optional setting that defaults to the directory where `viam-server` executes.

You can also toggle whether you want errors and other messages to be logged, and whether to execute the command just once or keep running the process indefinitely.
In raw JSON, these options are represented by `log` (bool) and `one_shot` (bool), respectively.

{{% expand "Click to see an example of a configured process." %}}

The following configuration executes the command `python3 my_cool_script.py` in your <file>/home/myName/project/</file> directory every time your robot boots, and keeps it executing indefinitely.

![The PROCESSES sub-tab of the CONFIG tab with a process called run-my-code configured. The executable is python3, the argument is my_cool_script.py, and the working directory is /home/myName/project. Logging is turned on and execute once is turned off.](../img/configuration/process-fancy.png)

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

{{% /expand %}}
