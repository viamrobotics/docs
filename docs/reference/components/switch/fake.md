---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake switch model. Fake switch for testing."
images: ["/icons/components/switch.svg"]
tags: ["switch", "components"]
aliases:
  - "/components/switch/fake/"
  - "/operate/reference/components/switch/fake/"
component_description: "A model used for testing, with no physical hardware."
---

The `fake` switch model is a model for testing switch functionality without physical hardware.
It simulates a multi-position switch which you can control programmatically.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-switch-name>",
      "model": "fake",
      "type": "switch",
      "namespace": "rdk",
      "attributes": {
        "position_count": <number>,
        "labels": ["<label1>", "<label2>", "<label3>"]
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
      "name": "my_switch",
      "model": "fake",
      "type": "switch",
      "namespace": "rdk",
      "attributes": {
        "position_count": 4,
        "labels": ["Off", "Low", "Medium", "High"]
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

The following attributes are available for the `fake` switch model:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `position_count` | int | **Required** | The number of positions that the switch can be in. Default: `2` |
| `labels` | array | Optional | An array of labels corresponding to the positions. Default: numeric values for the number of positions, starting with 0. |

## Troubleshooting

If your fake switch is not working as expected:

1. Check your machine logs on the **LOGS** tab to check for errors.
2. Make sure the `position_count` matches the number of `labels` if both are specified.
3. Verify that position values used with `SetPosition` are within the valid range (0 to `position_count - 1`).
4. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the switch there.
