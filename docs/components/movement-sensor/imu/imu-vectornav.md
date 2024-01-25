---
title: "Configure a VectorNav IMU"
linkTitle: "imu-vectornav"
weight: 10
type: "docs"
description: "Configure a VectorNav IMU."
images: ["/icons/components/imu.svg"]
draft: true
aliases:
  - "/components/movement-sensor/imu/imu-vectornav/"
# SMEs: Rand
---

An [inertial measurement unit (IMU)](https://en.wikipedia.org/wiki/Inertial_measurement_unit) provides data for the `AngularVelocity`, `Orientation`, `CompassHeading`, and `LinearAcceleration` methods.
Acceleration and magnetometer data are available by using the [sensor](/components/sensor/) `GetReadings` method, which IMUs wrap.

The `imu-vectornav` movement sensor model supports IMUs manufactured by [VectorNav](https://www.vectornav.com/products) that support SPI connection.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `movement-sensor` type, then select the `imu-vectornav` model.
Enter a name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/imu-vectornav-builder.png" alt="Creation of an `imu-vectornav` movement sensor in the Viam app config builder." resize="600x" >}}

Copy and paste the following attribute template into your movement sensor's **Attributes** box.
Then remove and fill in the attributes as applicable to your movement sensor, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "<your-board-name>",
  "spi": "<your-spi-bus-name-on-board>",
  "spi_baud_rate": <int>,
  "polling_freq_hz": <int>,
  "chip_select_pin": "<pin-number-on-board>"
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "local",
  "spi": "1",
  "spi_baud_rate": 3800,
  "polling_freq_hz": 80,
  "chip_select_pin": "36"
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
      "model": "imu-vectornav",
      "type": "movement_sensor",
      "namespace": "rdk",
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
      "model": "imu-vectornav",
      "type": "movement_sensor",
      "namespace": "rdk",
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

| Name                   | Type   | Inclusion    | Description                                                                                                                                                                                                                                         |
| ---------------------- | ------ | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `board`                | string | **Required** | The `name` of the [board](/components/board/) to which the device is wired.                                                                                                                                                                         |
| `spi`                  | string |              | The index of the SPI bus over which the device communicates with the board.                                                                                                                                                                         |
| `chip_select_pin`      | string | **Required** | The ({{< glossary_tooltip term_id="pin-number" text="pin number" >}}) of the pin on the board (other than the SPI bus pins) connected to the IMU chip. Used to tell the chip whether the current SPI message is meant for it or for another device. |
| `spi_baud_rate`        | int    | **Required** | The rate at which data is sent from the IMU. <br> Default: `115200`                                                                                                                                                                                 |
| `polling_frequency_hz` | int    | **Required** | How many times per second the sensor is polled.                                                                                                                                                                                                     |

{{< readfile "/static/include/components/test-control/movement-sensor-imu-control.md" >}}
