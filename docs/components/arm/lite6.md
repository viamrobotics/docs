---
title: "Configure a lite6 Arm"
linkTitle: "lite6"
weight: 34
type: "docs"
description: "Configure a UFACTORY Lite 6 arm for your machine."
tags: ["arm", "components"]
aliases:
  - "/components/arm/xarmlite/"
component_description: "Supports UFACTORY Lite 6."
# SMEs: Bucket, Motion
---

Configure a `lite6` arm to add a [UFACTORY Lite 6](https://www.ufactory.cc/product-page/ufactory-lite-6/) to your machine.

If you want to test your arm as you configure it, connect it to your machine's computer and turn it on.
Then, configure the arm:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `arm` type, then select the `lite6` model.
Enter a name or use the suggested name for your arm and click **Create**.

![Web UI configuration panel for an arm of model lite6 in the Viam app, with Attributes & Depends On dropdowns and the option to add a frame.](/components/arm/lite6-ui-config.png)

Fill in the attributes as applicable to your arm, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-arm-name>",
      "model": "lite6",
      "type": "arm",
      "namespace": "rdk",
      "attributes": {
        "host": "<your-arms-ip-address-on-your-network>",
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
      "name": "my_arm",
      "model": "lite6",
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

The following attributes are available for `lite6` arms:

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------- |
| `host` | string | **Required** | IP address of the arm's system on your network. Find this when setting up your xArm. |
| `port` | int | Optional | Port number of the arm's system. Find this when setting up your xArm. <br> Default: `502` |
| `speed_degs_per_sec` | float | Optional | Desired maximum speed of joint movement in degrees/sec. <br> Default: `20.0` |
| `acceleration_degs_per_sec_per_sec` | float | Optional | Desired maximum acceleration of joint movement in degrees/sec<sup>2</sup>. <br> Default: `50.0` |

See [the frame system service](/services/frame-system/) for more information on utilizing and modifying the `"frame"` configuration shown in the `JSON Example` above.

{{< readfile "/static/include/components/test-control/arm-control.md" >}}

### Additional commands

In addition to the [Arm API](/appendix/apis/components/arm/), the `lite6` arm supports some model-specific commands that allow you to set the speed and the acceleration of the arm.
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

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/arm.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/appendix/apis/components/arm/" customTitle="Arm API" noimage="true" %}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/tutorials/services/accessing-and-moving-robot-arm/" noimage="true" %}}
{{< /cards >}}
