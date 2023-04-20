---
title: "Configure an NMEA-based GPS"
linkTitle: "gps-nmea"
weight: 10
type: "docs"
description: "Configure an NMEA-based GPS."
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

On the **COMPONENTS** sub-tab, navigate to the **Create Component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `gps-nmea` model.

![Creation of a `gps-nmea` movement sensor in the Viam app config builder.](../../img/gps-nmea-builder.png)

Click **Create Component** and then fill in the attributes for your model.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <sensor_name>,
      "type": "movement_sensor",
      "model": "gps-nmea",
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
            "i2c_bus": "<name_of_bus_on_board>"
        },
        "disable_nmea": <>
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

Name | Inclusion | Type | Default Value | Description
---- | --------- | ---- | ------------- | -----
`board` | depends on connection type | string | - | Required for NMEA over I<sup>2</sup>C; the board connected to the chip. Not required for serial communication.
`connection_type` | **Required** | string | - | `"I2C"` or `"serial"`. See [connection configuration info](#connection-attributes).
`disable_nmea` | Optional | bool | false | If set to true, changes the NMEA message protocol to RTCM when using a chip as a base station.

### Connection Attributes

{{< readfile "/static/include/components/movement-sensor/connection.md" >}}
