---
title: "Arm API"
linkTitle: "Arm"
weight: 10
type: "docs"
description: "Give commands to your arm components for linear motion planning."
icon: true
images: ["/icons/components/arm.svg"]
date: "2022-01-01"
aliases:
  - /appendix/apis/components/arm/
# updated: ""  # When the content was last entirely checked
---

The arm API allows you to give commands to your [arm components](/operate/reference/components/arm/) for linear motion planning with self-collision prevention.
If you want the arm to avoid obstacles, or you want to plan complex motion in an automated way, use the [motion API](/dev/reference/apis/services/motion/).

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
