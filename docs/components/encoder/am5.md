---
title: "Configure an AM5-AS5048 encoder"
linkTitle: "AM5-AS5048"
type: "docs"
description: "Configure an AM5-AS5048 encoder."
tags: ["encoder", "components"]
# SMEs: Rand
---

The [`AM5-AS5048`](https://ams.com/en/as5048a) encoder is an absolute encoder that uses an I2C or SPI interface to connect.
This model supports the [AS5048A](https://ams.com/en/as5048a) sensor.

## Dependencies

1. To configure an AM5-AS5048 encoder, you must configure an I2C bus on your [board](../../board):

    ```json-viam
    {
          "name": "<board_name>",
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

2. Any motors using the `AM5-AS5048` encoder must set `ticks_per_rotation` to `1`.
   This is because the AM5 encoder is an absolute encoder which provides angular measurements directly.

## Configuration

{{< tabs name="Configure an AM5-AS5048 Encoder" >}}
{{< tab name="Config Builder" >}}

<br>
On the <b>COMPONENTS</b> subtab, navigate to the <b>Create Component</b> menu.
Enter a name for your encoder, select the type <code>encoder</code>, and select the <code>AM5-AS5048</code> model.
<br>
<img src="../img/create-am5.png" alt="Creation of an AM5 encoder in the Viam app config builder." style="max-width:600px" />
<br>
Fill in the attributes for your encoder:
<br>
<img src="../img/configure-am5.png" alt="Configuration of an AM5 encoder in the Viam app config builder." />
<br>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam {class="line-numbers linkable-line-numbers"}
{
    "name": "<encoder_name>",
    "type": "encoder",
    "model" : "AM5-AS5048",
    "attributes": {
      "board": "<board_name>",
      "connection_type": "i2c",
      "i2c_attributes": {
        "i2c_bus": <string>,
        "i2c_addr": <integer>
      }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for AM5-AS5048 encoders:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `board` | *Required* | The name of the board to which the encoder is connected. |
| `connection_type` | *Required* | Use `"i2c"`. |
| `i2c_attributes` | *Required* | The attributes to configure i2c connection: <ul> <li> <code>i2c_bus</code>: The name of the bus that was added to the board. Example: `"main"`. </li> <li> <code>i2c_addr</code>: The address of the bus. Example: `64`. </li> </ul> |

### Configure a SCUTTLE bot

If you are configuring a SCUTTLE bot, you must:

- Specify the bus number on the board as `"1"`.

  ```json-viam
  {
        "name": "<board_name>",
        "type": "board",
        "model": "<model_name>"
        "attributes": {
          "i2cs": [
            {
              "bus": "1",
              "name": "<main>"
            }
          ]
        },
        "depends_on": [],
  }
  ```

- Configure the left and right encoders as follows:

  - left:

    ```json
    {
      "board": "<board_name>",
      "connection_type": "i2c",
      "i2c_attributes": {
        "i2c_bus": "main",
        "i2c_addr": 64
      }
    }
    ```

  - right:

    ```json
    {
      "board": "<board_name>",
      "connection_type": "i2c",
      "i2c_attributes": {
        "i2c_bus": "main",
        "i2c_addr": 65
      }
    }
    ```
