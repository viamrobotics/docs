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

Click **Create Component**.

![Creation of an `imu-vectornav` movement sensor in the Viam app config builder.](../../img/imu-vectornav-builder.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "type": "movement_sensor",
      "model": "imu-vectornav",
      "attributes": {
        "board": "<your-board-name>",
        "spi": "<your-spi-bus-name-on-board>",
        "spi_baud_rate": <int>,
        "polling_freq_hz": <int>,
        "chip_select_pin": "<pin-number-on-board>"
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

Name | Type | Inclusion | Description |
-----| ---- | --------- | ----------- |
`board` | string | **Required** | The `name` of the [board](/components/board) to which the device is wired.
`spi` | string | | The `name` of the [SPI bus](/components/board/#spis) over which the device communicates with the board.
`chip_select_pin` | string | **Required** | The ({{< glossary_tooltip term_id="pin-number" text="pin number" >}}) of the pin on the board (other than the SPI bus pins) connected to the IMU chip. Used to tell the chip whether the current SPI message is meant for it or for another device.
`spi_baud_rate` | int | **Required** | The rate at which data is sent from the IMU. <br> Default: `115200`
`polling_frequency_hz` | int | **Required** | How many times per second the sensor is polled.
