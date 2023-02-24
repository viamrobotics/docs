---
title: "Configure a single encoder"
linkTitle: "single"
type: "docs"
description: "Configure a single encoder."
tags: ["encoder", "components"]
# SMEs: Rand
---

Configuring a `single` encoder requires configuring one pin (`i`) on the board to which the encoder is wired.
The single pin receives the output used to calculate the relative position.

{{< tabs name="Configure an single encoder" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> subtab, navigate to the <b>Create Component</b> menu.
Enter a name for your encoder, select the type <code>encoder</code>, and select the <code>single</code> model.
<br>
<img src="../img/create-single.png" alt="Creation of an AM5 encoder in the Viam app config builder." style="max-width:600px" />
<br>
Fill in the attributes for your encoder:
<br>
<img src="../img/configure-single.png" alt="Configuration of an AM5 encoder in the Viam app config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<encoder_name>",
    "type": "encoder",
    "model" : "single",
    "attributes": {
      "board": "<board_name>",
      "pins": {
        "i": <string>
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `single` encoders:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `board` | *Required* | The name of the board to which the encoder is wired. |
| `pins` | *Required* | A struct holding the name of the pin wired to the encoder: <ul> <li> <code>i</code>: Pin number of the pin to which the encoder is wired. Use pin number, not GPIO number. </li> </ul> |

Viam also supports a model of encoder called [`"incremental"`](../incremental) which uses two pins.
