---
title: "Configure a Fake Arm"
linkTitle: "fake"
weight: 34
type: "docs"
description: "Configure a fake arm to use for testing."
tags: ["arm", "components"]
# SMEs: William Spies
---

A `fake` arm is an arm model for testing without any physical hardware.

Configure a `fake` arm as follows:

{{< tabs name="Configure a Fake Arm" >}}
{{< tab name="Config Builder" >}}

<img src="../img/fake-arm-ui-config.png" alt="Creation of a fake ur5e arm in the Viam app config builder." style="max-width:600px" />

<br>
Note that this visual example sets the <code>fake</code> arm to act as a <code>ur5e</code> arm.

{{< /tab >}}
{{% tab name="JSON Template" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<arm_name">",
    "type": "arm",
    "model": "fake",
    "attributes": {
        "arm-model": "<your_arm_model>"
        "model-path": "<your_arm_ModelJSON_path>" // REMOVE if using arm-model
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for fake arms:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `arm-model` | *Optional* | The name of the robotic arm model you want your fake arm to act as. This attribute must match the `name` of one of the arms Viam currently supports. See [here](../#configuration) for supported model names. |
| `model-path` | *Optional* | The path to a compatible ArmModel JSON or URDF configuration file that you want your fake arm to act as. This path is within your `viam-server` instances' RDK directory from the `fake` model. An example: <file>../universalrobots/ur5e.json</file> `model-path` corresponds to [GitHub here.] |

{{% alert title="Note" color="note" %}}

At least one of these attributes must be supplied for your `fake` arm to work.
If neither are specified, an error is thrown asking for specification.
If both attributes are specified, an error is thrown, stating "can only populate either ArmModel or ModelPath - not both".

{{% /alert %}}

{{< tabs name="Configuration with arm-model or model-path" >}}
{{% tab name="arm-model JSON Example" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<arm-name">",
    "type": "arm",
    "model": "fake",
    "attributes": {
        "arm-model": "ur5e"
    }
}
```

{{% /tab %}}
{{% tab name="model-path JSON Example" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<arm-name">",
    "type": "arm",
    "model": "fake",
    "attributes": {
        "model-path": "components/arm/universalrobots/ur5e.json"
    }
}
```

{{% /tab %}}
{{< /tabs >}}
