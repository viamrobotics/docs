---
title: "Configure an NTRIP-based RTK GPS"
linkTitle: "gps-rtk"
weight: 10
type: "docs"
description: "Configure an NTRIP-based RTK GPS."
images: ["/components/img/components/imu.svg"]
# SMEs: Rand
---

{{% alert title="Note" color="note" %}}

The `gps-rtk` model is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

{{% /alert %}}

A global positioning system (GPS) receives signals from satellites in the earth’s orbit to determine where it is and how fast it is going.
All supported GPS models provide data for the `Position`, `CompassHeading` and `LinearVelocity` methods.
You can obtain fix and correction data by using the sensor `GetReadings` method, which is available because GPSes wrap the [sensor component](../../../sensor/).

The `gps-ntrip` movement sensor model supports [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [real time kinematic positioning (RTK)](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS units ([such as these](https://www.sparkfun.com/rtk)).

The chip requires a correction source to get to the required positional accuracy.
Our `gps-rtk` model uses an over-the-internet correction source [NTRIP](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) and sends the data over serial or I<sup>2</sup>C.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** sub-tab and navigate to the **Create component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `gps-rtk` model.

Click **Create Component**.

![Creation of a `gps-rtk` movement sensor in the Viam app config builder.](../../img/gps-rtk-builder.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "type": "movement_sensor",
      "model": "gps-rtk",
      "attributes": {
        "board": "<your-board-name-if-using-I2C>",
        "connection_type": "<serial|I2C>",
        "serial_attributes": {
          "serial_baud_rate": <int>,
          "serial_path": "<your-device-path>"
        },
        "i2c_attributes": {
          "i2c_baud_rate": <int>,
          "i2c_addr": <int>,
          "i2c_bus": "<name-of-bus-on-board>"
        },
        "ntrip_attributes": {
          "ntrip_addr": "<URL of NTRIP server>",
          "ntrip_baud": <int>,
          "ntrip_password": "<password for NTRIP server>",
          "ntrip_path": "<your-device-path>",
          "ntrip_username": "<username for NTRIP server>"
        }
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
      "name": "my_GPS",
      "type": "movement_sensor",
      "model": "gps-rtk",
      "attributes": {
        "connection_type": "serial",
        "correction_source": "ntrip",
        "serial_attributes": {
          "serial_baud_rate": 115200,
          "serial_path": "/dev/serial/by-path/12335"
        },
        "ntrip_attributes": {
          "ntrip_addr": "ntrip_address",
          "ntrip_baud": 38400,
          "ntrip_password": "password",
          "ntrip_username": "username"
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
      "name": "my_GPS",
      "type": "movement_sensor",
      "model": "gps-rtk",
      "attributes": {
        "board": "board",
        "connection_type": "I2C",
        "correction_source": "ntrip",
        "i2c_attributes": {
          "i2c_baud_rate": 115200,
          "i2c_addr": 111,
          "I2c_bus": "main",
        },
        "ntrip_attributes": {
          "ntrip_addr": "ntrip_address",
          "ntrip_baud": 38400,
          "ntrip_password": "password",
          "ntrip_username": "username"
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

Name | Inclusion | Type | Description |
---- | --------- | ---- | ----------- |
`board` | depends on connection type | string | Required for NMEA over [I<sup>2</sup>C](/components/board/#i2cs); the `name` of the [board](/components/board) connected to the chip. Not required for serial communication.
`connection_type` | **Required** | string |`"I2C"` or `"serial"`, respectively. See [connection configuration info](#connection-attributes).
`ntrip_addr` | **Required** | string | The URL of the NTRIP server from which you get correction data. Connects to a base station (maintained by a third party) for RTK corrections
`ntrip_username` | **Required** | string | Username for the NTRIP server
`ntrip_password` | **Required** | string | Password for the NTRIP server
`ntrip_baud` | Optional | int | defaults to `serial_baud_rate`  | Only necessary if you want NTRIP baud rate to be different from serial baud rate.
`ntrip_connect_attempts` | Optional | int | 10 | How many times to attempt connection before timing out
`ntrip_mountpoint` | Optional | string | If you know of an RTK mountpoint near you, write its identifier here. It will be appended to NTRIP address string (for example, "nysnet.gov/rtcm/**NJMTPT1**") and that mountpoint's data will be used for corrections.
`ntrip_path` | Optional | string | Use this when extra hardware is piping RTCM data through a second USB port on an [board](/components/board) instead of getting it directly from the internet.

### Connection Attributes

{{< readfile "/static/include/components/movement-sensor/connection.md" >}}
