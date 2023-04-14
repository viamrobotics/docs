---
title: "Configure an NTRIP-based RTK GPS"
linkTitle: "gps-rtk"
weight: 10
type: "docs"
description: "Configure an NTRIP-based RTK GPS."
# SMEs: Rand
---

{{% alert title="Note" color="note" %}}

The `gps-rtk` model is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

{{% /alert %}}

The `gps-ntrip` movement sensor model supports [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [real time kinematic positioning (RTK)](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS units ([such as these](https://www.sparkfun.com/rtk)).

The chip requires a correction source to get to the required positional accuracy.
Our `gps-rtk` model uses an over-the-internet correction source [NTRIP](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) and sends the data over serial or I<sup>2</sup>C.

{{< tabs >}}
{{% tab name="Config Builder" %}}

On the **COMPONENTS** sub-tab, navigate to the **Create Component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `gps-rtk` model.

![Creation of a `gps-rtk` movement sensor in the Viam app config builder.](../../img/gps-rtk-builder.png)

Click **Create Component** and then fill in the attributes for your model.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <sensor_name>,
      "type": "movement_sensor",
      "model": "gps-rtk",
      "attributes": {
        "board": <board name if using I2C>,
        "connection_type": <"serial" or "I2C">,
        "serial_attributes": {
          "serial_baud_rate": <>,
          "serial_path": <>
        },
        "i2c_attributes": {
          "i2c_baud_rate": <>,
          "i2c_addr": <>,
          "i2c_bus": <>
        },
        "ntrip_attributes": {
          "ntrip_addr": <URL of NTRIP server>,
          "ntrip_baud": <>,
          "ntrip_password": <password for NTRIP server>,
          "ntrip_path": <>,
          "ntrip_username": <username for NTRIP server>
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
          "serial_path": "/dev/serial/by-path/<device_ID>"
        },
        "ntrip_attributes": {
          "ntrip_addr": "<ntrip_address>",
          "ntrip_baud": 38400,
          "ntrip_password": "<password>",
          "ntrip_username": "<username>"
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
          "I2c_bus": "<name_of_bus_on_board>",
        },
        "ntrip_attributes": {
          "ntrip_addr": "<ntrip_address>",
          "ntrip_baud": 38400,
          "ntrip_password": "<password>",
          "ntrip_username": "<username>"
        }
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

Name | Inclusion | Type | Default Value | Description
---- | --------- | ---- | ------------- | ----------
`board` | depends on connection type | string | - | Required for NMEA over I<sup>2</sup>C; the board connected to the chip. Not required for serial communication.
`connection_type` | **Required** | string | - | `"I2C"` or `"serial"`, respectively. See [connection configuration info](../connection/).
`ntrip_addr` | **Required** | string | - | The URL of the NTRIP server from which you get correction data. Connects to a base station (maintained by a third party) for RTK corrections
`ntrip_username` | **Required** | string | - | Username for the NTRIP server
`ntrip_password` | **Required** | string | - | Password for the NTRIP server
`ntrip_baud` | Optional | int | defaults to `serial_baud_rate`  | Only necessary if you want NTRIP baud rate to be different from serial baud rate.
`ntrip_connect_attempts` | Optional | int | 10 | How many times to attempt connection before timing out
`ntrip_mountpoint` | Optional | string | |
`ntrip_path` | Optional | string | |

You also need to configure either serial connection attributes or I<sup>2</sup>C connection attributes.
See [the connection configuration page](../connection/).
