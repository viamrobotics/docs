---
title: "Configure a renogy Sensor"
linkTitle: "renogy"
weight: 80
type: "docs"
description: "Configure a renogy model sensor."
tags: ["sensor", "components"]
icon: "/icons/components/sensor.svg"
images: ["/icons/components/sensor.svg"]
# SME: #team-bucket
---

Configure a `renogy` sensor to integrate a [Renogy battery temperature sensor](https://www.amazon.com/Renogy-Battery-Temperature-Sensor-Controllers/dp/B07WMMJFWY) into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `sensor` type, then select the `renogy` model.
Enter a name for your sensor and click **Create**.

![Creation of a renogy sensor in the Viam app config builder.](/components/sensor/renogy-sensor-ui-config.png)

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
| `serial_path` | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyS0`, to its device file, such as <file>/dev/ttyS0</file>. If you omit this attribute, Viam will attempt to automatically detect the path.<br>Default: `/dev/serial0` |
| `serial_baud_rate` | int | **Required** | The baud rate to use for serial communications. <br> Default: `9600` |
| `modbus_id`  | int | **Required** | Controller MODBUS address. <br> Default: `1` |
