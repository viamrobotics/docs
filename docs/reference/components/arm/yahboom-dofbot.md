---
title: "yahboom-dofbot"
linkTitle: "yahboom-dofbot"
weight: 50
type: "docs"
draft: "true"
description: "Reference for the yahboom-dofbot arm model. Yahboom DOFBOT modular arm."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
aliases:
  - "/components/arm/yahboom-dofbot/"
  - "/operate/reference/components/arm/yahboom-dofbot/"
---

Viam supports the [Yahboom DOFBOT](https://category.yahboom.net/collections/r-robotics-arm) arm as a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}.
You can explore the source code on the [Viam-labs Yahboom GitHub repository](https://github.com/viam-labs/yahboom).

Configure a `dofbot` arm to add it to your machine.

If you want to test your arm as you configure it, connect it to your machine's computer and turn it on.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-arm-name>",
      "model": "dofbot",
      "api": "rdk:component:arm",
      "attributes": {},
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
      "name": "myarm",
      "model": "yahboom-dofbot",
      "api": "rdk:component:arm",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{< readfile "/static/include/components/test-control/arm-control.md" >}}
