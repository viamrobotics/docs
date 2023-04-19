---
title: "Configure a fake encoder"
linkTitle: "fake"
type: "docs"
description: "Configure a fake encoder."
tags: ["encoder", "components"]
# SMEs: Rand
---

The `fake` encoder is an encoder model for testing code without any hardware.

{{< tabs name="Configure an fake encoder" >}}
{{% tab name="Config Builder" %}}

On the **Components** subtab, navigate to the **Create Component** menu.
Enter a name for your encoder, select the type `encoder`, and select the `fake` model.

<img src="../img/create-fake.png" alt="Creation of a fake encoder in the Viam app config builder." style="max-width:600px" />

Fill in the attributes for your encoder:

<img src="../img/configure-fake.png" alt="Configuration of a fake encoder in the Viam app config builder." />

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<encoder_name>",
    "type": "encoder",
    "model" : "fake",
    "attributes": {}
}
```

{{% /tab %}}
{{< /tabs >}}
