---
title: "Configure an NTRIP-based RTK GPS with an I2C Connection"
linkTitle: "gps-nmea-rtk-pmtk"
weight: 10
type: "docs"
description: "Configure an NTRIP-based RTK GPS."
images: ["/icons/components/imu.svg"]
# SMEs: Susmita
---

{{% alert title="Stability Notice" color="note" %}}

The `gps-nmea-rtk-pmtk` model is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

{{% /alert %}}

A global positioning system (GPS) receives signals from satellites in the earth’s orbit to determine where it is and how fast it is going.
All supported GPS models provide data for the `Position`, `CompassHeading` and `LinearVelocity` methods.
You can obtain fix and correction data by using the sensor `GetReadings` method, which is available because GPSes wrap the [sensor component](../../../sensor/).

The `gps-ntrip` <!-- this isn't a model. What should this say? --> movement sensor model supports [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [real time kinematic positioning (RTK)](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS units ([such as these](https://www.sparkfun.com/rtk)).

The chip requires a correction source to get to the required positional accuracy.
The `gps-nmea-rtk-pmtk` model uses an over-the-internet correction source and sends the data over I<sup>2</sup>C.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `gps-rtk` model.

Click **Create Component**.

{{< imgproc src="/components/movement-sensor/gps-rtk-builder.png" alt="Creation of a `gps-rtk` movement sensor in the Viam app config builder." resize="600x" >}}

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
{{% tab name="JSON Example" %}}

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

The following attributes are available for a `gps-nmea-rtk-pmtk` movement sensor:

Name | Type | Inclusion | Description |
---- | ---- | --------- | ----------- |
`board` | string | **Required** | The `name` of the [board](/components/board/) connected to the sensor with [I<sup>2</sup>C](/components/board/#i2cs).
`i2c_addr` | int | **Required** | The device's I<sup>2</sup>C address.
`i2c_bus` | string | **Required** | The name of the [I<sup>2</sup>C bus](/components/board/#i2cs) wired to the sensor.
`i2c_baud_rate` | int | Optional | The rate at which data is sent from the sensor. Optional. <br> Default: `38400`
`ntrip_url` | string | **Required** | The URL of the NTRIP server from which you get correction data. Connects to a base station (maintained by a third party) for RTK corrections
`ntrip_username` | string | Optional | Username for the NTRIP server
`ntrip_password` | string | Optional | Password for the NTRIP server
`ntrip_baud` | int | Optional | defaults to `serial_baud_rate`  | Only necessary if you want NTRIP baud rate to be different from serial baud rate.
`ntrip_connect_attempts` | int | Optional | How many times to attempt connection before timing out. <br> Default: `10`
`ntrip_mountpoint` | string | Optional | If you know of an RTK mountpoint near you, write its identifier here. It will be appended to NTRIP address string (for example, "nysnet.gov/rtcm/**NJMTPT1**") and that mountpoint's data will be used for corrections.

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<my-movement-sensor-name>",
    "type": "<TYPE>",
    "model": "<MODEL>",
    "attributes": {
        "<whatever other attributes>": "<example>",
        "connection_type": "I2C",
        // "board": "<name of your board>"  Include if "model": "gps-rtk"
        "i2c_attributes": {
            "i2c_addr": 111,
            "i2c_bus": "1",
            // "board": "<name of your board>"  Include if "model": "gps-nmea"
        }
    }
}
```
