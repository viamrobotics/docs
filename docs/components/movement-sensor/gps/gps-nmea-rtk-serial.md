---
title: "Configure an NTRIP-based RTK GPS with a Serial Connection"
linkTitle: "gps-nmea-rtk-serial"
weight: 10
type: "docs"
description: "Configure an NTRIP-based RTK that uses serial communication."
images: ["/icons/components/imu.svg"]
aliases:
  - "/components/movement-sensor/gps/gps-rtk/"
# SMEs: Susmita
---


{{% alert title="Stability Notice" color="note" %}}

The `gps-nmea-rtk-serial` model is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

{{% /alert %}}

A global positioning system (GPS) receives signals from satellites in the earth’s orbit to determine where it is and how fast it is going.
All supported GPS models provide data for the `Position`, `CompassHeading` and `LinearVelocity` methods.
You can obtain fix and correction data by using the sensor `GetReadings` method, which is available because GPSes wrap the [sensor component](../../../sensor/).

The `gps-nmea-rtk-serial` and [`gps-nmea-rtk-pmtk`](../gps-nmea-rtk-pmtk/) movement sensor models support [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [real time kinematic positioning (RTK)](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS units ([such as these](https://www.sparkfun.com/rtk)).

The chip requires a correction source to get to the required positional accuracy.
The `gps-nmea-rtk-serial` model uses an over-the-internet correction source and sends the data over a serial connection to the [board](/components/board/).

{{% alert title="Tip" color="tip" %}}

If your movement sensor uses I<sup>2</sup> communication instead of serial, use the [`gps-nmea-rtk-pmtk`](../gps-nmea-rtk-pmtk/) model.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `gps-nmea-rtk-serial` model.

Click **Create Component**.

{{< imgproc src="/components/movement-sensor/gps-nmea-rtk-serial-builder.png" alt="Creation of a `gps-nmea-rtk-serial` movement sensor in the Viam app config builder." resize="600x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "type": "movement_sensor",
      "model": "gps-nmea-rtk-serial",
      "attributes": {
        "board": "<your-board-name>",
        "serial_path": "<path_to_serial_port>",
        "serial_baud_rate": <int>,
        "ntrip_connect_attempts": <int>,
        "ntrip_mountpoint": "<identifier>",
        "ntrip_password": "<password for NTRIP server>",
        "ntrip_url": "<URL of NTRIP server>",
        "ntrip_username": "<username for NTRIP server>"
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
      "model": "gps-nmea-rtk-serial",
      "attributes": {
        "board": "local",
        "serial_path": "/dev/ttyS0",
        "serial_baud_rate": 115200,
        "ntrip_connect_attempts": 12,
        "ntrip_mountpoint": "MNTPT",
        "ntrip_password": "pass",
        "ntrip_url": "http://ntrip/url",
        "ntrip_username": "usr"
      },
      "depends_on": [],
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for a `gps-nmea-rtk-pmtk` movement sensor:

Name | Type | Inclusion | Description |
---- | ---- | --------- | ----------- |
`board` | string | **Required** | The `name` of the [board](/components/board/) connected to the sensor.
`serial_path` | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyS0`, to its device file, such as <file>/dev/ttyS0</file>. If you omit this attribute, Viam will attempt to automatically detect the path.
`serial_baud_rate` | int | Optional | The rate at which data is sent from the sensor. <br> Default: `38400`
`ntrip_url` | string | **Required** | The URL of the NTRIP server from which you get correction data. Connects to a base station (maintained by a third party) for RTK corrections.
`ntrip_username` | string | Optional | Username for the NTRIP server.
`ntrip_password` | string | Optional | Password for the NTRIP server.
`ntrip_connect_attempts` | int | Optional | How many times to attempt connection before timing out. <br> Default: `10`
`ntrip_mountpoint` | string | Optional | If you know of an RTK mountpoint near you, write its identifier here. It will be appended to NTRIP address string (for example, "nysnet.gov/rtcm/**NJMTPT1**") and that mountpoint's data will be used for corrections.
