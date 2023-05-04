---
title: "Configure an NMEA-based GPS"
linkTitle: "gps-nmea"
weight: 10
type: "docs"
description: "Configure an NMEA-based GPS."
images: ["/components/img/components/imu.svg"]
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
Click on the **Components** sub-tab and navigate to the **Create component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `gps-nmea` model.

Click **Create Component**.

![Creation of a `gps-nmea` movement sensor in the Viam app config builder.](../../img/gps-nmea-builder.png)

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
        "board": "<your-board-name-if-using-I2C>",
        "serial_attributes": {
            "serial_baud_rate": <int>,
            "serial_path": "<your-device-path>"
        },
        "i2c_attributes": {
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
          "serial_baud_rate": 115200,
          "serial_path": "/dev/serial/by-path/<device_ID>"
        }
      },
      "depends_on": [],
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
        "board": "local",
        "connection_type": "I2C",
        "i2c_attributes": {
          "i2c_baud_rate": 115200,
          "i2c_addr": 111,
          "i2c_bus": "<name_of_bus_on_board>"
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
`connection_type` | **Required** | string |`"I2C"` or `"serial"`. See [connection configuration info](#connection-attributes).
`board` | depends on connection type | string | The `name` of the [board](/components/board) connected to the chip. Required for NMEA over [I<sup>2</sup>C](/components/board/#i2cs). Not required for serial communication.
`disable_nmea` | Optional | bool | If set to `true`, changes the NMEA message protocol to RTCM when using a chip as a base station. <br> Default: `false`

### Connection Attributes

{{< readfile "/static/include/components/movement-sensor/connection.md" >}}
