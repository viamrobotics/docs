---
title: "Configure a roboclaw motor"
linkTitle: "roboclaw"
weight: 22
type: "docs"
description: "Configure a brushed DC motor driven by a roboclaw motor controller."
images: ["/icons/components/motor.svg"]
# SMEs: Olivia, Rand
---

The `roboclaw` model of the motor component supports [standard brushed DC motors](https://en.wikipedia.org/wiki/DC_motor) driven by [Basicmicro's](https://www.basicmicro.com/) [RoboClaw](https://www.basicmicro.com/RoboClaw-2x30A-Motor-Controller_p_9.html) motor controller.

{{< alert title="Note" color="note" >}}

You must set up your RoboClaw before configuring it.
Make note of the baud rate that you set up during this process.
The default is `38400`.
Follow [this guide](https://resources.basicmicro.com/roboclaw-motor-controllers-getting-started-guide/) to do so.

{{< /alert >}}

To configure a `roboclaw` motor as a component of your robot:

{{< tabs name="Configure your roboclaw motor">}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `motor` type, then select the `roboclaw` model.
Enter a name for your motor and click **Create**.

![A roboclaw motor config.](/components/motor/roboclaw-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json
{
  "components": [
    {
      "name": "<your-roboclaw-motor-name>",
      "type": "motor",
      "model": "roboclaw",
      "attributes": {
        "serial_path": "<your-serial-path>",
        "motor_channel": <int>,
        "serial_baud_rate": <int>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

Example configuration for a `roboclaw` DC brushed motor:

```json
{
  "components": [
    {
      "name": "your-roboclaw-motor",
      "type": "motor",
      "model": "roboclaw",
      "attributes": {
        "serial_path": "/dev/ttyUSB0",
        "motor_channel": 1,
        "serial_baud_rate": 38400
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `roboclaw` motors:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `serial_path` | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyAMA0` , to its device file, such as <file>/dev/ttyAMA0</file>. On a Raspberry Pi, you can also run `ls /dev/serial/by-path` to list USB serial devices. If you omit this attribute, Viam will attempt to automatically detect the path.<br>Example: `"/dev/serial/by-path/usb-0:1.1:1.0"` |
| `serial_baud_rate` | int | Optional | [Rate to send data](https://learn.sparkfun.com/tutorials/serial-communication) over the serial line. This must match the baudrate you have set up using basicmicro's setup program. You cannot have multiple `roboclaw` motors with different baud rates. <br> Default: `38400` |
| `motor_channel` | int | **Required** | Channel the motor is connected to on the controller. Must be `1` or `2`. |
| `address` | int | Optional | Serial address of the controller. <br> Default: `128`  |
| `ticks_per_rotation` | int | Optional | Number of full steps in a rotation. Update this if you connect [encoders](/components/encoder/) to your controller through its EN1 and EN2 pins. <br> Default: `0` |

Refer to your motor and motor driver data sheets for specifics.

{{< readfile "/static/include/components/test-control/motor-control.md" >}}
