---
title: "Configure a Renogy Power Sensor"
linkTitle: "renogy"
weight: 10
type: "docs"
description: "Configure a renogy model power sensor to return battery voltage and load current, power, and various other readings."
tags: ["power sensor", "components", "renogy"]
icon: true
images: ["/icons/components/sensor.svg"]
aliases:
  - "/components/power-sensor/renogy/"
# SME: #team-bucket
---

Configure a `renogy` sensor to integrate a [Renogy charge controller](https://www.renogy.com/wanderer-10a-pwm-charge-controller/) into your machine:

{{< tabs name="Configure a Renogy Sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `power_sensor` type, then select the `renogy` model.
Enter a name for your sensor and click **Create**.

{{<imgproc src="/components/power-sensor/renogy-config-builder.png" resize="800x" declaredimensions=true alt="Renogy power sensor configuration tab ">}}

Edit the attributes as applicable to your power sensor, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "ren1",
      "model": "renogy",
      "type": "power_sensor",
      "namespace": "rdk",
      "attributes": {
        "serial_path": "<string>",
        "serial_baud_rate": <int>,
        "modbus_id": <int>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "your-renogy-sensor",
      "model": "renogy",
      "type": "power_sensor",
      "namespace": "rdk",
      "attributes": {
        "serial_path": "/dev/serial/by-path/usb-0:1.1:1.0",
        "serial_baud_rate": 9600,
        "modbus_id": 1
      },
      "depends_on": []
    }
  ]
}
```

The `"serial_path"` filepath used in this example is specific to serial devices connected to Linux systems.
The `"serial_path"` filepath on a macOS system might resemble <file>"/dev/ttyUSB0"</file> or <file>"/dev/ttyS0"</file>.

{{% /tab %}}
{{% /tabs %}}
The following attributes are available for `renogy` sensors:

<!-- prettier-ignore -->
| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------- |
| `serial_path` | string | Optional | The full filesystem path to the serial device, starting with <file>/dev/</file>. To find your serial device path, first connect the serial device to your machine, then:<ul><li>On Linux, run <code>ls /dev/serial/by-path/\*</code> to show connected serial devices, or look for your device in the output of <code>sudo dmesg \| grep tty</code>. Example: <code>"/dev/serial/by-path/usb-0:1.1:1.0"</code>.</li><li>On macOS, run <code>ls /dev/tty\* \| grep -i usb</code> to show connected USB serial devices, <code>ls /dev/tty\*</code> to browse all devices, or look for your device in the output of <code>sudo dmesg \| grep tty</code>. Example: <code>"/dev/ttyS0"</code>.</li></ul><br>Default: `/dev/serial0` |
| `serial_baud_rate` | integer | Optional | The baud rate to use for serial communications. <br> Default: `9600` |
| `modbus_id`  | integer | Optional | Controller MODBUS address. <br> Default: `1` |

{{< readfile "/static/include/components/test-control/power-sensor-control.md" >}}
