An [analog-to-digital converter](https://www.electronics-tutorials.ws/combination/analogue-to-digital-converter.html) (ADC) takes a continuous voltage input (analog signal) and converts it to an discrete integer output (digital signal).

ADCs are useful when building a robot, as they enable your board to read the analog signal output by most types of [sensors](/platform/build/configure/components/sensor/) and other hardware components.

To integrate an ADC into your robot, you must first physically connect the pins on your ADC to your board.
If your ADC communicates with your board using [SPI](/platform/build/configure/components/board/#spis), you need to wire and configure the SPI bus in addition to the `analogs`.

Then, integrate `analogs` into the `attributes` of your board by adding the following to your board's JSON configuration:

{{< tabs name="Configure an Analog Reader" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
"analogs": [
  {
    "chip_select": "<chip-select-pin-number-on-board>",
    "name": "<your-analog-reader-name>",
    "pin": "<pin-number-on-adc>",
    "spi_bus": "<your-spi-bus-name>",
    "average_over_ms": <int>,
    "samples_per_sec": <int>
  }
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "model": "pi",
      "name": "your-board",
      "type": "board",
      "attributes": {
        "analogs": [
          {
            "chip_select": "24",
            "name": "current",
            "pin": "1",
            "spi_bus": "main"
          },
          {
            "chip_select": "24",
            "name": "pressure",
            "pin": "0",
            "spi_bus": "main"
          }
        ],
        "spis": [
          {
            "bus_select": "0",
            "name": "main"
          }
        ]
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following properties are available for `analogs`:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`name` | string | **Required** | Your name for the analog reader. |
|`pin`| string | **Required** | The pin number of the ADC's connection pin, wired to the board. This should be labeled as the physical index of the pin on the ADC.
|`chip_select`| string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the board's connection pin, wired to the ADC. |
|`spi_bus` | string | Optional | The `name` of the SPI bus connecting the ADC and board. Required if your board must communicate with the ADC with the SPI protocol. |
| `average_over_ms` | int | Optional | Duration in milliseconds over which the rolling average of the analog input should be taken. |
|`samples_per_sec` | int | Optional | Sampling rate of the analog input in samples per second. |
