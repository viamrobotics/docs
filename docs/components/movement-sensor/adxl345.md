---
title: "Configure an ADXL345 Accelerometer"
linkTitle: "accel-adxl345"
weight: 20
type: "docs"
description: "Configure an ADXL345 digital accelerometer."
images: ["/icons/components/imu.svg"]
# SMEs: Rand, Kim Mishra
---

The `accel-adxl345` movement sensor model supports the Analog Devices [ADXL345 digital accelerometer](https://www.analog.com/en/products/adxl345.html).
This three axis accelerometer supplies linear acceleration data, supporting the `LinearAcceleration` method.

If you are using a [Viam Rover](https://docs.viam.com/try-viam/), this is the accelerometer on it.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `movement-sensor` type, then select the `accel-adxl345` model.
Enter a name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/adxl345-builder.png" alt="Creation of an `accel-adxl345` movement sensor in the Viam app config builder." resize="600x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "type": "movement_sensor",
      "model": "accel-adxl345",
      "attributes": {
        "board": "<your-board-name>",
        "i2c_bus": "<your-spi-bus-name-on-board>",
        "use_alternate_i2c_address": <boolean>,
        "tap": {
           "accelerometer_pin": <int>,
            "interrupt_pin": "<your-digital-interrupt-name-on-board>",
            "exclude_x": <boolean>,
            "exclude_y": <boolean>,
            "exclude_z": <boolean>,
            "threshold": <float>,
            "dur_us": <float>
        },
        "free_fall": {
            "accelerometer_pin": <int>,
            "interrupt_pin": "<your-digital-interrupt-name-on-board>",
            "threshold": <float>,
            "time_ms": <float>
        }
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
      "type": "board",
      "model": "pi",
      "attributes": {
        "i2cs": [
          {
            "name": "default_i2c_bus",
            "bus": "1"
          }
        ]
      }
    },
    {
      "name": "my-adxl",
      "type": "movement_sensor",
      "model": "accel-adxl345",
      "attributes": {
        "board": "local",
        "i2c_bus": "default_i2c_bus",
        "use_alternate_i2c_address": false
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

Name | Type | Inclusion | Description
---- | ---- | --------- | ---- | -----------
`board` | string | **Required** | The `name` of the [board](/components/board/) to which the device is wired.
`i2c_bus` | string | **Required** | The `name` of the [I<sup>2</sup>C bus configured](/components/board/#i2cs) on the [board](/components/board/) wired to this device.
`use_alt_i2c_address` | bool | Optional | Depends on whether you wire SDO low (leaving the default address of 0x53) or high (making the address 0x1D). If high, set true. If low, set false or omit the attribute. <br> Default: `false`
`tap` | object | Optional | Holds the configuration values necessary to use the tap detection interrupt on the ADXL345. See [table below](#tap-attributes).
`free_fall` | object | Optional | Holds the configuration values necessary to use the free-fall detection interrupt on the ADXL345. See [table below](#freefall-attributes).

### Tap attributes

Inside the `tap` object, you can include the following attributes:

Name | Type | Inclusion | Description
---- | ---- | --------- | -----------
`accelerometer_pin` | int | **Required** | On the accelerometer you can choose to send the interrupts to int1 or int2. Specify this by setting this config value to `1` or `2`.
`interrupt_pin` | string | **Required** | The `name` of the [digital interrupt](/components/board/#digital_interrupts) you configured for the pin on the [board](/components/board/) wired to the `accelerometer_pin`.
`exclude_x` | bool | Optional | Tap detection defaults to all three axes. Exclude the x axis by setting this to true. <br> Default: `false`
`exclude_y` | bool | Optional | Tap detection defaults to all three axes. Exclude the y axis by setting this to true. <br> Default: `false`
`exclude_z` | bool | Optional | Tap detection defaults to all three axes. Exclude the z axis by setting this to true. <br> Default: `false`
`threshold` | float | Optional | The magnitude of the threshold value for tap interrupt (in milligrams, between 0 and 15,937). <br> Default: `3000`
`dur_us` | float | Optional | Unsigned time value representing maximum time that an event must be above the `threshold` to qualify as a tap event (in microseconds, between 0 and 159,375). <br> Default: `10000`

### Freefall attributes

Inside the `freefall` object, you can include the following attributes:

Name | Type | Inclusion | Default Value | Description
---- | ---- | --------- |  ------------- | -----------
`accelerometer_pin` | int | **Required** | On the accelerometer you can choose to send the interrupts to int1 or int2. Specify this by setting this config value to `1` or `2`.
`interrupt_pin` | string | **Required** | The `name` of the [digital interrupt](/components/board/#digital_interrupts) you configured for the pin on the [board](/components/board/) wired to the `accelerometer_pin`.
`threshold` | float | Optional | The acceleration on each axis is compared with this value to determine if a free-fall event occurred (in milligrams, between 0 and 15,937). <br> Default: `437.5`
`time_ms` | float | Optional | Unsigned time value representing the minimum time that the value of all axes must be less than `threshold` to generate a free-fall interrupt (in milliseconds, between 0 and 1,275). <br> Default: `160`

{{< readfile "/static/include/components/movement-sensor-control.md" >}}
