---
title: "Configure a power_ina219 Sensor"
linkTitle: "power_ina219"
weight: 70
draft: false
type: "docs"
description: "Configure a power_ina219 model sensor."
tags: ["sensor", "components"]
icon: "img/components/sensor.png"
# SME: #team-bucket
---

Configure a `power_ina219` sensor to integrate a [INA219 current sensor](https://www.amazon.com/dp/B07QJW6L4C) into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `sensor`, and select the `power_ina219` model.

Click **Create component**.
Paste into the **Attributes** box:

``` json
{
  "board": <your-board-name>,
  "i2c_bus": <your-i2c-bus-name>
}
```

![Creation of a power_ina219 sensor in the Viam app config builder.](../img/power-ina219-sensor-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <your-power_ina219-sensor-name>,
      "type": "sensor",
      "model": "power_ina219",
      "attributes": {
        "board": <your-board-name>,
        "i2c_bus": <your-i2c-bus-name>
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
| `board`  | **Required** | The `name` of the [board](/components/board) the sensor is connected to. |
| `i2c_bus` | **Required** | The `name` of the [I2C bus](/components/board/#i2c) on the board that the sensor is connected to. |
| `i2c_address`  | Optional | Default: `0x40`. The [I2C device address](https://learn.adafruit.com/i2c-addresses/overview) of the sensor. |
