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
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> subtab, navigate to the <b>Create Component</b> menu.
Enter a name for your encoder, select the type <code>encoder</code>, and select the <code>fake</code> model.
<br>
<img src="../img/create-fake.png" alt="Creation of a Fake encoder in the Viam app config builder." style="max-width:600px" />
<br>
Fill in the attributes for your encoder:
<br>
<img src="../img/configure-fake.png" alt="Configuration of an AM5 encoder in the Viam app config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<encoder_name>",
    "type": "encoder",
    "model" : "fake",
    "attributes": {
      "update_rate_msec": <integer>
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for webcams:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `update_rate_msec` | *Required* | The update rate in milliseconds. |
