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

Configure an `eva` arm to integrate an [Automata Eva](https://automata.tech/products/hardware/about-eva/) robotic arm into your machine.

If you want to test your arm as you configure it, connect it to your machine's computer and turn it on.
Then, configure the arm:

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

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/arm.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/appendix/apis/components/arm/" customTitle="Arm API" noimage="true" %}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/move-robot-arm/" noimage="true" %}}
{{< /cards >}}
