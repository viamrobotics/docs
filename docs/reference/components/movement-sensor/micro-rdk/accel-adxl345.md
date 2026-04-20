---
title: "accel-adxl345"
linkTitle: "accel-adxl345"
titleMustBeLong: true
weight: 20
type: "docs"
description: "Reference for the accel-adxl345 movement-sensor model. ADXL345 digital accelerometer with a microcontroller."
images: ["/icons/components/imu.svg"]
aliases:
  - "/operate/reference/components/movement-sensor/accel-adxl345-micro-rdk/"
  - /micro-rdk/movement-sensor/accel-adxl345/
  - /components/movement-sensor/accel-adxl345-micro-rdk/
  - "/reference/components/movement-sensor/accel-adxl345-micro-rdk/"
micrordk_component: true
# SMEs: Rand, Kim Mishra
---

The `accel-adxl345` movement sensor model supports the Analog Devices [ADXL345 digital accelerometer](https://www.analog.com/en/products/adxl345.html).
This three axis accelerometer supplies linear acceleration data, supporting the `LinearAcceleration` method.

{{< tabs >}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "local",
  "i2c_bus": "default_i2c_bus"
}
```

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
| `board` | string | **Required** | The `name` of the [board](/reference/components/board/) to which the device is wired. |
| `i2c_bus` | string | **Required** | The `name` of the I<sup>2</sup>C bus on the [board](/reference/components/board/) wired to this device. |
| `use_alt_i2c_address` | bool | Optional | Depends on whether you wire SDO low (leaving the default address of 0x53) or high (making the address 0x1D). If high, set true. If low, set false or omit the attribute. <br> Default: `false` |
