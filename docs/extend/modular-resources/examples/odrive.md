---
title: "Add an ODrive motor as a Modular Resource"
linkTitle: "ODrive"
weight: 40
type: "docs"
description: "Configure an ODrive motor with serial or CANbus communication as a modular resource of your robot."
tags:
  [
    "motor",
    "odrive",
    "canbus",
    "serial",
    "module",
    "modular resources",
    "Python",
    "python SDK",
    "CAN",
  ]
# SMEs: Kim, Martha, Rand
---

The [Viam GitHub](https://github.com/viamrobotics/odrive) provides an implementation of ODrive Robotics' [ODrive S1](https://odriverobotics.com/shop/odrive-s1) motor driver as module defining two modular resources [extending](/extend/modular-resources/) the [motor API](/components/motor/#api) as new motor types.

[Install requirements](#requirements), [prepare](#prepare-your-odrive) your ODrive, and [configure](#configuration) the module to configure an `serial` or `canbus` [motor](/components/motor/) {{< glossary_tooltip term_id="resource" text="resource" >}} on your robot.

{{% alert title="Note" color="note" %}}

This module is only implemented for use with the [Viam Python SDK](https://python.viam.dev/).
The methods other SDKs provide for the [motor API](/components/motor/#api) will not work with this module.

{{% /alert %}}

## Requirements

On your robot's computer, clone the [Viam ODrive module](https://github.com/viamrobotics/odrive):

```{class="command-line" data-prompt="$"}
git clone https://github.com/viamrobotics/odrive.git
```

Install `python-can`, `cantools`, and the [Python `viam-sdk`](https://python.viam.dev/):

```{class="command-line" data-prompt="$"}
pip3 install python-can cantools viam-sdk
```

Follow [these instructions](https://docs.odriverobotics.com/v/latest/odrivetool.html) to install `odrivetool`.

Find and copy the path (either absolute, or relative to the working directory) to the executable module file `run.sh` on your robot's computer to provide when [configuring the module](#configuration).

{{% alert title="Tip" color="tip" %}}

Navigate to the `odrive/odrive-motor` directory of the ODrive module you cloned on a Terminal session with your computer and run `pwd` to obtain the path to `run.sh` on your robot's computer.

```{class="command-line" data-prompt="$"}
cd <your/path/to/odrive/odrive-motor>
pwd
```

{{% /alert %}}

### Prepare your ODrive

1. Read through the [ODrive documentation](https://docs.odriverobotics.com/v/latest/getting-started.html) to wire, calibrate, and configure your ODrive natively.

   {{% alert title="Tip" color="tip" %}}

This configuration remains on the same ODrive motor controller across reboots, and only changes when you go through the configuration of the ODrive again.

If you wish to set the native configuration dynamically, use `odrivetool` to find and copy the path to the motor's `config.json` file.
Provide this in configuration as the optional attribute `odrive_config_file`.
See [add an `odrive_config_file`](#add-an-odrive_config_file) for more information.

This option is not recommend for the `canbus` model.

    {{% /alert %}}

    Note that `iq_msg_rate_ms` in the `odrive_config_file` defaults to `0`, and you must set this to or around `100` to use the [motor API's `SetPower` method](https://docs.viam.com/components/motor/#setpower).

2. Follow [this guide](https://docs.odriverobotics.com/v/latest/control.html#control-doc) to tune your ODrive motor.

3. See the [ODrive CAN documentation](https://docs.odriverobotics.com/v/latest/can-guide.html) for detailed information on how to set up CAN on your ODrive.

   {{% alert title="Tip" color="tip" %}}

If you are using a Raspberry Pi as your [board](/components/board/), you must run `sudo ip link set can0 up type can bitrate <baud_rate>` in your terminal to receive CAN messages.
See "[Troubleshooting](#troubleshooting): [CAN Link Issues](https://github.com/viamrobotics/odrive#can-link-issues)" for more information.

Additionally, make sure you have [enabled SPI communication on your Pi](/installation/prepare/rpi-setup/) to use several common CANHats.

    {{% /alert %}}

4.  Make sure your ODrive is connected to your [board](/components/board/) as follows, depending on your preferred connection method:

        {{< tabs name="Connect your ODrive">}}

    {{% tab name="serial" %}}

Plug the [USB Isolator for Odrive](https://odriverobotics.com/shop/usb-c-to-usb-a-cable-and-usb-isolator) into a USB port on your board.
Plug a USB-C to USB-A cable from the isolator to the ODrive.

{{% /tab %}}
{{% tab name="canbus" %}}

Wire the CANH and CANL pins from your board to your ODrive.
Refer to your board and the [ODrive's pinout](https://docs.odriverobotics.com/v/latest/pinout.html) diagrams for the location of these pins.

You must make a serial connection to set up your ODrive.
If CAN chains together multiple ODrives, only one at a time must have this serial connection for reconfiguration
After setting up the ODrive, if you wish to use the `canbus` model, you can either leave the serial connection plugged in or remove it and leave only the CANH and CANL pins wired.

Note that if you want to only use the CAN pins, you cannot specify an `"odrive_config_file"` in your Viam configuration.
The ODrive would not be able to make the serial connection it needs to perform reconfiguration.

{{% /tab %}}
{{< /tabs >}}

    After preparing your ODrive, configure the module to configure `serial` or `canbus` model motors on your robot.

## Configuration

{{< tabs name="Connect your Odrive Module and Modular Resource">}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).

Click on the **Modules** subtab and navigate to the **Local** section.
Enter a name, for example `my_odrive_motor`, and the executable path, that points to the location where your ODrive module’s run script, <file>run.sh</file>, is stored on your robot’s computer.
Then click **Add module**.

![The ODrive module with the name 'odrive' and executable path '~/desktop/odrive/odrive-motor/run.sh' added to a robot in the Viam app config builder](/extend/modular-resources/add-odrive/add-odrive-module-ui.png)

Click on the **Components** subtab and click **Create component**.
Select the `local modular resource` type.
Then select `motor` as the type, enter the triplet `viam:odrive:serial`, and give your resource a name, for example `my_test_odrive`.
Click **Create**.

On the new component panel, copy and paste the following JSON object into the attributes field:

```json {class="line-numbers linkable-line-numbers"}
{
    "width_px": <int>,
    "height_px": <int>,
    "frame_rate": <int>,
    "debug": "<boolean>"
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

Navigate to the **Config** tab.
Select the **Raw JSON** mode.

To add the module, copy and paste the JSON object into the `"modules"` array:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "odrive",
  "executable_path": "<your/path/to/odrive/odrive-motor/run.sh>"
}
```

To add the modular resource from the module, copy and paste the JSON object into the `"components"` array:

{{< tabs name="Add an ODrive motor">}}
{{% tab name="serial" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "model": "viam:odrive:serial",
  "namespace": "rdk",
  "attributes": {},
  "depends_on": [],
  "type": "motor",
  "name": "<your-odrive-motor>"
}
```

{{% /tab %}}
{{% tab name="canbus" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "model": "viam:odrive:canbus",
    "namespace": "rdk",
    "attributes": {
      "canbus_node_id": <int>,
    },
    "depends_on": [],
    "type": "motor",
    "name": "<your-odrive-motor>"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "name": "odrive",
      "executable_path": "/path/to/odrive/odrive-motor/run.sh"
    }
  ],
  "components": [
    {
      "model": "viam:odrive:canbus",
      "namespace": "rdk",
      "attributes": {
        "canbus_node_id": 0,
        "odrive_config_file": "/path/to/first/config.json",
        "serial_number": "NUM0001"
      },
      "depends_on": [],
      "type": "motor",
      "name": "odrive-motor"
    },
    {
      "model": "viam:odrive:canbus",
      "namespace": "rdk",
      "attributes": {
        "canbus_node_id": 2,
        "odrive_config_file": "/path/to/second/config.json",
        "serial_number": "NUM0002"
      },
      "depends_on": [],
      "type": "motor",
      "name": "odrive-motor-2"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

Edit and fill in the attributes as applicable to your model of ODrive.

The following attributes are available for the motor resources available in the Viam ODrive module:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `canbus_node_id` | int | Optional | Required for successful initialization of the `"canbus"` type. <br> Node ID of the CAN node you would like to use. You configured this when [setting up your ODrive](https://docs.odriverobotics.com/v/latest/can-guide.html#setting-up-the-odrive). <br> Example: `0` |
| `odrive_config_file` | string | Optional | Filepath of a separate JSON file containing your ODrive's native configuration. See [add an `odrive_config_file`](#add-an-odrive_config_file) for instructions if you add this attribute. </br> See the [Odrive S1 Modular Component repository](https://github.com/viamrobotics/odrive/tree/main/sample-configs) for an example of this file. |
| `serial_number` | string | Optional | The serial number of the ODrive. Note that this is not necessary if you only have one ODrive connected. See "[Troubleshooting](#troubleshooting): [Hanging](https://github.com/viamrobotics/odrive#hanging)" for help finding this value. |
| `canbus_baud_rate` | string | Optional | [Baud rate](https://docs.odriverobotics.com/v/latest/can-guide.html#setting-up-the-odrive) of the ODrive CAN protocol. This attribute is only available for `"canbus"` connections. </br> Use [`odrivetool`](https://docs.odriverobotics.com/v/latest/odrivetool.html) to obtain this value with `<odrv>.can.config.baud_rate`. Format the string as a multiple of 1000 (k). <br> Example: `"250k"` |

Save the config.
Check the [**Logs** tab](/program/debug/) of your robot in the Viam app to make sure your ODrive motor has connected and no errors are being raised.

{{% alert title="Tip" color="tip" %}}

The `"canbus"` type allows you to connect multiple ODrives without providing a `serial_number` as long as you have not defined any `odrive_config_file` once the drive has been configured with `odrivetool`.

{{% /alert %}}

### Add an `odrive_config_file`

To add an `odrive_config_file` and reconfigure your ODrive natively each time the motor is initialized on the robot, use [`odrivetool`](https://docs.odriverobotics.com/v/latest/odrivetool.html) to extract your configuration from your ODrive:

1. Run `odrivetool backup-config config.json` to extract your configs to a file called `config.json`.
   See the [ODrive documentation](https://docs.odriverobotics.com/v/latest/odrivetool.html#configuration-backup) for more info.
2. `iq_msg_rate_ms` in the config defaults to `0`.
   You must set this to or around `100` to use the [motor API's `SetPower` method](https://docs.viam.com/components/motor/#setpower).
3. If you add an `odrive_config_file` to an `canbus` motor, you will have to leave the serial connection established with your ODrive plugged in to the USB port, in addition to wiring the CANH and CANL pins.

An alternative to adding an `odrive_config_file` is running the command `odrivetool restore-config /path/to/config.json` in your terminal.

## Troubleshooting

See the [Viam Github](https://github.com/viamrobotics/odrive#troubleshooting) for help with common issues.

{{< snippet "social.md" >}}
