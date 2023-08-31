---
title: "Configure an Agilex LIMO Base"
linkTitle: "agilex-limo"
weight: 40
type: "docs"
description: "Configure an Agilex LIMO base for your robot."
tags: ["base", "components"]
images: ["/icons/components/base.svg"]
# SMEs: Matt Vella, Steve B
---

An `agilex-limo` base supports [LIMO](https://global.agilex.ai/products/limo), a mobile robot designed around the AgileX mobile platform.

Configure an `agilex-limo` base as follows:

{{< tabs name="Configure an Agilex-Limo Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your base, select the type `base`, and select the `agilex-limo` model.

Click **Create component**.

![An example configuration for a agilex-limo base in the Viam app Config Builder.](/components/base/agilex-limo-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-base-name>",
      "type": "base",
      "model": "agilex-limo",
      "attributes": {
        "drive_mode": "<your-drive-mode>",
        "serial_path": "<your-serial-path>"
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
| `serial_path` | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyTHS1`, to its device file, such as <file>/dev/ttyTHS1</file>. If you omit this attribute, Viam will attempt to automatically detect the path.<br>Default: `/dev/ttyTHS1` |

{{< readfile "/static/include/components/base-control.md" >}}
