---
title: "Configure an xArm7 Arm"
linkTitle: "xArm7"
weight: 34
type: "docs"
description: "Configure a UFACTORY xArm 7 for your machine."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
aliases:
  - "/components/arm/xarm7/"
component_description: "Supports UFACTORY xArm 7."
# SMEs: Bucket, Motion
---

Configure an `xArm7` arm to integrate a [UFACTORY xArm 7](https://www.ufactory.cc/product-page/ufactory-xarm-7) into your machine.

Connect your arm to your machine and turn it on if you want to test your arm as you configure it.
Then, configure the arm:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `arm` type, then select the `xArm7` model.
Enter a name or use the suggested name for your arm and click **Create**.

![Web UI configuration panel for an arm of model xArm6 in the Viam app, with Attributes & Depends On dropdowns and the option to add a frame.](/components/arm/xArm7-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-arm-name>",
      "model": "xArm7",
      "type": "arm",
      "namespace": "rdk",
      "attributes": {
        "host": "<ip-address-to-connect-to-your-arm>",
        "port": <int>,
        "speed_degs_per_sec": <float>,
        "acceleration_degs_per_sec_per_sec": <float>
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
      "name": "my_xArm7",
      "model": "xArm7",
      "type": "arm",
      "namespace": "rdk",
      "attributes": {
        "host": "10.0.0.97"
      },
      "depends_on": [],
      "frame": {
        "orientation": {
          "type": "ov_degrees",
          "value": {
            "th": 0,
            "x": 0,
            "y": 0,
            "z": 1
          }
        },
        "parent": "world",
        "translation": {
          "x": 0,
          "y": 0,
          "z": 0
        }
      }
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `xArm7` arms:

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| ----------| ---- | --------- | ----------- |
| `host` | string | **Required** | IP address of the arm's system on your network. Find this when setting up your xArm. |
| `port` | int | Optional | Port number of the arm's system. Find this when setting up your xArm. <br> Default: `502` |
| `speed_degs_per_sec` | float | Optional | Desired maximum speed of joint movement in degrees/sec. <br> Default: `20.0` |
| `acceleration_degs_per_sec_per_sec` | float | Optional | Desired maximum acceleration of joint movement in degrees/sec<sup>2</sup>. <br> Default: `50.0` |

See [the frame system service](/services/frame-system/) for more information on utilizing and modifying the `"frame"` configuration shown in the `JSON Example` above.

{{< readfile "/static/include/components/test-control/arm-control.md" >}}

### Additional commands

In addition to the [Arm API](/appendix/apis/components/arm/), the `xArm7` arm supports some model-specific commands that allow you to set the speed and the acceleration of the arm.
You can invoke these commands by passing the following JSON document to the [`DoCommand()`](/appendix/apis/components/arm/#docommand) method:

```json
{
  "set_speed": 45.0,
  "set_acceleration": 10.0
}
```

| Key                | Type  | Description                                    |
| ------------------ | ----- | ---------------------------------------------- |
| `set_speed`        | float | Speed in degrees per second.                   |
| `set_acceleration` | float | Acceleration in degrees per second per second. |

For example:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
command = {
  "set_speed": 45.0,  # Set speed to 45.0 degrees per second
  "set_acceleration": 10.0  # Set acceleration to 10.0 degrees
                            # per second squared
}
result = await my_arm.do_command(command)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(machine, "my_arm")

cmd := map[string]interface{}{
    "set_speed": 45.0, // Set speed to 45.0 degrees per second
    "set_acceleration": 10.0  // Set acceleration to 10.0 degrees per second squared
}

result, err := myArm.DoCommand(context.Background(), cmd)
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart {class="line-numbers linkable-line-numbers"}
const command = {
  'set_speed': 45.0, // Set speed to 45.0 degrees per second
  'set_acceleration': 10.0 // Set acceleration to 10.0 degrees per second squared
};

var result = myArm.doCommand(command);
```

{{% /tab %}}
{{< /tabs >}}

## Next steps

For more configuration and development info, see:

{{< cards >}}
{{% card link="/appendix/apis/components/arm/" customTitle="Arm API" noimage="true" %}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/tutorials/services/accessing-and-moving-robot-arm/" noimage="true" %}}
{{< /cards >}}
