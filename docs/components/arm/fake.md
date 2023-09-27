---
title: "Configure a Fake Arm"
linkTitle: "fake"
weight: 34
type: "docs"
description: "Configure a fake arm to use for testing."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
# SMEs: William Spies
---

Configure a `fake` arm to test different models of robotic arms without any physical hardware:

{{< tabs name="Configure a Fake Arm" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `arm` type, then select the `fake` model.
Enter a name for your arm and click **Create**.

![An example configuration for a fake ur5e arm in the Viam app Config Builder.](/components/arm/fake-arm-ui-config.png)

Edit and fill in the attributes as applicable.
You can copy-paste from the [attribute examples](#attributes-examples) to help with formatting.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<arm_name>",
  "model": "fake",
  "type": "arm",
  "attributes": {
    "arm-model": "<your_arm_model>",
    "model-path": "<path_to_arm_model>"
  }
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
| `arm-model` | string | Optional | Model name of the robotic arm model you want your fake arm to act as. See [built-in arm models](../#configuration) for supported model names. |
| `model-path` | string | Optional | The path to the [kinematic configuration file](/internals/kinematic-chain-config/) of the arm driver you want your fake arm to act as. This path should point to the exact location where the file is located on your computer running `viam-server`. |

{{% alert title="Important" color="note" %}}

At least one of these attributes must be supplied for your `fake` arm to work.
If neither are specified, an error is thrown asking for specification.
If both attributes are specified, an error is thrown stating "can only populate either ArmModel or ModelPath - not both".

{{% /alert %}}

### Attributes examples

Paste one of the following examples into the **Attributes** section of your config:

{{< tabs >}}
{{% tab name="arm-model example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "arm-model": "ur5e"
}
```

Replace `ur5e` with the name of the arm model you want to use.
Examples include `xArm6`, `xArm7`, and `xArmLite`.

{{% /tab %}}
{{% tab name="model-path example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "model-path": "</Users/<YOUR-USERNAME>/downloads/universalrobots/ur5e.json>"
}
```

Replace the string with the path to your arm model.

{{% /tab %}}
{{< /tabs >}}
