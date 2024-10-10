---
title: "Configure a WitMotion HWT905-TTL IMU"
linkTitle: "imu-wit-hwt905"
weight: 10
type: "docs"
description: "Configure a WitMotion HWT905-TTL IMU on your machine. Once configured, use the API to obtain the AngularVelocity, Orientation, CompassHeading and LinearAcceleration."
images: ["/icons/components/imu.svg"]
toc_hide: true
component_description: "Supports the HWT905-TTL IMU manufactured by WitMotion."
aliases:
  - "/components/movement-sensor/imu/imu-wit-hwt905/"
# SMEs: Susmita, Bucket Team
---

An [inertial measurement unit (IMU)](https://en.wikipedia.org/wiki/Inertial_measurement_unit) provides data for the [`AngularVelocity`](/appendix/apis/components/movement-sensor/#getangularvelocity), [`Orientation`](/appendix/apis/components/movement-sensor/#getorientation), [`CompassHeading`](/appendix/apis/components/movement-sensor/#getcompassheading), [`LinearAcceleration`](/appendix/apis/components/movement-sensor/#getlinearacceleration), and [`GetAccuracy`](/appendix/apis/components/movement-sensor/#getaccuracy) methods.
To get all the raw sensor data, you can use the [sensor](/components/sensor/) [`GetReadings`](/appendix/apis/components/sensor/#getreadings) method, which movement sensors inherit from the general sensor API.

The `imu-wit-hwt905` movement sensor model supports the [HWT905-TTL IMU](https://www.wit-motion.com/proztgjd/39.html) manufactured by WitMotion.

Make sure to physically connect your movement sensor to your machine's computer and turn it on.
Then, configure the movement sensor:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `movement-sensor` type, then select the `imu-wit-hwt905` model.
Enter a name or use the suggested name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/imu-wit-hwt905-builder.png" alt="Creation of an `imu-wit` movement sensor in the Viam app config builder." resize="1200x" style="width:650px" >}}

Then fill in the attributes as applicable to your movement sensor, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-sensor-name>",
      "model": "imu-wit-hwt905",
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
      "model": "imu-wit-hwt905",
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
| Name  | Type   | Required? | Description |
| ----- | ------ | --------- | ----------- |
| `serial_path` | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. To find your serial device path, first connect the serial device to your machine, then:<ul><li>On Linux, run <code>ls /dev/serial/by-path/\*</code> to show connected serial devices, or look for your device in the output of <code>sudo dmesg \| grep tty</code>. Example: <code>"/dev/serial/by-path/usb-0:1.1:1.0"</code>.</li><li>On macOS, run <code>ls /dev/tty\* \| grep -i usb</code> to show connected USB serial devices, <code>ls /dev/tty\*</code> to browse all devices, or look for your device in the output of <code>sudo dmesg \| grep tty</code>. Example: <code>"/dev/ttyS0"</code>.</li></ul> |
| `serial_baud_rate` | int | Optional | The rate at which data is sent from the sensor over the serial connection. Valid rates are `9600` and `115200`.<br>Default: `115200` |

{{< readfile "/static/include/components/test-control/movement-sensor-imu-control.md" >}}

## Next steps

For more configuration and development info, see:

{{< cards >}}
{{% card link="/appendix/apis/components/movement-sensor/" customTitle="Movement sensor API" noimage="true" %}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{< /cards >}}
