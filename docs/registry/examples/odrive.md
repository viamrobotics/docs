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
aliases:
  - "/extend/modular-resources/examples/odrive/"
  - "/modular-resources/examples/odrive/"
# SMEs: Kim, Martha, Rand
---

Viam provides an `odrive` {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} which adds support for ODrive Robotics' [ODrive S1](https://odriverobotics.com/shop/odrive-s1) and [ODrive Pro](https://odriverobotics.com/shop/odrive-pro) motor drivers, extending the Viam [motor API](/components/motor/#api).
The `odrive` {{< glossary_tooltip term_id="module" text="module" >}} supports an ODrive motor driver connected in either `serial` or `canbus` mode.

The `odrive` module is available [from the Viam registry](https://app.viam.com/module/viam/odrive).
See [Modular resources](/registry/#the-viam-registry) for instructions on using a module from the Viam registry on your robot.

The source code for this module is available on the [`odrive` GitHub repository](https://github.com/viamrobotics/odrive).

## Requirements

If you haven't already, [install `viam-server`](/get-started/installation/) on your robot.

Your robot must have an ODrive S1 or ODrive Pro motor controller installed to be able to use the `odrive` module.

### Prepare your ODrive

1. Follow [these instructions](https://docs.odriverobotics.com/v/latest/odrivetool.html) to install `odrivetool` on your robot.

1. Read through the [ODrive documentation](https://docs.odriverobotics.com/v/latest/getting-started.html) to wire, calibrate, and configure your ODrive natively.

   {{% alert title="Tip" color="tip" %}}

   This configuration remains on the same ODrive motor controller across reboots, and only changes when you go through the configuration of the ODrive again.

   If you wish to set the native configuration dynamically, use `odrivetool` to find and copy the path to the motor's `config.json` file.
   Provide this in configuration as the optional attribute `odrive_config_file`.
   See [add an `odrive_config_file`](#add-an-odrive_config_file) for more information.

   This option is not recommend for the `canbus` model.

   {{% /alert %}}

   Note that `iq_msg_rate_ms` in the `odrive_config_file` defaults to `0`, and you must set this to around `100` to use the [motor API's `SetPower` method](/components/motor/#setpower).

1. Follow [this guide](https://docs.odriverobotics.com/v/latest/control.html#control-doc) to tune your ODrive motor.

1. See the [ODrive CAN documentation](https://docs.odriverobotics.com/v/latest/can-guide.html) for detailed information on how to set up CAN on your ODrive.

   {{% alert title="Tip" color="tip" %}}

   If you are using a Raspberry Pi as your [board](/components/board/), you must run `sudo ip link set can0 up type can bitrate <baud_rate>` in your terminal to receive CAN messages.
   See [Troubleshooting: CAN Link Issues](https://github.com/viamrobotics/odrive#can-link-issues) for more information.

   Additionally, make sure you have [enabled SPI communication on your Pi](/get-started/installation/prepare/rpi-setup/) to use several common CANHats.

   {{% /alert %}}

1. Make sure your ODrive is connected to your [board](/components/board/) as follows, depending on whether you are using a `serial` or `canbus` connection:

   {{< tabs name="Connect your ODrive">}}
   {{% tab name="Serial" %}}

   Plug the [USB Isolator for Odrive](https://odriverobotics.com/shop/usb-c-to-usb-a-cable-and-usb-isolator) into a USB port on your board.
   Plug a USB-C to USB-A cable from the isolator to the ODrive.

   In the next section, you will add the version of the `odrive` module that supports ODrives using a `serial` connection.

   {{% /tab %}}
   {{% tab name="Canbus" %}}

   Wire the CANH and CANL pins from your board to your ODrive.
   Refer to your board and the [ODrive's pinout](https://docs.odriverobotics.com/v/latest/pinout.html) diagrams for the location of these pins.

   You must make a serial connection to set up your ODrive.
   If CAN chains together multiple ODrives, only one at a time must have this serial connection for reconfiguration.
   After setting up the ODrive, if you wish to use the `canbus` model, you can either leave the serial connection plugged in or remove it and leave only the CANH and CANL pins wired.

   Note that if you want to only use the CAN pins, you cannot specify an `"odrive_config_file"` in your Viam configuration.
   The ODrive would not be able to make the serial connection it needs to perform reconfiguration.

   In the next section, you will add the version of the `odrive` module that supports ODrives using a `canbus` connection.

   {{% /tab %}}
   {{< /tabs >}}

## Configuration

Physically connect the ODrive to your robot before adding the `odrive` module.

{{< tabs name="Add the ODrive component">}}
{{% tab name="Config Builder" %}}

Follow the instructions below to set up the `odrive` module on your robot:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Components** subtab and click **Create component** in the lower-left corner.
1. Select **Motor**, then select either `odrive:serial` or `odrive:canbus` depending on how you have connected your ODrive to your robot.
   You can also search for "odrive".
1. Click **Add module**, give your component a name of your choice, then click **Create**.
1. In the resulting `motor` component configuration pane, paste the following configuration into the **Attributes** text window, depending on whether you are using a `serial` or `canbus` connection:

{{< tabs name="Add attributes">}}
{{% tab name="Serial" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "serial_number": "<your-odrive-serial-number>",
  "odrive_config_file": "<local/path/to/motor/config.json>"
}
```

See the [Attributes](#attributes) section for more information on available attributes.

{{% /tab %}}
{{% tab name="Canbus" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "canbus_node_id": <int>
}
```

See the [Attributes](#attributes) section for more information on available attributes.

{{% /tab %}}
{{< /tabs >}}

To save your changes, click **Save config** at the bottom of the page.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.

Paste in the following configuration, depending on whether you are using a `serial` or `canbus` connection:

{{< tabs name="JSON Template by connection">}}
{{% tab name="Serial" %}}

```json
{
  "components": [
    {
      "name": "<your-odrive-name>",
      "model": "viam:odrive:serial",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "serial_number": "<your-odrive-serial-number>",
        "odrive_config_file": "<local/path/to/motor/config.json>"
      },
      "depends_on": []
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_odrive",
      "module_id": "viam:odrive",
      "version": "0.0.13"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Canbus" %}}

```json
{
  "components": [
    {
      "name": "<your-odrive-name>",
      "model": "viam:odrive:canbus",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "canbus_node_id": <int>
      },
      "depends_on": []
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_odrive",
      "module_id": "viam:odrive",
      "version": "0.0.13"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

To save your changes, click **Save config** at the bottom of the page.

{{% /tab %}}
{{% tab name="JSON Example" %}}

Go to your robot's page on the [Viam app](https://app.viam.com/).
Navigate to the **Config** tab on your robot's page and select **Raw JSON** mode.

Paste in the following configuration, depending on whether you are using a `serial` or `canbus` connection:

{{< tabs name="JSON Example by connection">}}
{{% tab name="Serial" %}}

```json
{
  "components": [
    {
      "name": "my-odrive",
      "model": "viam:odrive:serial",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "serial_number": "NUM000",
        "odrive_config_file": "/etc/odrive/config.json"
      },
      "depends_on": []
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_odrive",
      "module_id": "viam:odrive",
      "version": "0.0.13"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Canbus" %}}

```json
{
  "components": [
    {
      "name": "my-odrive",
      "model": "viam:odrive:canbus",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "canbus_node_id": 0
      },
      "depends_on": []
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_odrive",
      "module_id": "viam:odrive",
      "version": "0.0.13"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

To save your changes, click **Save config** at the bottom of the page.

{{% /tab %}}
{{< /tabs >}}

## Attributes

The following attributes are available for the motor resources available in the Viam ODrive module:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `canbus_node_id` | int | Optional | Required for successful initialization of the `canbus` type. <br> Node ID of the CAN node you would like to use. You configured this when [setting up your ODrive](https://docs.odriverobotics.com/v/latest/can-guide.html#setting-up-the-odrive). <br> Example: `0` |
| `odrive_config_file` | string | Optional | Filepath of a separate JSON file containing your ODrive's native configuration. See [add an `odrive_config_file`](#add-an-odrive_config_file) for instructions if you add this attribute. </br> See the [ODrive S1 Modular Component repository](https://github.com/viamrobotics/odrive/tree/main/sample-configs) for an example of this file. |
| `serial_number` | string | Optional | The serial number of the ODrive. Note that this is not necessary if you only have one ODrive connected. See [Troubleshooting: Hanging](https://github.com/viamrobotics/odrive#hanging) for help finding this value. |
| `canbus_baud_rate` | string | Optional | [Baud rate](https://docs.odriverobotics.com/v/latest/can-guide.html#setting-up-the-odrive) of the ODrive CAN protocol. This attribute is only available for `canbus` connections. </br> Use [`odrivetool`](https://docs.odriverobotics.com/v/latest/odrivetool.html) to obtain this value with `<odrv>.can.config.baud_rate`. Format the string as a multiple of 1000 (k). <br> Example: `"250k"` |

Check the [**Logs** tab](/build/program/debug/) of your robot in the Viam app to make sure your ODrive motor has connected and no errors are being raised.

{{% alert title="Tip" color="tip" %}}

The `"canbus"` type allows you to connect multiple ODrives without providing a `serial_number` as long as you have not defined any `odrive_config_file` once the drive has been configured with `odrivetool`.

{{% /alert %}}

### Add an `odrive_config_file`

To add an `odrive_config_file` and reconfigure your ODrive natively each time the motor is initialized on the robot, use [`odrivetool`](https://docs.odriverobotics.com/v/latest/odrivetool.html) to extract your configuration from your ODrive:

1. Run `odrivetool backup-config config.json` to extract your configs to a file called `config.json`.
   See the [ODrive documentation](https://docs.odriverobotics.com/v/latest/odrivetool.html#configuration-backup) for more info.
2. Configure `iq_msg_rate_ms` to a value appropriate for your usage.
   By default, `iq_msg_rate_ms` is set to `0`.
   You must set this to or around `100` to use the [motor API's `SetPower` method](/components/motor/#setpower).
3. If you add an `odrive_config_file` to a `canbus` motor, you will have to leave the serial connection established with your ODrive plugged in to the USB port, in addition to wiring the CANH and CANL pins.

See the [ODrive sample `config.json` file](https://github.com/viamrobotics/odrive/tree/main/sample-configs) for an example of an `odrive_config_file`.

An alternative to adding an `odrive_config_file` is running the command `odrivetool restore-config /path/to/config.json` in your terminal.
See the [ODrive documentation](https://docs.odriverobotics.com/v/latest/odrivetool.html#configuration-backup) for more info.

## Troubleshooting

See the [`odrive` module documentation](https://github.com/viamrobotics/odrive#troubleshooting) for help with common issues.

{{< snippet "social.md" >}}
