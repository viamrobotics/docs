---
title: "Add an ODrive motor as a Modular Resource"
linkTitle: "ODrive"
weight: 40
type: "docs"
description: "How to add an ODrive motor with serial or CANbus communication as a modular resource of your robot."
tags: ["motor", "odrive", "canbus", "serial", "module", "modular resources", "Python", "python SDK", "CAN"]
# SMEs: Kim, Martha, Rand
---

The [Viam GitHub](https://github.com/viamrobotics/odrive) provides an implementation of ODrive Robotics' [ODrive S1](https://odriverobotics.com/shop/odrive-s1) motor driver as module defining two modular resources [extending](/extend/modular-resources/) the [motor API](/components/motor/#api) as new motor types.

[Prepare](#prepare-your-odrive) your ODrive and [download](#requirements) and [configure](#configuration) the module to add an `odrive-serial` or `odrive-canbus` [motor](/components/motor/) {{< glossary_tooltip term_id="resource" text="resource" >}} to your robot.

{{% alert title="Note" color="note" %}}

This module is only implemented for use with the [Viam Python SDK](https://python.viam.dev/).
The methods other SDKs provide for the [motor API](/components/motor/#api) will not work with this module.

{{% /alert %}}

### Prepare your ODrive

1. Read through the [ODrive documentation](https://docs.odriverobotics.com/v/latest/getting-started.html) to wire, calibrate, and configure your ODrive natively.

{{% alert title="Tip" color="tip" %}}

This configuration remains on the same ODrive motor controller across reboots, and only changes when you go through the configuration of the ODrive again.

If you wish to set the native configuration dynamically, use `odrivetool` to find and copy the path to the motor's `config.json` file.
Provide this in configuration as the optional attribute `"odrive_config_file"`.
See the [Odrive S1 Modular Component repository](https://github.com/viamrobotics/odrive/tree/main/sample-configs) for an example of this file.

This option is not recommend for the `odrive-canbus` model.

{{% /alert %}}

2. Follow [this guide](https://docs.odriverobotics.com/v/latest/control.html#control-doc) to tune your ODrive motor.

3. See the [ODrive CAN documentation](https://docs.odriverobotics.com/v/latest/can-guide.html) for detailed information on how to set up CAN on your ODrive.

{{% alert title="Tip" color="tip" %}}

If you are using a Raspberry Pi as your [board](/components/board/), you must run `sudo ip link set can0 up type can bitrate <baud_rate>` in your terminal to receive CAN messages.
See [Troubleshooting](#can-link-issues) for more information.

Additionally, make sure you have [enabled SPI communication on your Pi](/installation/prepare/rpi-setup/) to use several common CANHats.

{{% /alert %}}

4. Make sure your ODrive is connected to your [board](/components/board/) as follows, depending on your preferred connection method:

{{< tabs name="Connect your ODrive">}}
{{% tab name="odrive-serial" %}}

Plug the [USB Isolator for Odrive](https://odriverobotics.com/shop/usb-c-to-usb-a-cable-and-usb-isolator) into a USB port on your board.
Plug a USB-C to USB-A cable from the isolator to the ODrive.

{{% /tab %}}
{{% tab name="odrive-canbus" %}}

Wire the CANH and CANL pins from your board to your ODrive.
Refer to your board and the [ODrive's pinout](https://docs.odriverobotics.com/v/latest/pinout.html) diagrams for the location of these pins.

You must make a serial connection to set up your ODrive.
After setting up the ODrive, if you wish to use the `odrive-canbus` model, you can either leave the serial connection plugged in or remove it and leave only the CANH and CANL pins wired.

Note that if you want to only use the CAN pins, you cannot specify an `"odrive_config_file"` in your Viam configuration.
The ODrive would not be able to make the serial connection it needs to perform reconfiguration.

{{% /tab %}}
{{< /tabs >}}

After preparing your ODrive, download and configure the module to configure `odrive-serial` or `odrive-canbus` model motors on your robot.

## Requirements

On your robot's computer, clone the [Viam ODrive module](https://github.com/viamrobotics/odrive):

``` {id="terminal-prompt" class="command-line" data-prompt="$"}
git clone https://github.com/viamrobotics/odrive.git
```

Install `python-can`, `cantools`, and the [Python `viam-sdk`](https://python.viam.dev/):

``` {id="terminal-prompt" class="command-line" data-prompt="$"}
pip3 install python-can cantools viam-sdk
```

Follow [these instructions](https://docs.odriverobotics.com/v/latest/odrivetool.html) to install `odrivetool`.

Find and copy the path (either absolute, or relative to the working directory) to the executable module file `run.sh` on your robot's computer to provide in configuration.

{{% alert title="Tip" color="tip" %}}

Navigate to the `odrive/odrive-motor` directory of the ODrive module you cloned on a Terminal session with your computer and run `pwd` to obtain the path to `run.sh` on your robot's computer.

``` {id="terminal-prompt" class="command-line" data-prompt="$"}
cd <your/path/to/odrive/odrive-motor>
pwd
```

{{% /alert %}}

## Configuration

### Module

{{< tabs name="Add the ODrive module">}}
{{% tab name="Config Builder" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page, and click on the **Modules** subtab.

Add the ODrive module with a name of your choice and an `"executable_path"` that points to the location where your ODrive module’s run script, <file>run.sh</file>, is stored on your robot’s computer.

![The ODrive module with the name "odrive" and executable path "~/desktop/odrive/odrive-motor/run.sh" added to a robot in the Viam app config builder](../../img/add-odrive/add-odrive-module-ui.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
"modules": [
  {
    "name": "odrive",
    "executable_path": "<your/path/to/odrive/odrive-motor/run.sh>"
  }
]
```

{{% /tab %}}
{{< /tabs >}}

### Modular Resource

<!-- TODO sg: Unsure if this is supported in module registry stat

name="Config Builder" 

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page, and click on the **Components** subtab.

Add a new component with a **Name** of your choice and the **Type** `motor`.

In **Model**, enter either `viam:motor:odrive-serial` or `viam:motor:odrive-canbus`, depending on your preferred connection method.
A warning tooltip will appear explaining this model is not built-in to the RDK, so it is not recognized by Viam and won't have validation features.

![The ODrive motor component in the serial model being added as a component with name "your-odrive-serial" in the Viam app config builder](../../img/add-odrive/add-odrive-resource-ui.png)

Click **Create component**.
Edit and fill in the attributes as applicable to your model of ODrive.

![The ODrive motor component in the serial model with example configuration attributes pasted in the Viam app config builder](../../img/add-odrive/add-odrive-attributes-ui.png)

tab -->

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page, and click on the **Components** subtab.
Select **Raw JSON** mode.

Copy and paste the following JSON along with your module JSON depending on your preferred communication type:

{{< tabs name="Add an ODrive motor">}}
{{% tab name="odrive-serial" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  // "modules": [ {"name": "odrive" ...  } ] MODULE JSON
  "components": [
    {
      "model": "viam:motor:odrive-serial",
      "namespace": "rdk",
      "attributes": {
      },
      "depends_on": [],
      "type": "motor",
      "name": "<your-odrive-motor>"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="odrive-canbus" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  // "modules": [ {"name": "odrive" ...  } ]
  "components": [
    {
      "model": "viam:motor:odrive-canbus",
      "namespace": "rdk",
      "attributes": {
        "canbus_node_id": <int>,
      },
      "depends_on": [],
      "type": "motor",
      "name": "<your-odrive-motor>"
    }
  ]
}
```

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
      "model": "viam:motor:odrive-canbus",
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
      "model": "viam:motor:odrive-canbus",
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

Edit and fill in the attributes as applicable to your model of ODrive.

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for the motor resources available in the Viam ODrive module:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `canbus_node_id` | int | Optional | Required for successful initialization of the `"odrive-canbus"` type. <br> Node ID of the CAN node you would like to use. You configured this when [setting up your ODrive](https://docs.odriverobotics.com/v/latest/can-guide.html#setting-up-the-odrive). <br> Example: `0` |
| `odrive_config_file` | string | Optional | Filepath of a separate JSON file containing your ODrive's native configuration. </br> See the [Odrive S1 Modular Component repository](https://github.com/viamrobotics/odrive/tree/main/sample-configs) for an example of this file. |
| `serial_number` | string | Optional | The serial number of the ODrive. Note that this is not necessary if you only have one ODrive connected. See [Troubleshooting](#hanging) for help finding this value. |
| `canbus_baud_rate` | string | Optional | [Baud rate](https://docs.odriverobotics.com/v/latest/can-guide.html#setting-up-the-odrive) of the ODrive CAN protocol. This attribute is only available for `"odrive-canbus"` connections. </br> Use [`odrivetool`](https://docs.odriverobotics.com/v/latest/odrivetool.html) to obtain this value with `<odrv>.can.config.baud_rate`. Format the string as a multiple of 1000 (k). <br> Example: `"250k"` |

Save the config.
Check the [**Logs** tab](/program/debug/) of your robot in the Viam app to make sure your ODrive motor has connected and no errors are being raised.

{{% alert title="Tip" color="tip" %}}

The `"odrive-canbus"` type allows you to connect multiple ODrives without providing a `serial_number` as long as you have not defined any `odrive_config_file`.

{{% /alert %}}

## Troubleshooting

### Unstable Behavior

- The motor is likely not properly tuned.
See the [ODrive documentation](https://docs.odriverobotics.com/v/latest/control.html) for instructions on how to tune.

### Hanging

- If you have provided a serial number, make sure it is the correct serial number.
ODrives have 2 serial numbers: one that will be printed out when you start `odrivetool`, and one that can be accessed in `odrivetool` by running `odrv0.serial_number`.
The correct serial number is the one that is printed out when you start `odrivetool`.
- If you have not provided a serial number or you are sure you have provided the correct serial number, you are likely connected to the ODrive elsewhere.
Make sure any connections via Python, `odrivetool` or the GUI are closed.

### CAN Link Issues

- If you get an error of `"Device or resource busy"`, try setting CAN down and back up with the command `sudo ip link set can0 down`, followed by `sudo ip link set can0 up type can bitrate <baud_rate>`.
  - You have to do this any time you want to change the baud rate.
- If you get an error of `"Network is down"`, try setting CAN up with the command `sudo ip link set can0 up type can bitrate <baud_rate>`.

{{< snippet "social.md" >}}
