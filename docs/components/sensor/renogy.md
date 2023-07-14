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
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `sensor`, and select the `renogy` model.

Click **Create component**.

{{< imgproc src="/components/sensor/renogy-sensor-ui-config.png" alt="Creation of a renogy sensor in the Viam app config builder." resize="1000x" >}}

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
| `serial_path` | string | **Required** | The serial port your controller is connected to. <br> Default: `/dev/serial/0` |
| `serial_baud_rate` | int | **Required** | The baud rate to use for serial communications. <br> Default: `9600` |
| `modbus_id`  | int | **Required** | Controller MODBUS address. <br> Default: `1` |
