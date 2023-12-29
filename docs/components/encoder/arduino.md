---
title: "Configure an Arduino Encoder"
linkTitle: "arduino"
type: "docs"
description: "Configure an Arduino encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
draft: true
aliases:
  - /components/encoder/arduino/
# SMEs: Rand
---

{{< tabs name="Configure an arduino Encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `encoder` type, then select the `arduino` model.
Enter a name for your encoder and click **Create**.

![Configuration of an Arduino encoder in the Viam app config builder.](/components/encoder/configure-arduino.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "arduino",
  "type": "encoder",
  "namespace": "rdk",
  "attributes": {
    "board": "<your-board-name>",
    "motor_name": "your-motor-name>",
    "pins": {
      "a": "<pin-number-on-board>",
      "b": "<pin-number-on-board"
    }
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `arduino` encoders:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | The `name` of the board to which the encoder is wired. |
| `motor_name` | string | **Required** | The `name` of the motor. |
| `pins` | **Required** | object | A struct holding the names of the pins wired to the encoder: <ul> <li> <code>a</code>: {{< glossary_tooltip term_id="pin-number" text="Pin number" >}} of one of the pins to which the encoder is wired. </li> <li> <code>b</code>: Required for two phase encoder. {{< glossary_tooltip term_id="pin-number" text="Pin number" >}} for the second board pin to which the encoder is wired. </li> </ul> |
