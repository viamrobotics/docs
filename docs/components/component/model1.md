---
title: "Configure a Model1"
linkTitle: "Model1"
weight: 12
type: "docs"
description: "Configure a model1 arm."
tags: ["name", "components"]
draft: true
# SMEs:
---

The `model1` arm model supports the XYZ unit made by Some Company(INSERT LINK AS APPLICABLE).
Optional additional description/information.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** sub-tab and navigate to the **Create component** menu.
Enter a name for your arm, select the `arm` type, and select the `model1` model.

![Creation of a `model1` arm in the Viam app config builder.](../img/model1-builder.png)

Click **Create Component** and then fill in the attributes for your model.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <arm_name>,
      "type": "arm",
      "model": "model1",
      "attributes": {
        "board": <string>,
        "i2c_bus": <string>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "myArm",
      "type": "arm",
      "model": "model1",
      "attributes": {
        "board": "local",
        "i2c_bus": "1"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Annotated JSON" %}}

**Very optional**; probably don't bother making one if you don't already have one handy.

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `model1` arms:

Name | Inclusion | Type | Default Value | Description
---- | --------- | ---- | ------------- | -----------
`board` | **Required** | string | - | The name of the board to which the device is wired.
`i2c_bus` | **Required** | string | - | The name of the I<sup>2</sup>C bus through which the device communicates with the SBC. Note that this must match the name you gave the I<sup>2</sup>C bus you configured in the board component.
`attribute3` | Optional | int | 300 | Insert useful description here.
