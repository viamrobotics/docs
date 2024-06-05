---
title: "Configure a WitMotion IMU"
linkTitle: "imu-wit"
weight: 10
type: "docs"
description: "Configure a WitMotion IMU on your machine. Once configured use the API to obtain the AngularVelocity, Orientation, CompassHeading and LinearAcceleration."
images: ["/icons/components/imu.svg"]
aliases:
  - "/components/movement-sensor/imu/imu-wit/"
component_description: "Other IMUs manufactured by WitMotion: BWT61CL, BWT901CL, and HWT901B-TTL."
# SMEs: Rand
---

An [inertial measurement unit (IMU)](https://en.wikipedia.org/wiki/Inertial_measurement_unit) provides data for the [`AngularVelocity`](/components/movement-sensor/#getangularvelocity), [`Orientation`](/components/movement-sensor/#getorientation), [`CompassHeading`](/components/movement-sensor/#getcompassheading), [`LinearAcceleration`](/components/movement-sensor/#getlinearacceleration), and [`GetAccuracy`](/components/movement-sensor/#getaccuracy) methods.
Acceleration and magnetometer data are available by using the [sensor](/components/sensor/) [`GetReadings`](/components/sensor/#getreadings) method, which IMUs wrap.

The `imu-wit` movement sensor model supports the following IMUs manufactured by [WitMotion](https://www.wit-motion.com/):

- BWT61CL
- BWT901CL
- HWT901B-TTL

{{% alert title="Info" color="info" %}}

Other WitMotion IMUs that communicate over serial may also work with this model but have not been tested.

If you are using WitMotion's HWT905 IMU, configure an [`imu-wit-hwt905`](../imu-wit-hwt905/).

{{% /alert %}}

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `movement-sensor` type, then select the `imu-wit` model.
Enter a name or use the suggested name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/imu-wit-builder.png" alt="Creation of an `imu-wit` movement sensor in the Viam app config builder." resize="1200x" style="width:650px" >}}

Then fill in the attributes as applicable to your movement sensor, according to the table below.

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
        "serial_path": "/dev/serial/by-path/usb-0:1.1:1.0",
        "serial_baud_rate": 115200
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

## Attributes

<!-- prettier-ignore -->
| Name  | Type   | Inclusion    | Description |
| -------------- | ------ | ----------- | ----------- |
| `serial_path` | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. To find your serial device path, first connect the serial device to your machine, then:<ul><li>On Linux, run <code>ls /dev/serial/by-path/\*</code> to show connected serial devices, or look for your device in the output of <code>sudo dmesg \| grep tty</code>. Example: <code>"/dev/serial/by-path/usb-0:1.1:1.0"</code>.</li><li>On macOS, run <code>ls /dev/tty\* \| grep -i usb</code> to show connected USB serial devices, <code>ls /dev/tty\*</code> to browse all devices, or look for your device in the output of <code>sudo dmesg \| grep tty</code>. Example: <code>"/dev/ttyS0"</code>.</li></ul> |
| `serial_baud_rate` | int | Optional | The rate at which data is sent from the sensor over the serial connection. Valid rates are `9600` and `115200`. The default rate will work for all models. _Only the HWT901B can have a different serial baud rate._ Refer to your model's data sheet. <br>Default: `115200` |

{{< readfile "/static/include/components/test-control/movement-sensor-imu-control.md" >}}
