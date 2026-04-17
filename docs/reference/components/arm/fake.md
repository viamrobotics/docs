---
title: "fake"
linkTitle: "fake"
weight: 34
type: "docs"
description: "Reference for the fake arm model. Fake arm to use for testing."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
aliases:
  - "/components/arm/fake/"
  - "/operate/reference/components/arm/fake/"
component_description: "A model used for testing, with no physical hardware."
# SMEs: Bucket, Motion
---

Configure a `fake` arm to test different models of robotic arms without any physical hardware:

{{< tabs name="Configure a Fake Arm" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<arm_name>",
  "model": "fake",
  "api": "rdk:component:arm",
  "attributes": {
    "arm-model": "<your_arm_model>",
    "model-path": "<path_to_arm_model>"
  },
  "depends_on": []
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my-fake-arm",
  "model": "fake",
  "api": "rdk:component:arm",
  "attributes": {
    "arm-model": "ur5e"
  },
  "depends_on": []
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `fake` arms:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `arm-model` | string | Optional | Model name of the robotic arm model you want your fake arm to act as. See [built-in arm models](../) for supported model names. |
| `model-path` | string | Optional | The path to the [kinematic configuration file](/motion-planning/frame-system/) of the arm driver you want your fake arm to act as. This path should point to the exact location where the file is located on your computer running `viam-server`. |

{{< readfile "/static/include/components/test-control/arm-control.md" >}}
