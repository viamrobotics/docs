---
title: "Local Configuration File"
linkTitle: "Local Configuration File"
weight: 30
no_list: true
type: docs
draft: false
icon: "/installation/img/thumbnails/manage.png"
images: ["/installation/img/thumbnails/manage.png"]
description: "Building a local robot configuration file for use with viam-server."
---

The `viam-server` binary uses a JSON-formatted configuration file to define all resources (hardware [components](/components/) and software [services](/services/)) it has access to, as well as any relevant parameters for those resources.

When you [install `viam-server`](/installation/) from [the Viam app](https://app.viam.com), you can configure your robot directly in the app, and the app will automatically sync your configuration to your robot.

However, if your robot will never connect to the internet, you may wish to create your own local configuration file, using one of these options:

* [Build a local configuration file in the Viam app](#build-a-local-configuration-file-in-the-viam-app) - Use the Viam app to build the configuration file and download it to your robot, without connecting your robot to the Viam app.
* [Build a local configuration file manually](#build-a-local-configuration-file-manually) - Build your own local configuration file based on our example file.

For more information on the individual configuration options available, see [Configuration](/manage/configuration/).

## Build a local configuration file in the Viam app

If your robot will never connect to the internet, and you want to create a local configuration file manually, you can still use the Viam app to build the configuration file even without connecting your robot to it.
Follow the steps below to build and then download your configuration file:

1. Navigate to [the Viam app](https://app.viam.com) and select the **Config** tab.
1. Use **Builder** mode to add components and services, configure attributes, and map pin assignments.
1. Then, switch to **Raw JSON** mode to be shown the equivalent JSON configuration to the settings you made in **Builder** mode.
1. Download the JSON code to the board or computer you intend to run `viam-server` on; click the **See full config** link to be shown this file in plaintext for easy copying.

If you later need to make changes to your robot's configuration:

1. Make your edits under the **Config** tab in **Builder** mode
1. Switch to **Raw JSON** mode to view your full configuration in JSON format
1. Download the code to your robot, overwriting your local configuration file with the new one.
1. Restart `viam-server` to apply the changes.

{{% alert title="Note" color="note" %}}
This process is not required if your robot is connected to the Viam app.
When connected, any configuration changes you make in the app are propagated to your robot automatically.
If your robot temporarily disconnects from the internet, its configuration is cached locally, and any configuration changes you may have made in the app are propagated to your robot once it reconnects.
{{% /alert %}}

## Build a local configuration file manually

If your robot will never connect to the internet, you may create a local configuration file yourself without using the Viam app.
A locally-configured robot will not be able to access Viam's cloud features.

When you [install `viam-server`](/installation/), an example configuration file is provided at:

* Linux: <file>/etc/viam.json</file>
* macOS: <file>/opt/homebrew/etc/viam.json</file>

We recommend that you copy this example file to a custom configuration file location, such as your home directory.
Select the tab below for your platform:

{{< tabs name="Copy configuration file" >}}
{{% tab name="macOS" %}}

1. Copy the example configuration file to your home directory:

   ```sh {class="line-numbers linkable-line-numbers"}
   cp /opt/homebrew/etc/viam.json ~/viam.json
   ```

1. Start `viam-server`, providing the custom configuration file location using the `-config` flag:

   ```sh {class="line-numbers linkable-line-numbers"}
   viam-server -config ~/viam.json
   ```

{{% /tab %}}
{{% tab name="Linux" %}}

1. Copy the example configuration file to your home directory:

   ```sh {class="line-numbers linkable-line-numbers"}
   cp /etc/viam.json ~/viam.json
   ```

1. Start `viam-server`, providing the custom configuration file location using the `-config` flag:

   ```sh {class="line-numbers linkable-line-numbers"}
   viam-server -config ~/viam.json
   ```

1. If you are using `systemctl` to manage `viam-server`, you must also update your service file with this custom path.
   Update these lines in your <file>/etc/systemd/system/viam-server.service</file> file to reflect your custom path:

   ```sh {class="line-numbers linkable-line-numbers"}
   ...
   ConditionPathExists=~/viam.json
   ...
   ExecStart=/usr/local/bin/viam-server -config ~/viam.json
   ...
   ```

   Then, reload the service definition file:

   ```sh {class="line-numbers linkable-line-numbers"}
   sudo systemctl daemon-reload
   ```

   Finally, stop and restart `viam-server` to apply the changes:

   ```sh {class="line-numbers linkable-line-numbers"}
   systemctl stop viam-server
   systemctl start viam-server
   ```

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Note" color="note" %}}
This process is not required if your robot is connected to the Viam app.
When connected, any configuration changes you make in the app are propagated to your robot automatically.
If your robot temporarily disconnects from the internet, its configuration is cached locally, and any configuration changes you may have made in the app are propagated to your robot once it reconnects.
{{% /alert %}}

## Example JSON configuration file

If you want to create your own JSON configuration file without using [the Viam app](https://app.viam.com), you can start with the following example file.
This file contains some basic example [component](/components/) and [service](/services/) configurations, as well as an example of a {{< glossary_tooltip term_id="process" text="process" >}}:

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
