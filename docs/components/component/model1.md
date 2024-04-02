---
title: "Configure a Model1"
linkTitle: "Model1"
weight: 12
type: "docs"
description: "Configure a model1 arm."
images: ["/icons/components.png"]
tags: ["name", "components"]
draft: true
# SMEs:
---

The `model1` arm model supports the XYZ unit made by Some Company(INSERT LINK AS APPLICABLE).
Optional additional description/information.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `arm` type, then select the `model1` model.
Enter a name for your arm and click **Create**.

{{< imgproc src="/components/component/model1-builder.png" alt="Creation of a `model1` arm in the Viam app config builder." resize="600x" >}}

Edit and fill in the attributes as applicable.

<!-- If the model does not have a fancy config UI available, such that the user needs to write JSON attributes, refer to one of the other component models as an example. You should include easily copy-pastable attribute templates on the config tab. For example, replace "Edit and fill in the attributes as applicable." with the following:

Copy and paste the following attribute template into your COMPONENT's **Attributes** box.
Then remove and fill in the attributes as applicable to your COMPONENT, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "stream": "<color|depth>",
  "url": "<URL>",
  "intrinsic_parameters": {
    "width_px": <int>,
    "height_px": <int>,
    "fx": <float>,
    "fy": <float>,
    "ppx": <float>,
    "ppy": <float>
  },
  "distortion_parameters": {
    "rk1": <float>,
    "rk2": <float>,
    "rk3": <float>,
    "tp1": <float>,
    "tp2": <float>
  },
  "debug": <boolean>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "stream": "color",
  "url": "http://urltogetstreamingimagedatafrom"
}
```

{{% /tab %}}
{{< /tabs >}}
-->

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": <arm_name>,
      "model": "model1",
      "type": "arm",
      "namespace": "rdk",
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
      "model": "model1",
      "type": "arm",
      "namespace": "rdk",
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

<!-- prettier-ignore -->
| Name         | Inclusion    | Type   | Default Value | Description                                                                                                                                                                                      |
| ------------ | ------------ | ------ | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `board`      | **Required** | string | -             | The name of the board to which the device is wired.                                                                                                                                              |
| `i2c_bus`    | **Required** | string | -             | The name of the I<sup>2</sup>C bus through which the device communicates with the SBC. Note that this must match the name you gave the I<sup>2</sup>C bus you configured in the board component. |
| `attribute3` | Optional     | int    | 300           | Insert useful description here.                                                                                                                                                                  |

## Test the component

After you configure your compontent, navigate to the [**CONTROL** tab](/fleet/machines/#control) and select the **Component** dropdown panel.

Then _explain how to interact with the panel_.

{{<imgproc src="/components/sensor/sensor-control-tab.png" resize="800x" declaredimensions=true alt="Image or GIF of the control tab">}}
