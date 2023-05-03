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
      "model": "xArm7",
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
      "model": "xArm7",
      "name": "xArm7",
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

See [the Frame system](/services/frame-system) for more information on utilizing and modifying the `"frame"` configuration shown above.
