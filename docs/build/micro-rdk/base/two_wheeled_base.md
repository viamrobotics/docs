---
title: "Configure a Two Wheeled Base (Micro-RDK)"
linkTitle: "two_wheeled_base"
weight: 30
type: "docs"
description: "Configure and wire a two wheeled base with a microcontroller."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - /micro-rdk/base/esp32_wheeled_base/
  - /build/micro-rdk/base/esp32_wheeled_base/
# SMEs: Gautham V.
---

A `two_wheeled_base` base supports mobile robotic bases with drive motors on both sides (differential steering).
Only two-wheeled bases are supported by this micro-RDK model.

{{< alert title="Info" color="info" >}}

The`two_wheeled_base` base model is not currently available as a built-in option in [the Viam app](https://app.viam.com), so you cannot use **Builder** mode to configure this board.

{{< /alert >}}

Configure a `two_wheeled_base` base as follows:

{{< tabs name="Configure a Wheeled Base" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-base-name>",
      "model": "two_wheeled_base",
      "type": "base",
      "namespace": "rdk",
      "attributes": {
        "left": "<your-left-motor-name>",
        "right": "<your-right-motor-name>"
      }
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
      "name": "my-wheeled-base",
      "model": "two_wheeled_base",
      "type": "base",
      "namespace": "rdk",
      "attributes": {
        "left": "leftm",
        "right": "rightm"
      },
      "depends_on": []
    }, ... <INSERT LEFT AND RIGHT MOTOR CONFIGS>
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `two_wheeled_base` bases:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `left` | string | **Required** | The `name` of a drive motor on the left side of the base. |
| `right` | string | **Required** | The `name` of a drive motor on the right side of the base. |

## Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}
