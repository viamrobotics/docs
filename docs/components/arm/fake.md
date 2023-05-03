---
title: "Configure a Fake Arm"
linkTitle: "fake"
weight: 34
type: "docs"
description: "Configure a fake arm to use for testing."
tags: ["arm", "components"]
# SMEs: William Spies
---

Configure a `fake` arm to test different models of robotic arms without any physical hardware:

{{< tabs name="Configure a Fake Arm" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your arm, select the type `arm`, and select the `fake` model.

Click **Create component** and then fill in the attributes for your model:

![An example configuration for a fake ur5e arm in the Viam app Config Builder.](../img/fake-arm-ui-config.png)

Note that this visual example sets the `fake` arm to act as a `ur5e` arm.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<arm_name>",
    "type": "arm",
    "model": "fake",
    "attributes": {
        "arm-model": "<your_arm_model>",
        "model-path": "<your_arm_model_config_filepath>" // REMOVE if using arm-model
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for fake arms:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `arm-model` | Optional | The name of the robotic arm model you want your fake arm to act as. This attribute must match the `name` of one of the arms Viam currently supports. See [here](../#configuration) for supported model names. |
| `model-path` | Optional | The path to a compatible Arm's ModelJSON or URDF configuration file that you want your fake arm to act as. This path should point to the exact location where your configuration file is located on your computer running `viam-server`. |

{{% alert title="Note" color="note" %}}

At least one of these attributes must be supplied for your `fake` arm to work.
If neither are specified, an error is thrown asking for specification.
If both attributes are specified, an error is thrown stating "can only populate either ArmModel or ModelPath - not both".

{{% /alert %}}

Refer to the following JSON examples for differences in configuration between the two attributes available:

{{< tabs name="Configuration with arm-model or model-path" >}}
{{% tab name="arm-model JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<arm-name>",
    "type": "arm",
    "model": "fake",
    "attributes": {
        "arm-model": "ur5e"
    }
}
```

{{% /tab %}}
{{% tab name="model-path JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<arm-name>",
    "type": "arm",
    "model": "fake",
    "attributes": {
        "model-path": "/Users/<YOUR-USERNAME>/downloads/universalrobots/ur5e.json"
    }
}
```

{{% /tab %}}
{{< /tabs >}}

Once you have successfully configured your `fake` arm, you can navigate to the **control** tab of [the Viam app](https://app.viam.com).
A drop-down menu should appear with the name of your arm that allows you to toggle the fake arm's joint positions and Cartesian end positions to dynamically test motion planning:

<img src="../img/fake-arm-ui-remote-control.png" alt="Motion planning remote-control of a fake ur5e arm in the Viam app control tab." style="max-width:800px" />

Note that this visual example sets the `fake` arm to act as a  `ur5e` arm.
