---
title: "Configure a Two-Wheeled Base (Micro-RDK)"
linkTitle: "two_wheeled_base (Micro-RDK)"
weight: 30
type: "docs"
description: "Configure and wire a two-wheeled base with a microcontroller."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - /micro-rdk/base/esp32_wheeled_base/
  - /build/micro-rdk/base/esp32_wheeled_base/
  - /build/micro-rdk/base/two_wheeled_base/
  - /components/base/two_wheeled_base/
micrordk_component: true
toc_hide: true
# SMEs: Gautham V.
---

A `two_wheeled_base` base supports mobile robotic bases with drive motors on both sides (differential steering).
Only bases with two drive wheels are supported by this `viam-micro-server` model.

{{< alert title="Info" color="info" >}}

The`two_wheeled_base` base model is not currently available when configuring your machine using **Builder** mode.

{{< /alert >}}

If you want to test your base as you configure it, physically assemble the base, connect it to your machine's computer, and turn it on.
Then, configure a `two_wheeled_base` base as follows:

{{< tabs name="Configure a Wheeled Base" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-base-name>",
      "model": "two_wheeled_base",
      "api": "rdk:component:base",
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
      "api": "rdk:component:base",
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `left` | string | **Required** | The `name` of a drive motor on the left side of the base. |
| `right` | string | **Required** | The `name` of a drive motor on the right side of the base. |

## Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/base.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/base/" customTitle="Base API" noimage="true" %}}
{{% card link="/tutorials/configure/configure-rover/" noimage="true" %}}
{{% card link="/tutorials/control/drive-rover/" noimage="true" %}}
{{< /cards >}}
