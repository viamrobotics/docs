---
title: "Configure an NMEA-Based GPS"
linkTitle: "gps-nmea"
weight: 10
type: "docs"
description: "Configure an NMEA-based GPS on your machine. Once configured use the API to obtain the Position, CompassHeading and LinearVelocity."
images: ["/icons/components/imu.svg"]
aliases:
  - /components/movement-sensor/gps/gps-nmea/
# SMEs: Rand
---

A global positioning system (GPS) receives signals from satellites in the earth’s orbit to determine where it is and how fast it is going.
All supported GPS models provide data for the `Position`, `CompassHeading` and `LinearVelocity` methods.
You can obtain fix and correction data by using the sensor `GetReadings` method, which is available because GPSes wrap the [sensor component](/components/sensor/).

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

Copy and paste the following attribute template into your movement sensor's **Attributes** box.
Then remove and fill in the attributes as applicable to your movement sensor, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "connection_type": "<serial|I2C>",
  "serial_attributes": {
    "serial_path": "<your-device-path>",
    "serial_baud_rate": <int>
  },
  "i2c_attributes": {
    "i2c_bus": "<index-of-bus-on-board>",
    "i2c_addr": <int>,
    "i2c_baud_rate": <int>
  },
  "disable_nmea": <boolean>
}
```

{{% /tab %}}
{{% tab name="USB/serial attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "connection_type": "serial",
  "serial_attributes": {
    "serial_path": "/dev/serial/by-path/<device_ID>",
    "serial_baud_rate": 38400
  }
}
```

{{% /tab %}}
{{% tab name="I2c attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "connection_type": "I2C",
  "i2c_attributes": {
    "i2c_bus": "1",
    "i2c_addr": 111,
    "i2c_baud_rate": 38400
  }
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
      "model": "gps-nmea",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "connection_type": "<serial|I2C>",
        "serial_attributes": {
          "serial_path": "<your-device-path>",
          "serial_baud_rate": <int>
        },
        "i2c_attributes": {
            "i2c_bus": "<index-of-bus-on-board>",
            "i2c_addr": <int>,
            "i2c_baud_rate": <int>
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
      "model": "gps-nmea",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "connection_type": "serial",
        "serial_attributes": {
          "serial_path": "/dev/serial/by-path/usb-0:1.1:1.0",
          "serial_baud_rate": 38400
        }
      },
      "depends_on": []
    }
  ]
}
```

The `"serial_path"` filepath used in this example is specific to serial devices connected to Linux systems.
The `"serial_path"` filepath on a macOS system might resemble <file>"/dev/ttyUSB0"</file> or <file>"/dev/ttyS0"</file>.

{{% /tab %}}
{{% tab name="JSON Example: I2C" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "my-gps-nmea",
      "model": "gps-nmea",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "connection_type": "I2C",
        "i2c_attributes": {
          "i2c_bus": "1",
          "i2c_addr": 111,
          "i2c_baud_rate": 38400
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
You can use either serial communication (over USB) or I<sup>2</sup>C communication (through pins to a [board](/components/board/)).

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
| `serial_path` | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. To find your serial device path, first connect the serial device to your machine, then:<ul><li>On Linux, run <code>ls /dev/serial/by-path/\*</code> to show connected serial devices, or look for your device in the output of <code>sudo dmesg \| grep tty</code>. Example: <code>"/dev/serial/by-path/usb-0:1.1:1.0"</code>.</li><li>On macOS, run <code>ls /dev/tty\* \| grep -i usb</code> to show connected USB serial devices, <code>ls /dev/tty\*</code> to browse all devices, or look for your device in the output of <code>sudo dmesg \| grep tty</code>. Example: <code>"/dev/ttyS0"</code>.</li></ul> |
| `serial_baud_rate` | int    | Optional     | The rate at which data is sent from the sensor. <br> Default: `38400` |

{{% /tab %}}
{{% tab name="I2C" %}}

### I2C Config Attributes

For a movement sensor communicating over I<sup>2</sup>C, you'll need a `i2c_attributes` struct containing:

<!-- prettier-ignore -->
| Name            | Type   | Inclusion    | Description |
| --------------- | ------ | ------------ | ------------------------ |
| `i2c_bus`       | string | **Required** | The index of the I<sup>2</sup>C bus on the board wired to the sensor. |
| `i2c_addr`      | int    | **Required** | The device's I<sup>2</sup>C address. |
| `i2c_baud_rate` | int    | Optional     | The rate at which data is sent from the sensor. Optional. <br> Default: `38400` |

{{% /tab %}}
{{< /tabs >}}

{{< readfile "/static/include/components/test-control/movement-sensor-gps-control.md" >}}
