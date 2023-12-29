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
# SMEs: James
---

Configuring a `fake` input controller allows you to test an input controller communicating with your robot, without any physical hardware.

This controller can have [Controls](../#control-field) defined in `attributes`, as seen in the "JSON Template" tab below.
However, these Controls only ever return a single `PositionChangeAbs` event on the X axis, with the [Event.value](../#event-object) stuck at 0.7.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `input_controller` type, then select the `fake` model.
Enter a name for your input controller and click **Create**.

![An example configuration for a fake input controller component in the Viam App config builder.](/components/input-controller/fake-input-controller-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-fake-input-controller>",
      "model": "fake",
      "type": "input_controller",
      "namespace": "rdk",
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
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `callback_delay_sec` | float64 | **Required** | The number of seconds between callbacks getting triggered. Random between 1 and 2 if not specified. `0` is not valid and will be overwritten by a random delay. |
| `event_value` | float64 | Optional | Sets the value of events returned. Random between -1 and 1 if not specified. |

{{< readfile "/static/include/components/test-control/input-controller-control.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
