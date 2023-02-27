---
title: "Configure a xArm7 Arm"
linkTitle: "xArm7"
weight: 34
type: "docs"
description: "Configure a xArm7 arm."
tags: ["arm", "components"]
# SMEs: William Spies
---

Configuring a `xArm7` arm allows you to integrate a [UFACTORY xArm 7](https://www.ufactory.cc/product-page/ufactory-xarm-7) robotic arm into a Viam-based robot.

Configure a `xArm7` arm as follows:

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
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

```json-viam {class="line-numbers linkable-line-numbers"}
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
| `host`  |  *Optional* | A string representing the IP address of the arm. Find this when setting up your arm model. |
| `speed` | *Optional* | Default: `20.0`. A float representing the desired maximum speed of joint movement in degrees/second. |
| `acceleration`  | *Optional* | Default: `50.0`. A float representing the desired maximum joint acceleration in degrees/second/second. |
