---
title: "Configure a WitMotion IMU"
linkTitle: "imu-wit"
weight: 10
type: "docs"
description: "Configure a WitMotion IMU."
images: ["/icons/components/imu.svg"]
# SMEs: Rand
---

An [inertial measurement unit (IMU)](https://en.wikipedia.org/wiki/Inertial_measurement_unit) provides data for the `AngularVelocity`, `Orientation`, `CompassHeading`, and `LinearAcceleration` methods.
Acceleration and magnetometer data are available by using the [sensor](../../../sensor/) `GetReadings` method, which IMUs wrap.

The `imu-wit` movement sensor model supports the following IMUs manufactured by [WitMotion](https://www.wit-motion.com/):

- [BWT61CL](https://www.wit-motion.com/6-axis/witmotion-bluetooth-2-0.html)
- [BWT901CL](https://www.wit-motion.com/9-axis/witmotion-bluetooth-2-0-mult.html)
- [HWT901B TTL](https://www.wit-motion.com/10-axis/witmotion-hwt901b-ttl-10.html)

{{% alert title="Info" color="info" %}}

Other WitMotion IMUs that communicate over serial may also work with this model but have not been tested.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `movement-sensor` type, then select the `imu-wit` model.
Enter a name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/imu-wit-builder.png" alt="Creation of an `imu-wit` movement sensor in the Viam app config builder." resize="600x" >}}

Copy and paste the following attribute template into your movement sensor's **Attributes** box.
Then remove and fill in the attributes as applicable to your movement sensor, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "serial_path": "<your-port>",
  "serial_baud_rate": <int>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "serial_path": "/dev/serial/by-path/<device_ID>",
  "serial_baud_rate": 9600
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
      "model": "imu-wit",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "serial_path": "<your-port>",
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
      "model": "imu-wit",
      "type": "movement_sensor",
      "namespace": "rdk",
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

| Name               | Type   | Inclusion    | Description                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------ | ------ | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `serial_path`      | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyS0`, to its device file, such as <file>/dev/ttyS0</file>. If you omit this attribute, Viam will attempt to automatically detect the path. |
| `serial_baud_rate` | int    | Optional     | The rate at which data is sent from the sensor over the serial connection. Valid rates are `9600` and `115200`. The default rate will work for all models. _Only the HWT901B can have a different serial baud rate._ Refer to your model's data sheet. <br>Default: `115200`                                                                                                                             |

{{< readfile "/static/include/components/test-control/movement-sensor-imu-control.md" >}}
