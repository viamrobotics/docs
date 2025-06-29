---
title: "Configure an ADXL345 Accelerometer (Micro-RDK)"
linkTitle: "accel-adxl345 (Micro-RDK)"
titleMustBeLong: true
weight: 20
type: "docs"
description: "Configure an ADXL345 digital accelerometer with a microcontroller."
images: ["/icons/components/imu.svg"]
aliases:
  - /micro-rdk/movement-sensor/accel-adxl345/
  - /components/movement-sensor/accel-adxl345-micro-rdk/
micrordk_component: true
toc_hide: true
# SMEs: Rand, Kim Mishra
---

The `accel-adxl345` movement sensor model supports the Analog Devices [ADXL345 digital accelerometer](https://www.analog.com/en/products/adxl345.html).
This three axis accelerometer supplies linear acceleration data, supporting the `LinearAcceleration` method.

Physically connect your movement sensor to your microcontroller and power both on.
Then, configure the movement sensor:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `movement-sensor` type, then select the `accel-adxl345` model.
Enter a name or use the suggested name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/adxl345-builder.png" alt="Creation of an `accel-adxl345` movement sensor." resize="600x" class="shadow"  >}}

Copy and paste the following attribute template into your movement sensor's attributes field.
Then remove and fill in the attributes as applicable to your movement sensor, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "<your-board-name>",
  "i2c_bus": "<your-i2c-bus-name-on-board>",
  "use_alt_i2c_address": <boolean>,
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "local",
  "i2c_bus": "default_i2c_bus"
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
      "name": "<your-sensor-name>",
      "model": "accel-adxl345",
      "api": "rdk:component:movement_sensor",
      "attributes": {
        "board": "<your-board-name>",
        "i2c_bus": "<your-i2c-bus-name-on-board>",
        "use_alt_i2c_address": <boolean>
      }
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
      "name": "local",
      "model": "esp32",
      "api": "rdk:component:board",
      "attributes": {
        "pins": [15, 21, 22],
        "i2cs": [
          {
            "name": "default_i2c_bus",
            "bus": "i2c0",
            "data_pin": 21,
            "clock_pin": 22
          }
        ]
      }
    },
    {
      "name": "my-adxl",
      "model": "accel-adxl345",
      "api": "rdk:component:movement_sensor",
      "attributes": {
        "board": "local",
        "i2c_bus": "default_i2c_bus",
        "use_alt_i2c_address": false
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

<!-- prettier-ignore -->
| Name | Type   | Required? | Description |
| ---- | ------ | --------- | ----------- |
| `board` | string | **Required** | The `name` of the [board](/operate/reference/components/board/) to which the device is wired. |
| `i2c_bus` | string | **Required** | The `name` of the I<sup>2</sup>C bus on the [board](/operate/reference/components/board/) wired to this device. |
| `use_alt_i2c_address` | bool | Optional | Depends on whether you wire SDO low (leaving the default address of 0x53) or high (making the address 0x1D). If high, set true. If low, set false or omit the attribute. <br> Default: `false` |

## Test the movement sensor

After you configure your movement sensor, navigate to the [Control tab](/manage/troubleshoot/teleoperate/default-interface/) and select the dedicated movement sensor dropdown panel.
This panel presents the data collected by the movement sensor.

{{<imgproc src="/components/movement-sensor/movement-sensor-control-tab-adxl345.png" resize="400x" declaredimensions=true alt="The movement sensor component in the control tab">}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/movement-sensor.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/movement-sensor/" customTitle="Movement sensor API" noimage="true" %}}
{{% card link="/operate/get-started/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
