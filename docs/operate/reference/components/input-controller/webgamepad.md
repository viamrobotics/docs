---
title: "Configure a Web Gamepad"
linkTitle: "webgamepad"
weight: 30
type: "docs"
description: "Configure a web-based gamepad as an input controller."
images: ["/icons/components/controller.svg"]
tags: ["input controller", "components"]
aliases:
  - "/components/input-controller/webgamepad/"
component_description: "Supports a remote, web based gamepad."
toc_hide: true
# SMEs: James
---

Configuring a `webgamepad` input controller allows you to use a web-based gamepad as a device to communicate with your machine.

{{% alert title="Important" color="note" %}}
You **must** use "WebGamepad" as the `name` of the web gamepad controller.
This restriction will be removed in the future.
{{% /alert %}}

To be able to test your gamepad as you configure it, physically connect your gamepad to your machine's computer and turn both on.
Then, configure the controller.

## Configuration

Use the following configuration for an input controller of model `webgamepad`:

{{< tabs name="Configure a `webgamepad` input controller" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `input_controller` type, then select the `webgamepad` model.
Enter the name `WebGamepad` and click **Create**.

![An example configuration for a web-based gamepad input controller component](/components/input-controller/webgamepad-input-controller-ui-config.png)

{{% /tab %}}
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

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/input-controller.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/input-controller/" customTitle="Input controller API" noimage="true" %}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/tutorials/control/gamepad/" noimage="true" %}}
{{< /cards >}}
