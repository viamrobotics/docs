---
title: "Configure an ADXL345 Accelerometer"
linkTitle: "accel-adxl345"
weight: 10
type: "docs"
description: "Configure an ADXL345 digital accelerometer."
# SMEs: Rand, Kim Mishra
---

The `accel-adxl345` movement sensor model supports the Analog Devices [ADXL345 digital accelerometer](https://www.analog.com/en/products/adxl345.html).
This three axis accelerometer supplies linear acceleration data, supporting the `LinearAcceleration` method.

If you are using a [Viam Rover](https://docs.viam.com/try-viam/), this is the accelerometer on it.

{{< tabs >}}
{{% tab name="Config Builder" %}}

On the **COMPONENTS** sub-tab, navigate to the **Create Component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `accel-adxl345` model.

![Creation of an `accel-adxl345` movement sensor in the Viam app config builder.](../img/adxl345-builder.png)

Click **Create Component** and then fill in the attributes for your model.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <sensor_name>,
      "type": "movement_sensor",
      "model": "accel-adxl345",
      "attributes": {
        "board": <string>,
        "i2c_bus": <string>,
        "use_alternate_i2c_address": <boolean>,
        "tap": {
           "accelerometer_pin": <integer>,
            "interrupt_pin": <string>,
            "exclude_x": <boolean>,
            "exclude_y": <boolean>,
            "exclude_z": <boolean>,
            "threshold": <float>,
            "dur_us": <float>
        },
        "free_fall": {
            "accelerometer_pin": <integer>,
            "interrupt_pin": <string>,
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

Name | Inclusion | Type | Default Value | Description
---- | --------- | ---- | ------------- | -----------
`board` | **Required** | string | - | The name of the board to which the device is wired.
`i2c_bus` | **Required** | string | - | The name of the I<sup>2</sup>C bus through which the device communicates with the SBC. Note that this must match the name you gave the I<sup>2</sup>C bus you configured in the board component.
`use_alt_i2c_address` | Optional | bool | false | Depends on whether you wire SDO low (leaving the default address of 0x53) or high (making the address 0x1D). If high, set true. If low, set false or omit the attribute.
`tap` | Optional | object | - | Holds the configuration values necessary to use the tap detection interrupt on the ADXL345. See [table below](#tap-attributes).
`free_fall` | Optional | object | - | Holds the configuration values necessary to use the free-fall detection interrupt on the ADXL345. See [table below](#freefall-attributes).

### Tap attributes

Inside the `tap` object, you can include the following attributes:

Name | Inclusion | Type | Default Value | Description
---- | --------- | ---- | ------------- | -----------
`accelerometer_pin` | **Required** | int | - | On the accelerometer you can choose to send the interrupts to int1 or int2. Specify this by setting this config value to 1 or 2.
`interrupt_pin` | **Required** | string | - | The string name you gave your interrupt pin on your board.
`exclude_x` | Optional | bool | false | Tap detection defaults to all three axes. Exclude the x axis by setting this to true.
`exclude_y` | Optional | bool | false | Tap detection defaults to all three axes. Exclude the y axis by setting this to true.
`exclude_z` | Optional | bool | false | Tap detection defaults to all three axes. Exclude the z axis by setting this to true.
`threshold` | Optional | float32 | 3000 | The magnitude of the threshold value for tap interrupt (in milligrams, between 0 and 15,937).
`dur_us` | Optional | float32 | 10 | Unsigned time value representing maximum time that an event must be above the `threshold` to qualify as a tap event (in microseconds, between 0 and 159,375).

### Freefall attributes

Inside the `freefall` object, you can include the following attributes:

Name | Inclusion | Type | Default Value | Description
---- | --------- | ---- | ------------- | -----------
`accelerometer_pin` | **Required** | int | - | On the accelerometer you can choose to send the interrupts to int1 or int2. Specify this by setting this config value to 1 or 2.
`interrupt_pin` | **Required** | string | - | The string name you gave your interrupt pin on your board.
`threshold` | Optional | float32 | 437.5 | The acceleration on each axis is compared with this value to determine if a free-fall event occurred (in milligrams, between 0 and 15,937).
`time_ms` | Optional | float32 | 160 | Unsigned time value representing the minimum time that the value of all axes must be less than `threshold` to generate a free-fall interrupt (in milliseconds, between 0 and 1,275).
