---
title: "Configure a Fake Switch"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Configure a fake switch for testing."
images: ["/icons/components/switch.svg"]
tags: ["switch", "components"]
aliases:
  - "/components/switch/fake/"
component_description: "A model used for testing, with no physical hardware."
toc_hide: true
---

The `fake` switch model is a model for testing switch functionality without physical hardware.
It simulates a multi-position switch which you can control programmatically.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `switch` type, then select the `fake` model.
Enter a name or use the suggested name for your arm and click **Create**.

Fill in the attributes as applicable to your switch, according to the table below.

{{% /tab %}}
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

## Test the switch

{{< readfile "/static/include/components/test-control/switch-control.md" >}}

## Troubleshooting

If your fake switch is not working as expected:

1. Check your machine logs on the **LOGS** tab to check for errors.
2. Make sure the `position_count` matches the number of `labels` if both are specified.
3. Verify that position values used with `SetPosition` are within the valid range (0 to `position_count - 1`).
4. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the switch there.

## Next steps

Check out the [switch API](/dev/reference/apis/components/switch/) or check out one of these guides:

{{< cards >}}
{{% card link="/dev/reference/apis/components/switch/" customTitle="Switch API" noimage="true" %}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{< /cards >}}
