---
title: "Configure an MPU-6050 Gyroscope/Accelerometer"
linkTitle: "gyro-mpu6050"
weight: 40
type: "docs"
description: "Configure an MPU-6050 movement sensor."
images: ["/icons/components/imu.svg"]
# SMEs: Rand
---

The `gyro-mpu6050` movement sensor model supports a combination [gyroscope and accelerometer manufactured by TDK InvenSense](https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/).

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `movement-sensor` type, then select the `gyro-mpu6050` model.
Enter a name for your movement sensor and click **Create**.

{{< imgproc src="/components/movement-sensor/mpu6050-builder.png" alt="Creation of an `gyro-mpu6050` movement sensor in the Viam app config builder." resize="600x" >}}

Copy and paste the following attribute template into your movement sensor's **Attributes** box.
Then remove and fill in the attributes as applicable to your movement sensor, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "<your-board-name>",
  "i2c_bus": "<your-i2c-bus-name-on-board>",
  "use_alt_i2c_address": <boolean>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board": "local",
  "i2c_bus": "default_i2c_bus"
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
      "model": "gyro-mpu6050",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "board": "<your-board-name>",
        "i2c_bus": "<your-i2c-bus-name-on-board>",
        "use_alt_i2c_address": <boolean>
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
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "i2cs": [
          {
            "name": "default_i2c_bus",
            "bus": "1"
          }
        ]
      }
    },
    {
      "name": "my_accelgyro",
      "model": "gyro-mpu6050",
      "type": "movement_sensor",
      "namespace": "rdk",
      "attributes": {
        "board": "local",
        "i2c_bus": "default_i2c_bus"
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

<!-- prettier-ignore -->
| Name                  | Type    | Inclusion    | Description |
| --------------------- | ------- | ------------ | ----------- |
| `board`               | string  | **Required** | The `name` of the [board](/components/board/) to which the device is wired. |
| `i2c_bus`             | string  | **Required** | The `name` of the [I<sup>2</sup>C bus configured](/components/board/#i2cs) on your [board](/components/board/) wired to this device. |
| `use_alt_i2c_address` | boolean | Optional     | Depends on whether you wire AD0 low (leaving the default address of 0x68) or high (making the address 0x69). If high, set `true`. If low, set `false`. <br> Default: `false` |

{{< readfile "/static/include/components/test-control/movement-sensor-control.md" >}}
