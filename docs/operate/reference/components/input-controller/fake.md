---
title: "Configure a Fake Input Controller for Testing"
linkTitle: "fake"
weight: 30
type: "docs"
description: "Configure a fake input controller for testing."
images: ["/icons/components/controller.svg"]
tags: ["input controller", "components"]
aliases:
  - "/components/input-controller/fake/"
component_description: "A model for testing, with no physical hardware."
toc_hide: true
# SMEs: James
---

Configuring a `fake` input controller allows you to test an input controller communicating with your machine, without any physical hardware.

This controller can have [Controls](/dev/reference/apis/components/input-controller/#control-field) defined in `attributes`, as seen in the "JSON Template" tab below.
However, these Controls only ever return a single `PositionChangeAbs` event on the X axis, with the [Event.value](/dev/reference/apis/components/input-controller/#event-object) stuck at 0.7.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `input_controller` type, then select the `fake` model.
Enter a name or use the suggested name for your input controller and click **Create**.

![An example configuration for a fake input controller component.](/components/input-controller/fake-input-controller-ui-config.png)

Edit the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-fake-input-controller>",
      "model": "fake",
      "api": "rdk:component:input_controller",
      "attributes": {
        "controls": [
          "AbsoluteX",
          "AbsoluteY",
          "AbsoluteZ"
        ],
        "event_value": <float>,
        "callback_delay_sec": <float>
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `fake` input controllers:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `callback_delay_sec` | float | **Required** | The number of seconds between callbacks getting triggered. Random between 1 and 2 if not specified. `0` is not valid and will be overwritten by a random delay. |
| `event_value` | float | Optional | Set the value of events returned. Random between -1 and 1 if not specified. |
| `controls` | array | Optional | Set the [Controls](/dev/reference/apis/components/input-controller/#control-field) that are present on the controller. |

{{< readfile "/static/include/components/test-control/input-controller-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/input-controller.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/input-controller/" customTitle="Input controller API" noimage="true" %}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/tutorials/control/gamepad/" noimage="true" %}}
{{< /cards >}}
