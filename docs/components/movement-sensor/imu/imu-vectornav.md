---
title: "Configure a VectorNav IMU"
linkTitle: "imu-vectornav"
weight: 10
type: "docs"
description: "Configure a VectorNav IMU."
images: ["/components/img/components/imu.svg"]
# SMEs: Rand
---

An [inertial measurement unit (IMU)](https://en.wikipedia.org/wiki/Inertial_measurement_unit) provides data for the `AngularVelocity`, `Orientation`, `CompassHeading`, and `LinearAcceleration` methods.
Acceleration and magnetometer data are available by using the [sensor](../../../sensor/) `GetReadings` method, which IMUs wrap.

The `imu-vectornav` movement sensor model supports IMUs manufactured by [VectorNav](https://www.vectornav.com/products) that support SPI connection.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** sub-tab and navigate to the **Create component** menu.

Enter a name for your movement sensor, select the `movement-sensor` type, and select the `imu-vectornav` model.

![Creation of an `imu-vectornav` movement sensor in the Viam app config builder.](../../img/imu-vectornav-builder.png)

Click **Create Component** and then fill in the attributes for your model.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <sensor_name>,
      "type": "movement_sensor",
      "model": "imu-vectornav",
      "attributes": {
        "board": <board_name>,
        "spi": <string>,
        "spi_baud_rate": <int>,
        "polling_freq_hz": <int>,
        "chip_select_pin": <string>
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
      "name": "myIMU",
      "type": "movement_sensor",
      "model": "imu-vectornav",
      "attributes": {
        "board": "local",
        "spi": "1",
        "spi_baud_rate": 3800,
        "polling_freq_hz": 80,
        "chip_select_pin": "36"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

Name | Type | Default Value | Description
----- | ----- | ----- | -----
`board` | string | - | The name of the board to which the device is wired
`spi` | string | - | The name of the SPI bus over which the device communicates with the board. On a Raspberry Pi, people often use the bus named "1."
`chip_select_pin` | string | - | The board pin (other than the SPI bus pins) connected to the IMU chip. Used to tell the chip whether the current SPI message is meant for it or for another device.
`spi_baud_rate` | int | 115200 | The rate at which data is sent from the IMU.
`polling_frequency_hz` | int | - | How many times per second the sensor is polled.
