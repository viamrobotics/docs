---
title: "Gripper Component"
linkTitle: "Gripper"
childTitleEndOverwrite: "Gripper Component"
weight: 60
type: "docs"
description: "A gripper is a robotic grasping device that can open and close."
tags: ["gripper", "components"]
icon: true
images: ["/icons/components/gripper.svg"]
no_list: true
modulescript: true
aliases:
  - "/components/gripper/"
hide_children: true
date: "2024-10-21"
# SMEs: Bucket Team
---

The gripper component provides an API for opening and closing a device.

If you have a robotic grasping device that can open and close, use a gripper component.

## Configuration

To use a robotic gripper, you need to add it to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your gripper.

The following list shows the available gripper models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:gripper" type="gripper" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component compatible with the Micro-RDK.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The [gripper API](/dev/reference/apis/components/gripper/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/gripper-table.md" >}}

## Troubleshooting

If your gripper is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review your gripper model's documentation to ensure you have configured all required attributes.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the gripper there.
1. Disconnect and reconnect your gripper.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper" noimage="true" %}}
{{< /cards >}}

You can also use the gripper component with the following services:

- [Motion service](/operate/reference/services/slam/): To move machines or components of machines
- [Frame system service](/operate/reference/services/navigation/): To configure the positions of your components
