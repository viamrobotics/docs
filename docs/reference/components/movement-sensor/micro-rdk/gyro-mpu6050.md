---
title: "gyro-mpu6050"
linkTitle: "gyro-mpu6050"
weight: 40
type: "docs"
description: "Reference for the gyro-mpu6050 movement-sensor model. MPU-6050 movement sensor with a microcontroller."
images: ["/icons/components/imu.svg"]
aliases:
  - /micro-rdk/movement-sensor/gyro-mpu6050/
  - /build/micro-rdk/movement-sensor/gyro-mpu6050/
  - /components/movement-sensor/gyro-mpu6050-micro-rdk/
  - "/operate/reference/components/movement-sensor/gyro-mpu6050-micro-rdk/"
micrordk_component: true
# SMEs: Rand
---

The `gyro-mpu6050` movement sensor model supports a combination [gyroscope and accelerometer manufactured by TDK InvenSense](https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/).

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
      "model": "gyro-mpu6050",
      "api": "rdk:component:movement_sensor",
      "attributes": {
        "board": "<your-board-name>",
        "i2c_bus": "<your-i2c-bus-name-on-board>",
        "use_alt_i2c_address": <boolean>
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
      "name": "my_accelgyro",
      "model": "gyro-mpu6050",
      "api": "rdk:component:movement_sensor",
      "attributes": {
        "board": "local",
        "i2c_bus": "default_i2c_bus"
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

<!-- prettier-ignore -->
| Name                  | Type    | Required? | Description |
| --------------------- | ------- | --------- | ----------- |
| `board`               | string  | **Required** | The `name` of the [board](/reference/components/board/) to which the device is wired. |
| `i2c_bus`             | string  | **Required** | The `name` of the I<sup>2</sup>C bus configured on your [board](/reference/components/board/) wired to this device. |
| `use_alt_i2c_address` | boolean | Optional     | Depends on whether you wire AD0 low (leaving the default address of 0x68) or high (making the address 0x69). If high, set `true`. If low, set `false`. <br> Default: `false` |
