---
title: "Configure an ADXL345 Accelerometer"
linkTitle: "accel-adxl345"
weight: 20
type: "docs"
description: "Configure an ADXL345 digital accelerometer."
images: ["/icons/components/imu.svg"]
aliases:
  - "/machine/components/movement-sensor/adxl345/"
# SMEs: Rand, Kim Mishra
---

The `accel-adxl345` movement sensor model supports the Analog Devices [ADXL345 digital accelerometer](https://www.analog.com/en/products/adxl345.html).
This three axis accelerometer supplies linear acceleration data, supporting the `LinearAcceleration` method.

If you are using a [Viam Rover](/get-started/try-viam/), this is the accelerometer on it.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `movement-sensor` type, then select the `accel-adxl345` model.
Enter a name or use the suggested name for your movement sensor and click **Create**.

{{< imgproc src="/machine/components/movement-sensor/adxl345-builder.png" alt="Creation of an `accel-adxl345` movement sensor in the Viam app config builder." resize="1200x" style="width:650px" >}}

Fill in the attributes as applicable to your movement sensor, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "model": "accel-adxl345",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "board": "<your-board-name>",
        "i2c_bus": "<your-i2c-bus-index-on-board>",
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
      "name": "my-adxl",
      "model": "accel-adxl345",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "i2c_bus": "2",
        "use_alternate_i2c_address": false
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

<!-- prettier-ignore -->
| Name | Type   | Inclusion    | Description |
| ---- | ------ | ------------ | ----------- |
| `i2c_bus` | string | **Required** | The index of the I2C bus on the board your device is connected to. Often a number. <br> Example: "2"  |
| `use_alternate_i2c_address` | bool | Optional | Depends on whether you wire SDO low (leaving the default address of 0x53) or high (making the address 0x1D). If high, set true. If low, set false or omit the attribute. <br> Default: `false` |
| `board` | string | Optional | The `name` of the [board](/machine/components/board/) to which the device is wired. Only needed if you've configured any [interrupt](/machine/components/board/#digital_interrupts) functionality. |
| `tap` | object | Optional | Holds the configuration values necessary to use the tap detection interrupt on the ADXL345. See [Tap attributes](#tap-attributes). |
| `free_fall` | object | Optional | Holds the configuration values necessary to use the free-fall detection interrupt on the ADXL345. See [Freefall attributes](#freefall-attributes). |

### Tap attributes

Inside the `tap` object, you can include the following attributes:

<!-- prettier-ignore -->
| Name                | Type   | Inclusion    | Description |
| ------------------- | ------ | ------------ | ----------- |
| `accelerometer_pin` | int    | **Required** | On the accelerometer you can choose to send the interrupts to int1 or int2. Specify this by setting this config value to `1` or `2`. |
| `interrupt_pin`     | string | **Required** | The `name` of the [digital interrupt](/machine/components/board/#digital_interrupts) you configured for the pin on the [board](/machine/components/board/) wired to the `accelerometer_pin`. |
| `exclude_x`         | bool   | Optional     | Tap detection defaults to all three axes. Exclude the x axis by setting this to true. <br> Default: `false` |
| `exclude_y`         | bool   | Optional     | Tap detection defaults to all three axes. Exclude the y axis by setting this to true. <br> Default: `false` |
| `exclude_z`         | bool   | Optional     | Tap detection defaults to all three axes. Exclude the z axis by setting this to true. <br> Default: `false` |
| `threshold`         | float  | Optional     | The magnitude of the threshold value for tap interrupt (in milligrams, between `0` and `15,937`). <br> Default: `3000` |
| `dur_us`            | float  | Optional     | Unsigned time value representing maximum time that an event must be above the `threshold` to qualify as a tap event (in microseconds, between 0 and 159,375). <br> Default: `10000` |

### Freefall attributes

Inside the `freefall` object, you can include the following attributes:

<!-- prettier-ignore -->
| Name                | Type   | Inclusion    | Default Value | Description |
| ------------------- | ------ | ------------ | ------------- | ----------- |
| `accelerometer_pin` | int    | **Required** | On the accelerometer you can choose to send the interrupts to int1 or int2. Specify this by setting this config value to `1` or `2`. |
| `interrupt_pin`     | string | **Required** | The `name` of the [digital interrupt](/machine/components/board/#digital_interrupts) you configured for the pin on the [board](/machine/components/board/) wired to the `accelerometer_pin`. |
| `threshold`         | float  | Optional     | The acceleration on each axis is compared with this value to determine if a free-fall event occurred (in milligrams, between `0` and `15,937`). <br> Default: `437.5` |
| `time_ms`           | float  | Optional     | Unsigned time value representing the minimum time that the value of all axes must be less than `threshold` to generate a free-fall interrupt (in milliseconds, between 0 and 1,275). <br> Default: `160` |

## Test the movement sensor

After you configure your movement sensor, navigate to the [Control tab](/app/fleet/control/) and select the dedicated movement sensor dropdown panel.
This panel presents the data collected by the movement sensor.

{{<imgproc src="/machine/components/movement-sensor/movement-sensor-control-tab-adxl345.png" resize="400x" declaredimensions=true alt="The movement sensor component in the control tab">}}
