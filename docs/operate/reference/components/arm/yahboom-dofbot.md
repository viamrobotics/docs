---
title: "Configure a Yahboom DOFBOT Arm"
linkTitle: "yahboom-dofbot"
weight: 50
type: "docs"
draft: "true"
description: "Configure a Yahboom DOFBOT modular arm."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
aliases:
  - "/components/arm/yahboom-dofbot/"
toc_hide: true
---

Viam supports the [Yahboom DOFBOT](https://category.yahboom.net/collections/r-robotics-arm) arm as a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}.
You can explore the source code on the [Viam-labs Yahboom GitHub repository](https://github.com/viam-labs/yahboom).

Configure a `dofbot` arm to add it to your machine.

If you want to test your arm as you configure it, connect it to your machine's computer and turn it on.
Then, configure the arm:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `arm` type, then select the `rand:yahboom:dofbot` modular resource.
Enter a name or use the suggested name for your arm and click **Create**.

There are no attributes available for this modular arm.

<!-- ![Web UI configuration panel for an arm of model yahboom-dofbot, with Attributes & Depends On dropdowns and the option to add a frame.](/components/arm/yahboom-dofbot-ui-config.png) -->

Edit and fill in the attributes as applicable.

{{% /tab %}}
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

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/arm.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/arm/" customTitle="Arm API" noimage="true" %}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/operate/mobility/move-arm/" noimage="true" %}}
{{< /cards >}}
