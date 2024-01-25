---
title: "Configure an xArmLite Arm"
linkTitle: "xArmLite"
weight: 34
type: "docs"
description: "Configure a UFACTORY Lite 6 arm for your machine."
tags: ["arm", "components"]
aliases:
  - "/components/arm/xarmlite/"
# SMEs: Bucket, Motion
---

Configure an `xArmLite` arm to add a [UFACTORY Lite 6](https://www.ufactory.cc/product-page/ufactory-lite-6/) to your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `arm` type, then select the `xArmLite` model.
Enter a name for your arm and click **Create**.

![Web UI configuration panel for an arm of model xArmLite in the Viam app, with Attributes & Depends On dropdowns and the option to add a frame.](/components/arm/xArmLite-ui-config.png)

Copy and paste the following attribute template into your arm's **Attributes** box.
Then remove and fill in the attributes as applicable to your arm, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "host": "<your-arms-ip-address-on-your-network>",
  "port": <int>,
  "speed_degs_per_sec": <float>,
  "acceleration_degs_per_sec_per_sec": <float>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "host": "10.0.0.23"
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
      "name": "<your-arm-name>",
      "model": "xArmLite",
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
      "model": "xArmLite",
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

The following attributes are available for `xArmLite` arms:

<!-- prettier-ignore -->
| Attribute | Type | Inclusion | Description |
| --------- | ---- | ----------| ----------- |
| `host` | string | **Required** | IP address of the arm's system on your network. Find this when setting up your xArm. |
| `port` | int | Optional | Port number of the arm's system. Find this when setting up your xArm. <br> Default: `502` |
| `speed_degs_per_sec` | float | Optional | Desired maximum speed of joint movement in degrees/sec. <br> Default: `20.0` |
| `acceleration_degs_per_sec_per_sec` | float | Optional | Desired maximum acceleration of joint movement in degrees/sec<sup>2</sup>. <br> Default: `50.0` |

See [the frame system service](/mobility/frame-system/) for more information on utilizing and modifying the `"frame"` configuration shown in the `JSON Example` above.

{{< readfile "/static/include/components/test-control/arm-control.md" >}}
