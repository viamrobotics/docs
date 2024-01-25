---
title: "Configure a Fake Arm"
linkTitle: "fake"
weight: 34
type: "docs"
description: "Configure a fake arm to use for testing."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
aliases:
  - "/components/arm/fake/"
# SMEs: Bucket, Motion
---

Configure a `fake` arm to test different models of robotic arms without any physical hardware:

{{< tabs name="Configure a Fake Arm" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `arm` type, then select the `fake` model.
Enter a name for your arm and click **Create**.

![An example configuration for a fake ur5e arm in the Viam app Config Builder.](/components/arm/fake-arm-ui-config.png)

Copy and paste the following attribute template into your arm's **Attributes** box.
Then remove and fill in the attributes as applicable to your arm, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "arm-model": "<string>",
  "model-path": "<string>"
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "arm-model": "ur5e"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<arm_name>",
  "model": "fake",
  "type": "arm",
  "namespace": "rdk",
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
  "type": "arm",
  "namespace": "rdk",
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
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `arm-model` | string | Optional | Model name of the robotic arm model you want your fake arm to act as. See [built-in arm models](../#supported-models) for supported model names. |
| `model-path` | string | Optional | The path to the [kinematic configuration file](/internals/kinematic-chain-config/) of the arm driver you want your fake arm to act as. This path should point to the exact location where the file is located on your computer running `viam-server`. |

{{% alert title="Important" color="note" %}}

Exactly one of these attributes must be supplied for your `fake` arm to work.
If neither are specified, an error is thrown asking for specification.
If both attributes are specified, an error is thrown stating "can only populate either ArmModel or ModelPath - not both".

{{% /alert %}}

{{< readfile "/static/include/components/test-control/arm-control.md" >}}
