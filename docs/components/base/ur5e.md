---
title: "Configure a ur5e Arm"
linkTitle: "ur5e"
weight: 40
type: "docs"
description: "Configure a ur5e arm."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
---

Configure a `ur5e` arm to add a [Universal Robots UR5e](https://www.universal-robots.com/products/ur5-robot) to your robot:

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "model": "ur5e",
      "name": "<your-arm-name>",
      "type": "arm",
      "attributes": {
        "speed_degs_per_sec": <float>,
        "host": "<your-host-address>",
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
      "depends_on": [],
      "model": "pi",
      "name": "local",
      "type": "board",
      "attributes": {
      }
    },
    {
      "name": "my-arm",
      "type": "arm",
      "model": "ur5e",
      "attributes": {
        "speed_degs_per_sec": 1,
        "host": "10.1.10.82"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `ur5e` arms:

| Attribute | Type | Inclusion | Description |
| --------- | ---- | ----------| ----------- |
| `speed_degs_per_sec`  | float | **Required** | Desired maximum speed of joint movement in degrees/sec. <br> Range: `[.1, 1]` |
| `host`  | string | **Required** | The IP address of the arm's system on your network. Find this when setting up your UR5e. |
