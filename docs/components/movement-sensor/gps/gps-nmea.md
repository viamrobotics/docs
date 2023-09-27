---
title: "Configure an NMEA-based GPS"
linkTitle: "gps-nmea"
weight: 10
type: "docs"
description: "Configure an NMEA-based GPS."
images: ["/icons/components/imu.svg"]
# SMEs: Rand
---

A global positioning system (GPS) receives signals from satellites in the earth’s orbit to determine where it is and how fast it is going.
All supported GPS models provide data for the `Position`, `CompassHeading` and `LinearVelocity` methods.
You can obtain fix and correction data by using the sensor `GetReadings` method, which is available because GPSes wrap the [sensor component](../../../sensor/).

The `gps-nmea` movement sensor model supports [NMEA-based](https://en.wikipedia.org/wiki/NMEA_0183) GPS units.

This GPS model uses communication standards set by the National Marine Electronics Association (NMEA).
The `gps-nmea` model can be connected using USB and send data through a serial connection to any device, or employ an I<sup>2</sup>C connection to a board:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `movement-sensor` type, then select the `gps-nmea` model.
Enter a name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/gps-nmea-builder.png" alt="Creation of a `gps-nmea` movement sensor in the Viam app config builder." resize="600x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "type": "movement_sensor",
      "model": "gps-nmea",
      "attributes": {
        "connection_type": "<serial|I2C>",
        "serial_attributes": {
            "serial_baud_rate": <int>,
            "serial_path": "<your-device-path>"
        },
        "i2c_attributes": {
            "board": "<your-board-name>",
            "i2c_baud_rate": <int>,
            "i2c_addr": <int>,
            "i2c_bus": "<name-of-bus-on-board>"
        },
        "disable_nmea": <boolean>
      },
      "depends_on": [],
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example: USB/Serial" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "my-gps-nmea",
      "type": "movement_sensor",
      "model": "gps-nmea",
      "attributes": {
        "connection_type": "serial",
        "serial_attributes": {
          "serial_baud_rate": 38400,
          "serial_path": "/dev/serial/by-path/<device_ID>"
        }
      },
      "depends_on": []
    }
  ]
}
```

Note that the example `"serial_path"` filepath is specific to serial devices connected to Linux systems.

{{% /tab %}}
{{% tab name="JSON Example: I2C" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "my-gps-nmea",
      "type": "movement_sensor",
      "model": "gps-nmea",
      "attributes": {
        "connection_type": "I2C",
        "i2c_attributes": {
          "board": "local",
          "i2c_baud_rate": 38400,
          "i2c_addr": 111,
          "i2c_bus": "1"
        }
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
| Name              | Type    | Inclusion    | Description  |
| ----------------- | ------- | ------------ | ---------------- |
| `connection_type` | string  | **Required** | `"I2C"` or `"serial"`. See [Connection Attributes](#connection-attributes) below. |
| `disable_nmea`    | boolean | Optional     | If set to `true`, changes the NMEA message protocol to RTCM when using a chip as a base station. <br> Default: `false` |

### Connection Attributes

You need to configure attributes to specify how the GPS connects to your computer.
You can use either serial communication (over USB) or I<sup>2</sup>C communication (through pins to a [board](../../../board/)).

Use `connection_type` to specify `"serial"` or `"I2C"` connection in the main `attributes` config.
Then create a struct within `attributes` for either `serial_attributes` or `i2c_attributes`, respectively.
See examples of this struct in the example tabs above.

{{< tabs >}}
{{% tab name="Serial" %}}

### Serial Config Attributes

For a movement sensor communicating over serial, you'll need to include a `serial_attributes` struct containing:

<!-- prettier-ignore -->
| Name               | Type   | Inclusion    | Description  |
| ------------------ | ------ | ------------ | ------------------------- |
| `serial_path`      | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyS0`, to its device file, such as <file>/dev/ttyS0</file>. If you omit this attribute, Viam will attempt to automatically detect the path. |
| `serial_baud_rate` | int    | Optional     | The rate at which data is sent from the sensor. <br> Default: `38400` |

{{% /tab %}}
{{% tab name="I2C" %}}

### I2C Config Attributes

For a movement sensor communicating over I<sup>2</sup>C, you'll need a `i2c_attributes` struct containing:

<!-- prettier-ignore -->
| Name            | Type   | Inclusion    | Description |
| --------------- | ------ | ------------ | ------------------------ |
| `board`         | string | **Required** | The `name` of the [board](/components/board/) to which the [I<sup>2</sup>C](/components/board/#i2cs) connection is being made. |
| `i2c_bus`       | string | **Required** | The name of the [I<sup>2</sup>C bus](/components/board/#i2cs) wired to the sensor. |
| `i2c_addr`      | int    | **Required** | The device's I<sup>2</sup>C address. |
| `i2c_baud_rate` | int    | Optional     | The rate at which data is sent from the sensor. Optional. <br> Default: `38400` |

{{% /tab %}}
{{< /tabs >}}

{{< readfile "/static/include/components/movement-sensor-control.md" >}}
