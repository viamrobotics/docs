[Serial Peripheral Interface (SPI)](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) is a serial communication protocol that uses four [signal wires](https://learn.sparkfun.com/tutorials/serial-peripheral-interface-spi) to exchange information between a controller and peripheral devices:

- Main Out/Secondary In: MOSI
- Main In/Secondary Out: MISO
- Clock, an oscillating signal line: SCLK
- Chip Select, with 1 line for each peripheral connected to controller: CS\*

To connect your board (controller) and a [component](/build/configure/components/) that requires SPI communication (peripheral device), wire a connection between CS and MOSI/MISO/SLCK pins on the board and component.

{{% alert title="Important" color="note" %}}

You must also enable SPI on your board if it is not enabled by default.
See your [board model's configuration instructions](/build/configure/components/board/#supported-models) if applicable.

{{% /alert %}}

As supported boards have CS pins internally configured to correspond with SPI bus indices, you can enable this connection in your board's configuration by specifying the index of the bus at your CS pin's location and giving it a name.

Integrate `spis` into your robot in the `attributes` of your board by adding the following to your board's JSON configuration:

{{< tabs name="Configure a SPI Bus" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
"spis": [
  {
    "name": "<your-bus-name>",
    "bus_select": "<your-bus-index>"
  }
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"spis": [
  {
    "name": "main",
    "bus_select": "0"
  }
]
```

{{% /tab %}}
{{< /tabs >}}

The following properties are available for `spis`:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`name`| string | **Required** | The `name` of the SPI bus. |
|`bus_select`| string | **Required** | The index of the SPI bus. |

{{% alert title="WIRING WITH SPI" color="tip" %}}

Refer to your board's pinout diagram or data sheet for SPI bus indexes and corresponding CS/MOSI/MISO/SCLK {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}}.

Refer to your peripheral device's data sheet for CS/MOSI/MISO/SLCK pin layouts.

{{% /alert %}}
