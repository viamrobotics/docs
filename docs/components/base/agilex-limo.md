---
title: "Configure an Agilex LIMO Base"
linkTitle: "agilex-limo"
weight: 40
type: "docs"
description: "Configure an Agilex LIMO base."
tags: ["base", "components"]
# SMEs: Matt Vella, Steve B
---

An `agilex-limo` base supports [LIMO](https://global.agilex.ai/products/limo), a mobile robot designed around the AgileX mobile platform.

Configure an `agilex-limo` base as follows:

{{< tabs name="Configure an Agilex-Limo Base" >}}
{{% tab name="Config Builder" %}}

On the **Components** subtab of your robot's page in [the Viam app](https://app.viam.com), navigate to the **Create Component** menu.
Enter a name for your base, select the type `base`, and select the `agilex-limo` model.

![An example configuration for a agilex-limo base in the Viam app Config Builder.](../img/agilex-limo-ui-config.png)

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
| `drive_mode` | string | **Required** | Options: `differential`, `ackermann`, `omni` (mecanum). LIMO [steering mode](https://docs.trossenrobotics.com/agilex_limo_docs/operation/steering_modes.html#switching-steering-modes). |
| `serial_path` | string | **Required** | Default: `/dev/ttyTHS1`. Your serial port connection to your LIMO's [board](../../board/). Determine during setup and start of your LIMO. |
