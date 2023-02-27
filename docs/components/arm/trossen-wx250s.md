---
title: "Configure a trossen-wx250s Arm"
linkTitle: "trossen-wx250s"
weight: 34
type: "docs"
draft: "true"
description: "Configure a trossen-wx250s arm."
tags: ["arm", "components"]
# SMEs: William Spies
---

Configuring a `trossen-wx250s` arm allows you to integrate a [Trossen Robotics WidowX 250](https://www.trossenrobotics.com/widowx-250-robot-arm.aspx) robotic arm into a Viam-based robot.

Configure a `trossen-wx250s` arm as follows:

{{< tabs name="Configure a trossen-wx250 Arm" >}}
{{% tab name="JSON Template" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<arm_name">",
    "type": "arm",
    "model": "trossen-wx250s",
    "attributes": {
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for trossen-wx250s arms:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
|  |  |  |
