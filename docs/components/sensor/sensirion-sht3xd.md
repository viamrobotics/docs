---
title: "Configure a Sensirion-SHT3x-DIS Sensor"
linkTitle: "sensirion-sht3xd"
weight: 70
type: "docs"
description: "Configure a sensirion-sht3xd model sensor."
tags: ["sensor", "components"]
icon: "/icons/components/sensor.svg"
images: ["/icons/components/sensor.svg"]
aliases:
  - "/components/sensor/sensirion-sht3xd/"
# SME: #team-bucket
---

Configure a `sensirion-sht3xd` sensor to integrate a [Sensirion SHT3x-DIS temperature and humidity sensor](https://www.adafruit.com/product/2857) into your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `sensor` type, then select the `sensirion-sht3xd` model.
Enter a name for your sensor and click **Create**.

![Creation of a sensirion-sht3xd sensor in the Viam app config builder.](/components/sensor/sensirion-sht3xd-sensor-ui-config.png)

Copy and paste the following attribute template into your sensor's **Attributes** box.
Then remove and fill in the attributes as applicable to your sensor, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "i2c_bus": "<your-i2c-bus-index-on-board>"
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "i2c_bus": "2"
}
```

{{% /tab %}}
{{< /tabs >}}

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
