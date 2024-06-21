---
title: "Configure a VectorNav IMU"
linkTitle: "imu-vectornav"
weight: 10
type: "docs"
description: "Configure a VectorNav IMU."
images: ["/icons/components/imu.svg"]
toc_hide: true
draft: true
aliases:
  - "/components/movement-sensor/imu/imu-vectornav/"
# SMEs: Rand
---

An [inertial measurement unit (IMU)](https://en.wikipedia.org/wiki/Inertial_measurement_unit) provides data for the [`AngularVelocity`](/components/movement-sensor/#getangularvelocity), [`Orientation`](/components/movement-sensor/#getorientation), [`CompassHeading`](/components/movement-sensor/#getcompassheading), and [`LinearAcceleration`](/components/movement-sensor/#getlinearacceleration) methods.
Acceleration and magnetometer data are available by using the [sensor](/components/sensor/) [`GetReadings`](/components/sensor/#getreadings) method, which IMUs wrap.

The `imu-vectornav` movement sensor model supports IMUs manufactured by [VectorNav](https://www.vectornav.com/products) that support SPI connection.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `movement-sensor` type, then select the `imu-vectornav` model.
Enter a name or use the suggested name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/imu-vectornav-builder.png" alt="Creation of an `imu-vectornav` movement sensor in the Viam app config builder." resize="1200x" style="width:650px" >}}

Fill in the attributes as applicable to your movement sensor, according to the table below.

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
        "spi_bus": "<your-spi-bus-name-on-board>",
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
        "spi_bus": "1",
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

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | The `name` of the [board](/components/board/) to which the device is wired. |
| `spi_bus` | string | **Required** | The index of the SPI bus over which the device communicates with the board. |
| `chip_select_pin` | string | **Required** | The ({{< glossary_tooltip term_id="pin-number" text="pin number" >}}) of the pin on the board (other than the SPI bus pins) connected to the IMU chip. Used to tell the chip whether the current SPI message is meant for it or for another device. |
| `spi_baud_rate` | int | **Required** | The rate at which data is sent from the IMU. <br> Default: `115200` |
| `polling_frequency_hz` | int | **Required** | How many times per second the sensor is polled. |

{{< readfile "/static/include/components/test-control/movement-sensor-imu-control.md" >}}
