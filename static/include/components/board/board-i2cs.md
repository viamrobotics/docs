The [Inter-Integrated circuit (I<sup>2</sup>C)](https://learn.sparkfun.com/tutorials/i2c/all) serial communication protocol is similar to SPI, but requires two signal wires to exchange information between a controller and a peripheral device:

- Serial Data: SDA
- Serial Clock: SCL

To connect your board (controller) and a [component](/components/) that requires I<sup>2</sup>C communication (peripheral device), wire a connection between SDA and SCL pins on the board and component.

{{% alert title="Important" color="note" %}}

You must also enable I<sup>2</sup>C on your board if it is not enabled by default.
See your [board model's configuration instructions](/components/board/#supported-models) if applicable.

{{% /alert %}}

As supported boards have SDA and SCL pins internally configured to correspond with I<sup>2</sup>C bus indices, you can enable this connection in your board's configuration by specifying the index of the bus and giving it a name.

Integrate `i2cs` into your robot in the `attributes` of your board as follows:

{{< tabs name="Configure i2cs" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
{
  "i2cs": [
    {
      "name": "<your-bus-name>",
      "bus": "<your-bus-index>"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
{
  "i2cs": [
    {
      "name": "bus1",
      "bus": "1"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following properties are available for `i2cs`:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`name`| string| **Required** | `name` of the I<sup>2</sup>C bus. |
|`bus`| string | **Required** | The index of the I<sup>2</sup>C bus. |

{{% alert title="WIRING WITH I<sup>2</sup>C" color="tip" %}}

Refer to your board's pinout diagram or data sheet for I<sup>2</sup>C bus indexes and corresponding SDA/SCL {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}}.

Refer to your peripheral device's data sheet for SDA/SCL pin layouts.

{{% /alert %}}
