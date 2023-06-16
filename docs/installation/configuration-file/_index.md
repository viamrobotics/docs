---
title: "Configuration File"
linkTitle: "Configuration File"
weight: 30
no_list: true
type: docs
draft: false
icon: "/installation/img/thumbnails/manage.png"
images: ["/installation/img/thumbnails/manage.png"]
description: "Building your robot configuration file for use with viam-server."
---

The `viam-server` binary uses a JSON-formatted configuration file to define all *resources* (hardware [components](/components/) and software [services](/services/)) it has access to, as well as any relevant parameters for those resources.

In order to start `viam-server` on a {{< glossary_tooltip term_id="board" text="board" >}} or computer, you must have a valid configuration file present on the local system.

For more information on the individual configuration options available, see [Configuration](/manage/configuration/).

## Configuration file location

By default, the configuration file is located at:

* Linux: <file>/etc/viam.json</file>
* macOS: <file>/opt/homebrew/etc/viam.json</file>

### Custom configuration file location

You can store your configuration file in a custom filesystem location as well.
Provide your custom path to the configuration file to the `viam-server` binary using the `-config` flag:

```sh {class="line-numbers linkable-line-numbers"}
viam-server -config /path/to/config-file.json
```

If you are using `systemctl` on Linux to manage `viam-server`, be sure to also update your service file with your custom path.
You'll need to update these lines in your <file>/etc/systemd/system/viam-server.service</file> file to reflect your custom path:

```sh {class="line-numbers linkable-line-numbers"}
...
ConditionPathExists=/path/to/config-file.json
...
ExecStart=/usr/local/bin/viam-server -config /path/to/config-file.json
...
```

## Build the configuration file in the Viam app

The easiest way to configure your robot and create the configuration file is from the Viam app.

1. Navigate to [the Viam app](https://app.viam.com) and select the **Config** tab.
1. Use **Builder** mode to add components and services, configure attributes, and map pin assignments.
1. Then, switch to **Raw JSON** mode to be shown the equivalent JSON configuration to the settings you made in **Builder** mode.
1. Download the JSON code to the board or computer you intend to run `viam-server` on; click the **See full config** link to be shown this file in plaintext for easy copying.

If you configure your robot in the **Config** tab before following the steps under the **Setup** tab to install `viam-server`, those steps will download and use the configuration file you've built.

If you later need to make changes to your robot's configuration:

1. Make your edits under the **Config** tab in **Builder** mode
1. Switch to **Raw JSON** mode to view your full configuration in JSON format
1. Download the code to your robot, overwriting your local configuration file with the new one.
1. Restart `viam-server` to apply the changes.

## Example JSON configuration file

If you want to create your own JSON configuration file without using [the Viam app](https://app.viam.com), you can start with the following example file.
This file contains some basic [component](/components/) and [service](/services/) configurations, as well as an example of a {{< glossary_tooltip term_id="process" text="process" >}}:

```json {class="line-numbers linkable-line-numbers"}
{
    "network": {
        "fqdn": "something-unique",
        "bind_address": ":8080"
    },
    "components": [
        {
            "name": "arm1",
            "type": "arm",
            "model": "fake",
            "attributes": {
                "arm-model": "xArm6"
            }
        },
        {
            "name": "audio_input1",
            "type": "audio_input",
            "model": "fake"
        },
        {
            "name": "base1",
            "type": "base",
            "model": "fake"
        },
        {
            "name": "board1",
            "type": "board",
            "model": "fake",
            "attributes": {
                "analogs": [
                    {
                        "name": "analog1",
                        "pin": "0"
                    }
                ],
                "digital_interrupts": [
                    {
                        "name": "di1",
                        "pin": "14"
                    }
                ]
            }
        },
        {
            "name": "camera1",
            "type": "camera",
            "model": "fake"
        },
        {
            "name": "encoder1",
            "type": "encoder",
            "model": "fake",
            "attributes": {
                "update_rate_msec": 200
            }
        },
        {
            "name": "gantry1",
            "type": "gantry",
            "model": "fake"
        },
        {
            "name": "generic1",
            "type": "generic",
            "model": "fake"
        },
        {
            "name": "gripper1",
            "type": "gripper",
            "model": "fake"
        },
        {
            "name": "input_controller1",
            "type": "input_controller",
            "model": "fake"
        },
        {
            "name": "motor1",
            "type": "motor",
            "model": "fake",
            "attributes": {
                "encoder": "encoder1",
                "pins": {
                    "a": "1",
                    "b": "2",
                    "pwm": "3"
                },
                "ticks_per_rotation": 100
            },
            "depends_on": [
                "board1",
                "encoder1"
            ]
        },
        {
            "name": "movement_sensor1",
            "type": "movement_sensor",
            "model": "fake"
        },

        {
            "name": "sensor1",
            "type": "sensor",
            "model": "fake"
        },
        {
            "name": "servo1",
            "type": "servo",
            "model": "fake"
        }
    ],
    "processes": [
        {
            "id": "1",
            "name": "echo",
            "args": [
                "hello",
                "world"
            ],
            "one_shot": true
        },
        {
            "id": "2",
            "name": "bash",
            "args": [
                "-c",
                "trap \"exit 0\" SIGINT; while true; do echo hey; sleep 2; done"
            ],
            "log": true
        }
    ],
    "services": [
        {
            "name": "navigation1",
            "type": "navigation",
            "attributes": {
                "store": {
                    "type": "memory"
                },
                "movement_sensor": "movement_sensor1",
                "base": "base1"
            }
        },
        {
            "name": "slam1",
            "type": "slam",
            "model": "fake"
        },
        {
            "name": "dm",
            "type": "data_manager",
            "model": "builtin"
        }
    ]
}
```

For more information on the individual configuration options available, see [Configuration](/manage/configuration/).
