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

The `imu-wit` movement sensor model supports the following IMUs manufactured by [WitMotion](https://witmotion-sensor.com/):

- [BWT61CL](https://witmotion-sensor.com/products/bluetooth-accelerometer-inclinometer-bwt61cl-mpu6050-high-precision-6-axis-gyroscope-anglexy-0-05-accuracy-acceleration-with-kalman-filter-100hz-high-stability-6dof-data-logger-for-arduino?_pos=2&_sid=34ad342de&_ss=r&variant=40749736689861)
- [BWT901CL](https://witmotion-sensor.com/products/bluetooth-accelerometer-inclinometer-bwt901cl-mpu9250-high-precision-9-axis-gyroscope-anglexy-0-05-accuracy-magnetometer-with-kalman-filter-200hz-high-stability-3-axis-imu-sensor-for-arduino?_pos=1&_sid=68bf26406&_ss=r&variant=40580102226117)
- [HWT901B TTL](https://witmotion-sensor.com/products/military-grade-accelerometer-inclinometer-hwt901b-mpu9250-9-axis-gyroscope-anglexy-0-05-accuracy-digital-compass-air-pressure-altitude-rm3100-magnetometer-compensation-and-kalman-filtering?_pos=1&_sid=dfbf7e412&_ss=r)

{{% alert title="Info" color="info" %}}

Other WitMotion IMUs that communicate over serial may also work with this model but have not been tested.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your movement sensor, select the `movement-sensor` type, and select the `imu-wit` model.

Click **Create Component**.

{{< imgproc src="/components/movement-sensor/imu-wit-builder.png" alt="Creation of an `imu-wit` movement sensor in the Viam app config builder." resize="600x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "type": "movement_sensor",
      "model": "imu-wit",
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

Name | Type | Inclusion | Description
---- | ---- | --------- | -----------
`serial_path` | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyAMA0` , to its device file, such as <file>/dev/ttyAMA0</file>. On a Raspberry Pi, you can also run `ls /dev/serial/by-path` to list USB serial ports. If you omit this attribute, Viam will attempt to automatically detect the path.<br>Example: `"/dev/serial/by-path/usb-0:1.1:1.0"`
`serial_baud_rate` | int | Optional | The rate at which data is sent from the sensor over the serial connection. Valid rates are `9600` and `115200`. The default rate will work for all models. *Only the HWT901B can have a different serial baud rate.* Refer to your model's data sheet. <br>Default: `115200`
