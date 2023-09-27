---
title: "Configure a renogy power sensor"
linkTitle: "renogy"
weight: 10
type: "docs"
description: "Configure a renogy model power sensor to return battery voltage and load current, power, and various other readings."
tags: ["power sensor", "components", "renogy"]
icon: "/icons/components/sensor.svg"
images: ["/icons/components/sensor.svg"]
# SME: #team-bucket
---

Configure a `renogy` sensor to integrate a [Renogy battery temperature sensor](https://www.renogy.com/wanderer-10a-pwm-charge-controller/) into your robot:

{{< tabs name="Configure a Renogy Sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component** in the lower-left corner.
Select the type `power_sensor`, then select the `renogy` model.
Name your sensor, and click **Create**.

{{<imgproc src="/components/power-sensor/renogy-config-builder.png" resize="800x" declaredimensions=true alt="Renogy power sensor configuration tab ">}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "ren1",
      "type": "power_sensor",
      "model": "renogy",
      "attributes": {
        "serial_path": "string",
        "serial_baud_rate": "integer",
        "modbus_id": "integer"
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
      "type": "power_sensor",
      "model": "renogy",
      "attributes": {
        "serial_path": "/dev/serial0",
        "serial_baud_rate": 9600,
        "modbus_id": 1
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}
The following attributes are available for `renogy` sensors:

<!-- prettier-ignore -->
| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------- |
| `serial_path` | string | Optional | The full filesystem path to the serial device, starting with /dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyS0`, to its device file, such as <file>/dev/ttyS0</file>. If you omit this attribute, Viam will attempt to automatically detect the path. On a Raspberry Pi, you can also run `ls /dev/serial/by-path` to list USB serial devices. If you omit this attribute, Viam will attempt to automatically detect the path.<br>Example: `"/dev/serial/by-path/usb-0:1.1:1.0"` <br>Default: `/dev/serial0` |
| `serial_baud_rate` | integer | Optional | The baud rate to use for serial communications. <br> Default: `9600` |
| `modbus_id`  | integer | Optional | Controller MODBUS address. <br> Default: `1` |
