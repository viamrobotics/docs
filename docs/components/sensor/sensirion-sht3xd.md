---
title: "Configure a sensirion-sht3xd Sensor"
linkTitle: "sensirion-sht3xd"
weight: 70
type: "docs"
description: "Configure a sensirion-sht3xd model sensor."
tags: ["sensor", "components"]
icon: "/components/img/components/sensor.svg"
images: ["/components/img/components/sensor.svg"]
# SME: #team-bucket
---

Configure a `sensirion-sht3xd` sensor to integrate a [Sensirion SHT3x-DIS temperature and humidity sensor](https://www.adafruit.com/product/2857) into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `sensor`, and select the `sensirion-sht3xd` model.

Click **Create component**.

![Creation of a sensirion-sht3xd sensor in the Viam app config builder.](../img/sensirion-sht3xd-sensor-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensirion-sht3xd-sensor-name>",
      "type": "sensor",
      "model": "sensirion-sht3xd",
      "attributes": {
        "board": "<your-board-name>",
        "i2c_bus": "<your-i2c-bus-name-on-board>"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `sensirion-sht3xd` sensors:

| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------- |
| `board` | string | **Required** | The `name` of the [board](/components/board/) the sensor is wired to. |
| `i2c_bus` | string | **Required** | The `name` of the [I2C bus](/components/board/#i2cs) on the board that the sensor is wired to. |
| `i2c_address` | string | Optional | The [I2C device address](https://learn.adafruit.com/i2c-addresses/overview) of the sensor. <br> Default: `0x44` |
