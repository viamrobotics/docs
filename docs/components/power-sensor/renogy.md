---
title: "Configure a renogy sensor"
linkTitle: "renogy"
weight: 80
type: "docs"
description: "Configure a renogy model sensor."
tags: ["sensor", "components"]
icon: "/icons/components/sensor.svg"
images: ["/icons/components/sensor.svg"]
# SME: #team-bucket
---

Configure a `renogy` sensor to integrate a [Renogy battery temperature sensor](https://www.renogy.com/battery-temperature-sensor-for-renogy-solar-charge-controllers/) into your robot's system:

{{< tabs name="Configure an Renogy Sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu. Select the type `power_sensor`, then select the `renogy` model. Name your sensor, and click **Create**.

{{<imgproc src="/components/power-sensor/renogy-config-builder.png" resize="800x" declaredimensions=true alt="Renogy power sensor configuration tab ">}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}
```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-renogy-sensor-name>",
      "type": "sensor",
      "model": "renogy",
      "attributes": {
        "serial_path": "<your-serial-path>",
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
      "type": "sensor",
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

| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------- |
| `serial_path` | string | Optional | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyS0`, to its device file, such as <file>/dev/ttyS0</file>. If you omit this attribute, Viam will attempt to automatically detect the path.<br>Default: `/dev/serial0` |
| `serial_baud_rate` | integer | Optional | The baud rate to use for serial communications. <br> Default: `9600` |
| `modbus_id`  | integer | Optional | Controller MODBUS address. <br> Default: `1` |
