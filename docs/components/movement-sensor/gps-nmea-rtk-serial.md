---
title: "Configure NTRIP-Based RTK GPS with Serial Connection"
linkTitle: "gps-nmea-rtk-serial"
weight: 10
type: "docs"
description: "Configure an NTRIP-based RTK that uses serial communication."
images: ["/icons/components/imu.svg"]
toc_hide: true
aliases:
  - "/components/movement-sensor/gps/gps-rtk/"
  - "/components/movement-sensor/gps/gps-nmea-rtk-serial/"
component_description: "NTRIP-based RTK GPS models using serial communication (experimental)."
# SMEs: Susmita
---

{{% alert title="Stability Notice" color="note" %}}

The `gps-nmea-rtk-serial` model is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

{{% /alert %}}

A global positioning system (GPS) receives signals from satellites in the earth’s orbit to determine where it is and how fast it is going.
All supported GPS models provide data for the [`Position`](/components/movement-sensor/#getposition), [`CompassHeading`](/components/movement-sensor/#getcompassheading), [`LinearVelocity`](/components/movement-sensor/#getlinearvelocity), and [`GetAccuracy`](/components/movement-sensor/#getaccuracy) methods.
You can obtain fix and correction data by using the sensor [`GetReadings`](/components/sensor/#getreadings) method, which is available because GPSes wrap the [sensor component](/components/sensor/).

The `gps-nmea-rtk-serial` and [`gps-nmea-rtk-pmtk`](../gps-nmea-rtk-pmtk/) movement sensor models support [NTRIP-based](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) [real time kinematic positioning (RTK)](https://en.wikipedia.org/wiki/Real-time_kinematic_positioning) GPS units ([such as these](https://www.sparkfun.com/rtk)).

The chip requires a correction source to get to the required positional accuracy.
The `gps-nmea-rtk-serial` model uses an over-the-internet correction source like an RTK reference station and sends the data over a serial connection to the [board](/components/board/).

Follow the guide to [Set up a SparkFun RTK Reference Station](/components/movement-sensor/set-up-base-station/) to configure a SparkFun station for use with this RTK-enabled GPS movement sensor model.

{{% alert title="Tip" color="tip" %}}

If your movement sensor uses I<sup>2</sup>C communication instead of serial, use the [`gps-nmea-rtk-pmtk`](../gps-nmea-rtk-pmtk/) model.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `movement-sensor` type, then select the `gps-nmea-rtk-serial` model.
Enter a name or use the suggested name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/gps-nmea-rtk-serial-builder.png" alt="Creation of a `gps-nmea-rtk-serial` movement sensor in the Viam app config builder." resize="1200x" style="width:650px" >}}

Fill in the attributes as applicable to your movement sensor, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "model": "gps-nmea-rtk-serial",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
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
      "model": "gps-nmea-rtk-serial",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "serial_path": "/dev/serial/by-path/usb-0:1.1:1.0",
        "serial_baud_rate": 115200,
        "ntrip_connect_attempts": 12,
        "ntrip_mountpoint": "MNTPT",
        "ntrip_password": "pass",
        "ntrip_url": "http://ntrip/url",
        "ntrip_username": "usr"
      },
      "depends_on": []
    }
  ]
}
```

The `"serial_path"` filepath used in this example is specific to serial devices connected to Linux systems.
The `"serial_path"` filepath on a macOS system might resemble <file>"/dev/ttyUSB0"</file> or <file>"/dev/ttyS0"</file>.

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for a `gps-nmea-rtk-pmtk` movement sensor:

<!-- prettier-ignore -->
| Name                     | Type   | Required? | Description |
| ------------------------ | ------ | ------------ | ---------------- |
| `serial_path`            | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. To find your serial device path, first connect the serial device to your machine, then:<ul><li>On Linux, run <code>ls /dev/serial/by-path/\*</code> to show connected serial devices, or look for your device in the output of <code>sudo dmesg \| grep tty</code>. Example: <code>"/dev/serial/by-path/usb-0:1.1:1.0"</code>.</li><li>On macOS, run <code>ls /dev/tty\* \| grep -i usb</code> to show connected USB serial devices, <code>ls /dev/tty\*</code> to browse all devices, or look for your device in the output of <code>sudo dmesg \| grep tty</code>. Example: <code>"/dev/ttyS0"</code>.</li></ul> |
| `serial_baud_rate`       | int    | Optional     | The rate at which data is sent from the sensor. <br> Default: `38400` |
| `ntrip_url`              | string | **Required** | The URL of the NTRIP server from which you get correction data. Connects to a base station (maintained by a third party) for RTK corrections. |
| `ntrip_username`         | string | Optional     | Username for the NTRIP server. |
| `ntrip_password`         | string | Optional     | Password for the NTRIP server. |
| `ntrip_connect_attempts` | int    | Optional     | How many times to attempt connection before timing out. <br> Default: `10` |
| `ntrip_mountpoint`       | string | Optional     | If you know of an RTK mountpoint near you, write its identifier here. It will be appended to NTRIP address string (for example, "nysnet.gov/rtcm/**NJMTPT1**") and that mountpoint's data will be used for corrections. |

{{% alert title="Tip" color="tip" %}}

How you connect your device to an NTRIP server varies by geographic region.
You will need to research the options available to you.
If you are not sure where to start, check out this [GPS-RTK2 Hookup Guide from SparkFun](https://learn.sparkfun.com/tutorials/gps-rtk2-hookup-guide/connecting-the-zed-f9p-to-a-correction-source).

{{% /alert %}}

{{< readfile "/static/include/components/test-control/movement-sensor-gps-control.md" >}}
