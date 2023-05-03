---
title: "Configure a fake input controller for testing"
linkTitle: "fake"
weight: 30
type: "docs"
description: "Configure a fake input controller for testing."
images: ["/components/img/components/controller.svg"]
tags: ["input controller", "components"]
# SMEs: James
---

Configuring a `fake` input controller allows you to test an input controller communicating with your robot, without any physical hardware.

This controller can have [Controls](../#control-field) defined in `attributes`, as seen in the "JSON Template" tab below.
However, these Controls only ever return a single `PositionChangeAbs` event on the X axis, with the [Event.value](../#event-object) stuck at 0.7.

## Configuration

Refer to the following example configuration for an input controller of model `fake`:

{{< tabs name="Configure a `fake` input controller" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your input controller, select the type `input_controller`, and select the `fake` model.
Click **Create component**.

![An example configuration for a fake input controller component in the Viam App config builder.](../img/fake-input-controller-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
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

{{< snippet "social.md" >}}
