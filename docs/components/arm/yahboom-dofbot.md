---
title: "Configure a yahboom-dofbot Arm"
linkTitle: "yahboom-dofbot"
weight: 34
type: "docs"
draft: "true"
description: "Configure a yahboom-dofbot arm."
tags: ["arm", "components"]
# SMEs: William Spies
---

Configuring a `yahboom-dofbot` arm allows you to integrate a [Trossen Robotics ViperX 300](https://www.trossenrobotics.com/viperx-300-robot-arm.aspx) robotic arm into a Viam-based robot.

Configure a `yahboom-dofbot` arm as follows:

{{< tabs name="Configure a yahboom-dofbot Arm" >}}
{{% tab name="JSON Template" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<arm_name">",
    "type": "arm",
    "model": "yahboom-dofbot",
    "attributes": {
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for yahboom-dofbot arms:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
|  |  |  |
