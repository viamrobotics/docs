---
title: "eva"
linkTitle: "eva"
weight: 34
type: "docs"
draft: "true"
description: "Reference for the eva arm model. Eva arm."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
aliases:
  - "/components/arm/eva/"
  - "/operate/reference/components/arm/eva/"
# SMEs: Bucket, Motion
---

Configure an `eva` arm to integrate an [Automata Eva](https://automata.tech/products/hardware/about-eva/) robotic arm into your machine.

If you want to test your arm as you configure it, connect it to your machine's computer and turn it on.

{{< tabs name="Configure an eva Arm" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<arm_name>",
  "model": "eva",
  "api": "rdk:component:arm",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

{{< readfile "/static/include/components/test-control/arm-control.md" >}}
