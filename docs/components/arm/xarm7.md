---
title: "Configure an xArm7 Arm"
linkTitle: "xArm7"
weight: 34
type: "docs"
description: "Configure an xArm7 arm."
images: ["/components/img/components/arm.svg"]
tags: ["arm", "components"]
# SMEs: William Spies
---

Configure an `xArm7` arm to integrate a [UFACTORY xArm 7](https://www.ufactory.cc/product-page/ufactory-xarm-7) into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your arm, select the type `arm`, and select the `xArm7` model.

Click **Create component**.

![Web UI configuration panel for an arm of model xArm6 in the Viam app, with Attributes & Depends On drop-downs and the option to add a frame.](../img/xArm7-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [{
      "model": "xArm7",
      "name": "<your-arm-name>",
      "type": "arm",
      "attributes": {
          "host": "<ip-address-to-connect-to-your-arm>"
      },
      "depends_on": []
    }]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [{
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
      },
      "model": "xArm7",
      "name": "xArm7",
      "type": "arm"
  }]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `xArm7` arms:

| Attribute | Type | Inclusion | Description |
| ----------| ---- | ----------| ----------- |
| `host`  | string | **Required** | IP address of the arm's system on your network. Find this when setting up your xArm. |
| `port`  | int | Optional | Port number of the arm's system. Find this when setting up your xArm. <br> Default: `502` |
| `speed` | float | Optional | Desired maximum speed of joint movement in degrees/sec. <br> Default: `20.0` |
| `acceleration`  | float | Optional | Desired maximum acceleration of joint movement in degrees/sec<sup>2</sup>. <br> Default: `50.0` |

See [the Frame System Service](/services/frame-system) for more information on utilizing and modifying the `"frame"` configuration shown in the `JSON Example` above.
