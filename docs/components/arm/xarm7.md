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

Configure an `xArm7` arm to integrate a [UFACTORY xArm 7](https://www.ufactory.cc/product-page/ufactory-xarm-7) into your machine:

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

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Raises:**

- (NotImplementedError): Raised if the Resource does not support arbitrary commands.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
command = {
  "set_speed": 45.0, # Set speed to 45.0 degrees per second
  "set_acceleration": 10.0 # Set acceleration to 10.0 degrees per second squared
}
result = await my_arm.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(machine, "my_arm")

cmd := map[string]interface{}{
    "set_speed": 45.0, // Set speed to 45.0 degrees per second
    "set_acceleration": 10.0  // Set acceleration to 10.0 degrees per second squared
}

result, err := myArm.DoCommand(context.Background(), cmd)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
const command = {
  'set_speed': 45.0, // Set speed to 45.0 degrees per second
  'set_acceleration': 10.0 // Set acceleration to 10.0 degrees per second squared
};

var result = myArm.doCommand(command);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Resource/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

## Next steps

For more configuration and development info, see:

{{< cards >}}
{{% card link="/appendix/apis/components/arm/" customTitle="Arm API" noimage="true" %}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/tutorials/services/accessing-and-moving-robot-arm/" noimage="true" %}}
{{< /cards >}}
