---
title: "Configure a lite6 Arm"
linkTitle: "lite6"
weight: 34
type: "docs"
description: "Configure a UFACTORY Lite 6 arm for your machine."
tags: ["arm", "components"]
aliases:
  - "/components/arm/xarmlite/"
# SMEs: Bucket, Motion
---

Configure a `lite6` arm to add a [UFACTORY Lite 6](https://www.ufactory.cc/product-page/ufactory-lite-6/) to your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
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
| Attribute | Type | Inclusion | Description |
| --------- | ---- | ----------| ----------- |
| `host` | string | **Required** | IP address of the arm's system on your network. Find this when setting up your xArm. |
| `port` | int | Optional | Port number of the arm's system. Find this when setting up your xArm. <br> Default: `502` |
| `speed_degs_per_sec` | float | Optional | Desired maximum speed of joint movement in degrees/sec. <br> Default: `20.0` |
| `acceleration_degs_per_sec_per_sec` | float | Optional | Desired maximum acceleration of joint movement in degrees/sec<sup>2</sup>. <br> Default: `50.0` |

See [the frame system service](/mobility/frame-system/) for more information on utilizing and modifying the `"frame"` configuration shown in the `JSON Example` above.

{{< readfile "/static/include/components/test-control/arm-control.md" >}}
