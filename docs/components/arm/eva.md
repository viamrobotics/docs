---
title: "Configure an Eva Arm"
linkTitle: "eva"
weight: 34
type: "docs"
draft: "true"
description: "Configure an Eva arm."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
aliases:
  - "/components/arm/eva/"
# SMEs: Bucket, Motion
---

Configure an `eva` arm to integrate a [Automata Eva](https://automata.tech/products/hardware/about-eva/) robotic arm into your machine:

{{< tabs name="Configure an eva Arm" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<arm_name>",
  "model": "eva",
  "type": "arm",
  "namespace": "rdk",
  "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}

{{< readfile "/static/include/components/test-control/arm-control.md" >}}

## Next steps

To get started using your arm, see the [arm API](/appendix/apis/components/arm/).
For more configuration and development info, see

{{< cards >}}
{{% card link="/appendix/apis/components/arm/" customTitle="Arm API" noimage="true" %}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/tutorials/services/accessing-and-moving-robot-arm/" noimage="true" %}}
{{< /cards >}}
