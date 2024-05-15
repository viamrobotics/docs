---
title: "Configure a Sensirion-SHT3x-DIS Sensor"
linkTitle: "sensirion-sht3xd"
weight: 70
type: "docs"
description: "Configure a sensirion-sht3xd model sensor."
tags: ["sensor", "components"]
icon: true
images: ["/icons/components/sensor.svg"]
aliases:
  - "/machine/components/sensor/sensirion-sht3xd/"
# SME: #team-bucket
---

Configure a `sensirion-sht3xd` sensor to integrate a [Sensirion SHT3x-DIS temperature and humidity sensor](https://www.adafruit.com/product/2857) into your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `sensor` type, then select the `sensirion-sht3xd` model.
Enter a name or use the suggested name for your sensor and click **Create**.

![Creation of a sensirion-sht3xd sensor in the Viam app config builder.](/machine/components/sensor/sensirion-sht3xd-sensor-ui-config.png)

Fill in the attributes as applicable to your sensor, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensirion-sht3xd-sensor-name>",
      "model": "sensirion-sht3xd",
      "type": "sensor",
      "namespace": "rdk",
      "attributes": {
        "i2c_bus": "<your-i2c-bus-index-on-board>",
        "i2c_address": "<your-i2c-address>"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `sensirion-sht3xd` sensors:

<!-- prettier-ignore -->
| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------- |
| `i2c_bus` | string | **Required** | The index of the I2C bus on the board that the sensor is wired to. |
| `i2c_address` | string | Optional | The [I2C device address](https://learn.adafruit.com/i2c-addresses/overview) of the sensor. <br> Default: `0x44` |

{{< readfile "/static/include/components/test-control/sensor-control.md" >}}
