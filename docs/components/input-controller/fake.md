---
title: "Configure a fake input controller for testing"
linkTitle: "fake"
weight: 30
type: "docs"
description: "Configure a fake input controller for testing."
tags: ["input controller", "components"]
# SMEs: James
---

Configuring a `fake` input controller allows you to test an input controller communicating with your robot, without any physical hardware.

This controller can have [Controls](../#control-field) defined in `attributes`, as seen in the "JSON Template" tab below.
However, these Controls only ever return a single `PositionChangeAbs` event on the X axis, with the [Event.value](../#event-object) stuck at 0.7.

## Configuration

Refer to the following example configuration for an input controller of model `fake`:

{{< tabs name="Configure a `fake` input controller" >}}
{{< tab name="Config Builder" >}}

<img src="../img/fake-input-controller-ui-config.png" alt="What an example configuration for a fake input controller component looks like in the Viam App config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="JSON Template" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <your-fake-input-controller>,
      "type": "input_controller",
      "model": "fake",
      "attributes": {
        controls: [
          "AbsoluteX", 
          "AbsoluteY", 
          "AbsoluteZ"
        ]
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
