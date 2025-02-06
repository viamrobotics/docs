---
title: "Arm API"
linkTitle: "Arm"
weight: 10
type: "docs"
description: "Give commands to your arm components for linear motion planning."
icon: true
images: ["/icons/components/arm.svg"]
date: "2022-01-01"
modulescript: true
hide_children: true
outputs:
  - html
  - typesense
aliases:
  - /appendix/apis/components/arm/
  - /components/arm/
# updated: ""  # When the content was last entirely checked
---

The arm component API allows you to give commands to your arm components for linear motion with self-collision prevention.
If you want the arm to avoid obstacles, or you want to plan complex motion in an automated way, use the [motion API](/dev/reference/apis/services/motion/).
See also [Move an arm](/operate/mobility/move-arm/).

{{< expand "What is an arm component?" >}}
An arm {{< glossary_tooltip term_id="component" text="component" >}} represents a physical robotic arm, consisting of a serial chain of joints and links, with a fixed end and an end effector end, use an arm component.

Arms have two ends: one fixed in place, and one with a device you can position.
When controlling an arm, you can place its end effector at arbitrary cartesian positions relative to the base of the arm.
{{< /expand >}}

{{< expand "What models are supported?" >}}

The following list shows the available arm models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:arm" type="arm" no-intro="true">}}

{{< alert title="Add support for other models" color="tip" >}}

If none of the existing models fit your use case, you can [create](/operate/get-started/other-hardware/) a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} to add support for it.

{{< /alert >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component compatible with the Micro-RDK.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}

The arm component supports the following methods:

{{< readfile "/static/include/components/apis/generated/arm-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your arm and the rest of your machine, go to your machine's page on the [Viam app](https://app.viam.com),
Navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have an arm called `"my_arm"` configured as a component of your machine.
If your arm has a different name, change the `name` in the code.

Import the arm package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.arm import Arm
# To use move_to_position:
from viam.proto.common import Pose
# To use move_to_joint_positions:
from viam.proto.component.arm import JointPositions
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/arm"
  // To use MoveToPosition:
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/spatialmath"
  // To use MoveToJointPositions ("armapi" name optional, but necessary if importing other packages called "v1"):
  armapi "go.viam.com/api/component/arm/v1"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/components/apis/generated/arm.md" >}}

## Troubleshooting

If your arm is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
2. Review your arm model's documentation to ensure you have configured all required attributes.
3. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the arm there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.
