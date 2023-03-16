---
title: "Configure a Agilex Limo Base"
linkTitle: "agilex-limo"
weight: 35
type: "docs"
description: "Configure an Agilex Limo base."
tags: ["base", "components"]
# SMEs: Steve B
---

A `agilex-limo` base is a model for [LIMO](https://global.agilex.ai/products/limo), a mobile robot designed around the AgileX mobile platform.

{{< tabs name="Configure a Wheeled Base" >}}
{{% tab name="Config Builder" %}}

On the **COMPONENTS** subtab of your robot's page in [the Viam app](https://app.viam.com), navigate to the **Create Component** menu.
Enter a name for your base, select the type `base`, and select the `agilex-limo` model.

<img src="../../img/base/base-ui-config.png" alt="An example configuration for a agilex-limo base in the Viam app, with Attributes & Depends On drop-downs and the option to add a frame." style="max-width:600px"/>

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "base",
      "type": "base",
      "model": "agilex-limo",
      "attributes": {
        "drive_mode": <"a_drive_mode_option">,
        "serial_path": <"/dev/ttyXXXX">
      },
      "depends_on": []
    }
}
```
{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `agilex-limo` bases:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `drive_mode` | string | **Required** | LIMO [steering mode](https://docs.trossenrobotics.com/agilex_limo_docs/operation/steering_modes.html#switching-steering-modes). Options: `differential`, `ackermann`, `omni` (mecanum). |
| `serial_path` | string | **Required** | Path to the LIMO's. |

## Next Steps