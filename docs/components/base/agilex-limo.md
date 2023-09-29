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
Click on the **Components** subtab and click **Create component**.
Select the `base` type, then select the `agilex-limo` model.
Enter a name for your base and click **Create**.

![An example configuration for a agilex-limo base in the Viam app Config Builder.](/components/base/agilex-limo-ui-config.png)

Copy and paste the following attribute template into your base's **Attributes** box.
Then remove and fill in the attributes as applicable to your base, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "drive_mode": "< ackermann | differential | omni >",
  "serial_path": "<your-serial-path>"
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "drive_mode": "omni",
  "serial_path": "/dev/ttyTHS1"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-base-name>",
      "model": "agilex-limo",
      "type": "base",
      "namespace": "rdk",
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

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `drive_mode` | string | **Required** | LIMO [steering mode](https://docs.trossenrobotics.com/agilex_limo_docs/operation/steering_modes.html#switching-steering-modes). Options: `differential`, `ackermann`, `omni` (mecanum). |
| `serial_path` | string | **Required** | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyTHS1`, to its device file, such as <file>/dev/ttyTHS1</file>. If you omit this attribute, Viam will attempt to automatically detect the path.<br>Default: `/dev/ttyTHS1` |

## Test the base

{{< readfile "/static/include/components/base-control.md" >}}
