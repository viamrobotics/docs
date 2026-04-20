---
title: "webgamepad"
linkTitle: "webgamepad"
weight: 30
type: "docs"
description: "Reference for the webgamepad input-controller model. Web-based gamepad as an input controller."
images: ["/icons/components/controller.svg"]
tags: ["input controller", "components"]
aliases:
  - "/operate/reference/components/input-controller/webgamepad/"
  - "/components/input-controller/webgamepad/"
  - "/reference/components/input-controller/webgamepad/"
component_description: "Supports a remote, web based gamepad."
# SMEs: James
---

Configuring a `webgamepad` input controller allows you to use a web-based gamepad as a device to communicate with your machine.

{{% alert title="Important" color="note" %}}
You **must** use "WebGamepad" as the `name` of the web gamepad controller.
This restriction will be removed in the future.
{{% /alert %}}

To be able to test your gamepad as you configure it, physically connect your gamepad to your machine's computer and turn both on.

## Configuration

Use the following configuration for an input controller of model `webgamepad`:

{{< tabs name="Configure a `webgamepad` input controller" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "WebGamepad",
      "model": "webgamepad",
      "api": "rdk:component:input_controller",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

{{< readfile "/static/include/components/test-control/input-controller-control.md" >}}

{{% alert title="Important" color="note" %}}
You have to press a button or move a stick on your gamepad for the browser to report the gamepad.
For your security, the browser won't report a gamepad until an input has been sent.
{{% /alert %}}
