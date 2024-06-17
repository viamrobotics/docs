---
title: "Configure an xArm6 Arm"
linkTitle: "xArm6"
weight: 34
type: "docs"
description: "Configure a UFACTORY xArm 6 into your machine."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
aliases:
  - "/components/arm/xarm6/"
component_description: "UFACTORY xArm 6."
# SMEs: Bucket, Motion
---

Configure an `xArm6` arm to integrate a [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6) into your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `arm` type, then select the `xArm6` model.
Enter a name or use the suggested name for your arm and click **Create**.

![Web UI configuration panel for an arm of model xArm6 in the Viam app, with Attributes & Depends On dropdowns and the option to add a frame.](/components/arm/xArm6-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-arm-name>",
      "model": "xArm6",
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
      "name": "my_xArm6",
      "model": "xArm6",
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

The following attributes are available for `xArm6` arms:

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | ----------| ----------- |
| `host`  | string | **Required** | IP address of the arm's system on your network. Find this when setting up your xArm. |
| `port`  | int | Optional | Port number of the arm's system. Find this when setting up your xArm. <br> Default: `502` |
| `speed_degs_per_sec` | float | Optional | Desired maximum speed of joint movement in degrees/sec. <br> Default: `20.0` |
| `acceleration_degs_per_sec_per_sec`  | float | Optional | Desired maximum acceleration of joint movement in degrees/sec<sup>2</sup>. <br> Default: `50.0` |

See [the frame system Service](/services/frame-system/) for more information on utilizing and modifying the `"frame"` configuration shown in the `JSON Example` above.

{{< readfile "/static/include/components/test-control/arm-control.md" >}}
