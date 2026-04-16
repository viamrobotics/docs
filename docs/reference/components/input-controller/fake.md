---
title: "fake"
linkTitle: "fake"
weight: 30
type: "docs"
description: "Reference for the fake input-controller model. Fake input controller for testing."
images: ["/icons/components/controller.svg"]
tags: ["input controller", "components"]
aliases:
  - "/components/input-controller/fake/"
  - "/operate/reference/components/input-controller/fake/"
component_description: "A model for testing, with no physical hardware."
# SMEs: James
---

Configuring a `fake` input controller allows you to test an input controller communicating with your machine, without any physical hardware.

This controller can have [Controls](/reference/apis/components/input-controller/#control-field) defined in `attributes`, as seen in the "JSON Template" tab below.
However, these Controls only ever return a single `PositionChangeAbs` event on the X axis, with the [Event.value](/reference/apis/components/input-controller/#event-object) stuck at 0.7.

{{< tabs >}}
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
| `controls` | array | Optional | Set the [Controls](/reference/apis/components/input-controller/#control-field) that are present on the controller. |

{{< readfile "/static/include/components/test-control/input-controller-control.md" >}}
