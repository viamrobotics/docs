---
title: "Configure an arduino encoder"
linkTitle: "arduino"
type: "docs"
description: "Configure an arduino encoder."
images: ["/components/img/components/encoder.svg"]
tags: ["encoder", "components"]
draft: true
# SMEs: Rand
---

The `arduino` encoder requires configuring two pins on the board to which the encoder is wired.

{{< tabs name="Configure an arduino Encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your encoder, select the type `encoder`, and select the `arduino` model.

![Creation of an Arduino encoder in the Viam app config builder.](../img/create-arduino.png)

Click **Create component**.
Fill in the attributes for your encoder:

![Configuration of an Arduino encoder in the Viam app config builder.](../img/configure-arduino.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<your-encoder-name>",
    "type": "encoder",
    "model" : "arduino",
    "attributes": {
      "board": "<your-board-name>",
      "motor_name": "<motor_name>",
      "pins": {
        "a": <string>,
        "b": <string>
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `arduino` encoders:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | The `name` of the board to which the encoder is wired. |
| `motor_name` | string | **Required** | The `name` of the motor. |
| `pins` | **Required** | object | A struct holding the names of the pins wired to the encoder: <ul> <li> <code>a</code>: {{< glossary_tooltip term_id="pin-number" text="Pin number" >}} of one of the pins to which the encoder is wired. </li> <li> <code>b</code>: Required for two phase encoder. {{< glossary_tooltip term_id="pin-number" text="Pin number" >}} for the second board pin to which the encoder is wired. </li> </ul> |
