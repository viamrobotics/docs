---
title: "Configure a xArm6 Arm"
linkTitle: "xArm6"
weight: 34
type: "docs"
description: "Configure a xArm6 arm."
tags: ["arm", "components"]
# SMEs: William Spies
---

Configure a `xArm6` arm to integrate a [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6) into your robot.

Configure a `xArm6` arm as follows:

{{< tabs >}}
{{% tab name="Config Builder" %}}

<img src="../../img/arm/arm-ui-config-xarm6.png" alt="Web UI configuration panel for an arm of model xArm6 in the Viam app, with Attributes & Depends On drop-downs and the option to add a frame." max-width="800px"/>

{{% /tab %}}

{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [{
      "attributes": {
          "host": <your_arms_ip_address_on_your_network>
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
      "model": "xArm6",
      "name": <your_arm_name>,
      "type": "arm"
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
      "model": "xArm6",
      "name": "xArm6",
      "type": "arm"
  }]
}
```

{{% /tab %}}
{{% /tabs %}}

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `host`  | **Required** | A string representing the IP address of the arm. Find this when setting up your arm model. |
| `speed` | **Required** | Default: `20.0`. A float representing the desired maximum speed of joint movement in degrees/second. |
| `acceleration`  | **Required** | Default: `50.0`. A float representing the desired maximum joint acceleration in degrees/second/second. |

See [the Frame system](../../../services/frame-system/) for more information on utilizing and modifying the `"frame"` configuration shown above.
