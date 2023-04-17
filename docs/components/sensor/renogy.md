---
title: "Configure a renogy Sensor"
linkTitle: "renogy"
weight: 80
type: "docs"
description: "Configure a renogy model sensor."
tags: ["sensor", "components"]
icon: "img/components/sensor.png"
# SME: #team-bucket
---

Configure a `renogy` sensor to integrate a [Renogy battery temperature sensor](https://www.amazon.com/Renogy-Battery-Temperature-Sensor-Controllers/dp/B07WMMJFWY) into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

On the **Components** subtab of your robot's page in [the Viam app](https://app.viam.com), navigate to the **Create Component** menu.
Enter a name for your sensor, select the type `sensor`, and select the `renogy` model.

Paste into the **Attributes** box:

``` json
{
  "serial_path": "/dev/serial0",
  "serial_baud_rate": 9600,
  "modbus_id": 1
}
```

Adjust these `attributes` from these default values as necessary.

![Creation of a renogy sensor in the Viam app config builder.](../img/renogy-sensor-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <your-renogy-sensor-name>,
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

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `serial_path`  | **Required** | Default: `/dev/serial/0`. The serial port your controller is connected to. |
| `serial_baud_rate` | **Required** | Default: `9600`. The baud rate to use for serial communications. |
| `modbus_id`  | **Required** | Default: `1`. Controller MODBUS address. |
