---
title: "Configure an eva Arm"
linkTitle: "eva"
weight: 34
type: "docs"
draft: "true"
description: "Configure an eva arm."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
# SMEs: Bucket, Motion
---

Configure an `eva` arm to integrate a [Automata Eva](https://automata.tech/products/hardware/about-eva/) robotic arm into your robot.

Configure an `eva` arm as follows:

{{< tabs name="Configure an eva Arm" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<arm_name>",
  "type": "arm",
  "model": "eva",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for fake arms:

<!-- prettier-ignore -->
| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| | |  |
