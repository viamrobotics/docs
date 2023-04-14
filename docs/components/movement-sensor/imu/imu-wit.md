---
title: "Configure a WitMotion IMU"
linkTitle: "imu-wit"
weight: 10
type: "docs"
description: "Configure a WitMotion IMU."
# SMEs: Rand
---

The `imu-wit` movement sensor model supports IMUs manufactured by [WitMotion](https://witmotion-sensor.com/).

{{< tabs >}}
{{% tab name="Config Builder" %}}

On the **COMPONENTS** sub-tab, navigate to the **Create Component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `imu-wit` model.

![Creation of an `imu-wit` movement sensor in the Viam app config builder.](../../img/imu-wit-builder.png)

Click **Create Component** and then fill in the attributes for your model.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <sensor_name>,
      "type": "movement_sensor",
      "model": "imu-wit",
      "attributes": {
        "serial_path": <string>,
        "serial_baud_rate": <int>
      },
      "depends_on": []
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
      "name": "myIMU",
      "type": "movement_sensor",
      "model": "imu-wit",
      "attributes": {
        "serial_path": "/dev/serial/by-path/<device_ID>",
        "serial_baud_rate": 115200
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

Name | Type | Default Value | Description
---- | ---- | ------------- | -----
`serial_path` | string | - | The name of the port through which the sensor communicates with the computer.
`serial_baud_rate` | int | 115200 | The rate at which data is sent from the sensor. Optional.
