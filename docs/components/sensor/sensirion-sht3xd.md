---
title: "Configure a sensirion-sht3xd Sensor"
linkTitle: "sensirion-sht3xd"
weight: 70
type: "docs"
description: "Configure a sensirion-sht3xd model sensor."
tags: ["sensor", "components"]
icon: "img/components/sensor.svg"
images: ["/components/img/components/sensor.svg"]
# SME: #team-bucket
---

Configure a `sensirion-sht3xd` sensor to integrate a [Sensirion SHT3x-DIS temperature and humidity sensor](https://www.adafruit.com/product/2857) into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `sensor`, and select the `sensirion-sht3xd` model.

Click **Create component**.
Paste into the **Attributes** box:

``` json
{
  "board": <your-board-name>,
  "i2c_bus": <your-i2c-bus-name>
}
```

![Creation of a sensirion-sht3xd sensor in the Viam app config builder.](../img/sensirion-sht3xd-sensor-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <your-sensirion-sht3xd-sensor-name>,
      "type": "sensor",
      "model": "sensirion-sht3xd",
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

The following attributes are available for `sensirion-sht3xd` sensors:

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `board`  | **Required** | The `name` of the [board](/components/board) the sensor is connected to. |
| `i2c_bus` | **Required** | The `name` of the [I2C bus](/components/board/#i2cs) on the board that the sensor is connected to. |
| `i2c_address`  | Optional | Default: `0x44`. The [I2C device address](https://learn.adafruit.com/i2c-addresses/overview) of the sensor. |
