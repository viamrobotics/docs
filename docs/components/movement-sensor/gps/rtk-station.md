---
title: "Configure an RTK GPS Correction Source"
linkTitle: "rtk-station"
weight: 10
type: "docs"
description: "Configure an experimental RTK correction source to use with an RTK-ready GPS."
images: ["/components/img/components/imu.svg"]
# SMEs: Rand
---

{{% alert title="Note" color="note" %}}

The `rtk-station` model is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

{{% /alert %}}

The `rtk-station` movement sensor model is an **experimental** model that you can use to configure your own correction source for an RTK-ready GPS.

The experimental `rtk-station` model allows you to configure your own correction source.
This does not provide any movement sensor data on its own, but can be linked to an RTK-ready GPS module on a moving robot and send that robot correction data over your own network, radio, or Bluetooth in areas where internet connectivity is limited, or where an NTRIP server is unavailable.
We have implemented this in a way that does not rely on an internet connection to get correction data for a moving GPS.

For all of the following RTK-station configurations, `children` is the list of one or more other GPS components that can take RTCM corrections.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** sub-tab and navigate to the **Create component** menu.

Enter a name for your movement sensor, select the `movement-sensor` type, and select the `rtk-station` model.

![Creation of a `rtk-station` movement sensor in the Viam app config builder.](../../img/rtk-station-builder.png)

Click **Create Component** and then fill in the attributes for your model.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <sensor_name>,
      "type": "movement_sensor",
      "model": "rtk-station",
      "attributes": {
        "board": <board_name>,
        "children": [
          <list of children>
        ],
        "connection_type": "<serial" or "I2C>",
        "i2c_attributes": {
          "i2c_baud_rate": <>,
          "i2c_addr": <>,
          "i2c_bus": <>
        },
        "ntrip_attributes": {
          "ntrip_addr": <>,
          "ntrip_baud": <>,
          "ntrip_password": <>,
          "ntrip_path": <>,
          "ntrip_username": <>
        },
        "serial_attributes": {
          "serial_baud_rate": <>,
          "serial_path": <>
        },
        "correction_source": <string>,
        // non-NTRIP attributes:
        "svin": <string>, //SurveyIn
        "required_accuracy": <float64>,
        "required_time_sec": <int>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example: NTRIP" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "my-rtk-station",
    "type": "movement_sensor",
    "model": "rtk-station",
    "children": [
        "gps1"
    ],
    "attributes": {
        "connection_type": "serial",
        "ntrip_attributes": {
            "ntrip_addr": "<NTRIP_address>",
            "ntrip_baud": 38400,
            "ntrip_password": "<password>",
            "ntrip_path": "",
            "ntrip_username": "<username>"
        },
        "correction_source": "ntrip"
    }
}
```

{{% /tab %}}
{{% tab name="JSON Example: I2C" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "my-rtk-station",
    "type": "movement_sensor",
    "model": "rtk-station",
    "children": [
        "gps1"
    ],
    "attributes": {
        "board": "board",
        "connection_type": "serial",
        "i2c_attributes": {
            "i2c_baud_rate": 115200,
            "i2c_addr": 111,
            "i2c_bus": "<name_of_bus_on_board>",
       },
        "correction_source": "I2C",
        "loc_accuracy": 10,
        "svin": "time",
        "time_accuracy": 60
    }
}
```

{{% /tab %}}
{{% tab name="JSON Example: Serial/USB" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "my-rtk-station",
    "type": "movement_sensor",
    "model": "rtk-station",
    "children": [
        "gps1"
    ],
    "attributes": {
        "connection_type": "serial",
        "serial_attributes": {
            "serial_baud_rate": 115200,
            "serial_path": "/dev/serial/by-path/<device_ID>"
        },
        "correction_source": "serial"
    }
}
```

{{% /tab %}}
{{< /tabs >}}

Find NTRIP and configuration attribute information in the [GPS-RTK documentation](../gps-rtk/#attributes).
