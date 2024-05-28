---
title: "Configure an AMS-AS5048 Encoder"
linkTitle: "AMS-AS5048"
type: "docs"
description: "Configure an AMS-AS5048 encoder."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components"]
aliases:
  - "/components/encoder/ams-as5048/"
component_description: "The AMS-AS5048 encoder is an absolute encoder that which can connect using an I2C interface."
# SMEs: Rand
---

The `AMS-AS5048` encoder model supports AMS's [AS5048](https://ams.com/en/as5048a) encoder.
This is an absolute encoder that uses an I<sup>2</sup>C or SPI interface to connect.

{{% alert title="Important" color="note" %}}
Any [motor](/components/motor/) using the `AMS-AS5048` encoder must have its `ticks_per_rotation` attribute configured as `1` because this encoder provides angular measurements directly.
{{% /alert %}}

{{< tabs name="Configure an AMS-AS5048 Encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `encoder` type, then select the `AMS-AS5048` model.
Enter a name or use the suggested name for your encoder and click **Create**.

![Configuration of an AS5048 encoder in the Viam app config builder.](/components/encoder/configure-ams.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-encoder-name>",
  "model": "AMS-AS5048",
  "type": "encoder",
  "namespace": "rdk",
  "attributes": {
    "connection_type": "i2c",
    "i2c_attributes": {
      "i2c_bus": "<your-i2c-bus-index-on-board>",
      "i2c_addr": <int>
    }
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `AMS-AS5048` encoders:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `connection_type` | string | **Required** | Use `"i2c"`. |
| `i2c_attributes` | object | **Required** | The attributes to configure the I<sup>2</sup>C connection: <ul> <li> <code>i2c_bus</code>: The index of the I<sup>2</sup>C bus on the [board](/components/board/) wired to this encoder. <br> Example: `"1"` </li> <li> <code>i2c_addr</code>: The address of the bus. <br> Example: `64` </li> </ul> |

{{< readfile "/static/include/components/test-control/encoder-control.md" >}}
