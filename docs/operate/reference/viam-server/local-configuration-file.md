---
title: "Local Configuration File"
linkTitle: "Local Configuration File"
weight: 200
no_list: true
type: docs
icon: true
images: ["/installation/thumbnails/manage.png"]
description: "Building a local machine configuration file for use with viam-server."
date: "2022-01-01"
aliases:
  - /internals/local-configuration-file/
# updated: ""  # When the content was last entirely checked
---

The `viam-server` binary uses a JSON-formatted configuration file to define all {{< glossary_tooltip term_id="resource" text="resources" >}} it has access to, as well as any relevant parameters for those resources.

When you [install `viam-server`](/operate/get-started/setup/) from the [Viam app](https://app.viam.com), you configure your machine directly in the app, and the app will automatically sync your configuration to your machine.

However, if your machine will never connect to the internet, you will need to create your own local configuration file, using one of these options:

- [Build a local configuration file in the Viam app](#build-a-local-configuration-file-in-the-viam-app) - Use the Viam app to build the configuration file and copy it to your machine, without connecting your machine to the Viam app.
- [Build a local configuration file manually](#build-a-local-configuration-file-manually) - Build your own local configuration file based on the example file.

## Build a local configuration file in the Viam app

If your machine will never connect to the internet, and you want to create a local configuration file manually, you can still use the Viam app to build the configuration file even without connecting your machine to it.
Follow the steps below to build and then download your configuration file:

1. Navigate to the [Viam app](https://app.viam.com) and select the **CONFIGURE** tab.
1. Use **Builder** mode to add components and services, configure attributes, and map pin assignments.
1. Then, switch to **JSON** mode to be shown the equivalent JSON configuration to the settings you made in **Builder** mode.
1. Download the JSON configuration to the board or computer you intend to run `viam-server` on.
   In **Builder** mode, you can click the **...** menu to the right of your main part's name in the left-hand panel and click the **View debug configuration** option to view the full configuration file in plaintext for easy copying.

If you later need to make changes to your machine's configuration:

1. Make your edits under the **CONFIGURE** tab in **Builder** mode
1. Select the **View debug configuration** option from the **...** menu to the right of your main part's name in the left-hand panel to view your full configuration in JSON format.
1. Download the code to your machine, overwriting your local configuration file with the new one.
   If it is currently running, `viam-server` will detect the updated configuration and apply it automatically -- there is no need to restart `viam-server` to apply changes.

{{% alert title="Note" color="note" %}}
This process is not required if your machine is connected to the Viam app.
When connected, any configuration changes you make in the app are propagated to your machine automatically.
If your machine temporarily disconnects from the internet, its configuration is cached locally, and any configuration changes you may have made in the app are propagated to your machine once it reconnects.
{{% /alert %}}

## Build a local configuration file manually

If your machine will never connect to the internet, you can create a local configuration file yourself without using the Viam app.
A locally-configured machine will not be able to access Viam's cloud features.
For most users, we recommend [using the Viam app to create the configuration file](#build-a-local-configuration-file-in-the-viam-app) as it is less error-prone.

If you followed the instructions to [install `viam-server`](/operate/get-started/setup/), the installation process provides an example configuration file in the following location:

- Linux: <file>/etc/viam.json</file>
- macOS: <file>/opt/homebrew/etc/viam.json</file>

You can also use the [example configuration file](#example-json-configuration-file) below to base your machine's configuration on.

{{% alert title="Note" color="note" %}}
This process is not required if your machine is connected to the Viam app.
When connected, any configuration changes you make in the app are propagated to your machine automatically.
If your machine temporarily disconnects from the internet, its configuration is cached locally, and any configuration changes you may have made in the app are propagated to your machine once it reconnects.
{{% /alert %}}

## Example JSON configuration file

If you want to create your own JSON configuration file without using the [Viam app](https://app.viam.com), you can start with the following example file.
The following file contains some example {{< glossary_tooltip term_id="component" text="component" >}} and {{< glossary_tooltip term_id="service" text="service" >}} configurations:

```json {class="line-numbers linkable-line-numbers"}
{
  "network": {
    "fqdn": "something-unique",
    "bind_address": ":8080"
  },
  "components": [
    {
      "name": "arm1",
      "model": "fake",
      "api": "rdk:component:arm",
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
      "api": "rdk:component:base",
      "model": "fake"
    },
    {
      "name": "board1",
      "model": "fake",
      "api": "rdk:component:board",
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
      "api": "rdk:component:camera",
      "model": "fake"
    },
    {
      "name": "encoder1",
      "model": "fake",
      "api": "rdk:component:encoder",
      "attributes": {
        "update_rate_msec": 200
      }
    },
    {
      "name": "gantry1",
      "api": "rdk:component:gantry",
      "model": "fake"
    },
    {
      "name": "generic1",
      "api": "rdk:component:generic",
      "model": "fake"
    },
    {
      "name": "gripper1",
      "api": "rdk:component:gripper",
      "model": "fake"
    },
    {
      "name": "input_controller1",
      "api": "rdk:component:input_controller",
      "model": "fake"
    },
    {
      "name": "motor1",
      "model": "fake",
      "api": "rdk:component:motor",
      "attributes": {
        "encoder": "encoder1",
        "pins": {
          "a": "1",
          "b": "2",
          "pwm": "3"
        },
        "ticks_per_rotation": 100
      },
      "depends_on": ["board1", "encoder1"]
    },
    {
      "name": "movement_sensor1",
      "api": "rdk:component:movement_sensor",
      "model": "fake"
    },

    {
      "name": "sensor1",
      "api": "rdk:component:sensor",
      "model": "fake"
    },
    {
      "name": "servo1",
      "api": "rdk:component:servo",
      "model": "fake"
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
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin"
    }
  ]
}
```
