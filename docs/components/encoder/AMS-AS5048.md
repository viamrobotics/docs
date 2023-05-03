---
title: "Configure an AMS-AS5048 encoder"
linkTitle: "AMS-AS5048"
type: "docs"
description: "Configure an AMS-AS5048 encoder."
images: ["/components/img/components/encoder.svg"]
tags: ["encoder", "components"]
# SMEs: Rand
---

The `AMS-AS5048` encoder model supports AMS's [AS5048](https://ams.com/en/as5048a) encoder.
This is an absolute encoder that uses an I2C or SPI interface to connect.

To can configure the encoder, you must change some other configuration details:

1. You must configure an I2C bus on your [board](../../board):

    ```json
    {
          "name": "<your-board-name>",
          "type": "board",
          "model": "<model_name>"
          "attributes": {
            "i2cs": [
              {
                "bus": "<bus>",
                "name": "<bus_name>"
              }
            ]
          },
          "depends_on": [],
    }
    ```

2. Any motors using the `AMS-AS5048` encoder must set `ticks_per_rotation` to `1`.
   This is because the AS5048 encoder is an absolute encoder which provides angular measurements directly.

Now you can configure the encoder:

{{< tabs name="Configure an AMS-AS5048 Encoder" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your encoder, select the type `encoder`, and select the `AMS-AS5048` model.

![Creation of an AS5048 encoder in the Viam app config builder.](../img/create-am5.png)

Click **Create component**.
Fill in the attributes for your encoder:

![Configuration of an AS5048 encoder in the Viam app config builder.](../img/configure-am5.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<your-encoder-name>",
    "type": "encoder",
    "model" : "AMS-AS5048",
    "attributes": {
      "board": "<your-board-name>",
      "connection_type": "i2c",
      "i2c_attributes": {
        "i2c_bus": <string>,
        "i2c_addr": <int>
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `AMS-AS5048` encoders:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `board` | *Required* | The name of the board to which the encoder is connected. |
| `connection_type` | *Required* | Use `"i2c"`. |
| `i2c_attributes` | *Required* | The attributes to configure i2c connection: <ul> <li> <code>i2c_bus</code>: The name of the bus that was added to the board. Example: `"main"`. </li> <li> <code>i2c_addr</code>: The address of the bus. Example: `64`. </li> </ul> |
