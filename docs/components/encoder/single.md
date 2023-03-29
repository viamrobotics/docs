---
title: "Configure a single encoder"
linkTitle: "single"
type: "docs"
description: "Configure a single encoder."
tags: ["encoder", "components"]
# SMEs: Rand
---

A `single` encoder sends a signal from the rotating encoder over a single wire to one pin on the board.
Software calculates the relative position that the motor has rotated.

Configuring a `single` encoder requires configuring one pin (`i`) on the board to which the encoder is wired.
The direction of spin is dictated by the motor that has this encoder's name in its `encoder` attribute field.

{{< tabs name="Configure an single encoder" >}}
{{% tab name="Config Builder" %}}

On the **COMPONENTS** subtab, navigate to the **Create Component** menu.
Enter a name for your encoder, select the type `encoder`, and select the `single` model.

<img src="../img/create-single.png" alt="Creation of a single encoder in the Viam app config builder." style="max-width:600px" />

Fill in the attributes for your encoder:

<img src="../img/configure-single.png" alt="Configuration of a single encoder in the Viam app config builder." />

{{% /tab %}}
{{% tab name="Raw JSON" %}}

```json {class="line-numbers linkable-line-numbers"}
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
