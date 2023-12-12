An [analog-to-digital converter](https://www.electronics-tutorials.ws/combination/analogue-to-digital-converter.html) (ADC) takes a continuous voltage input (analog signal) and converts it to an discrete integer output (digital signal).

ADCs are useful when building a robot, as they enable your board to read the analog signal output by most types of [sensors](/components/sensor/) and other hardware components.

To integrate an ADC into your robot, you must first physically connect the pins on your ADC to your board.

Then, integrate `analogs` into the `attributes` of your board by adding the following to your board's JSON configuration:

{{< tabs name="Configure an Analog Reader" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
"analogs": [
  {
    "name": "<your-analog-reader-name>",
    "pin": "<pin-number-on-adc>",
    "spi_bus": "<your-spi-bus-name>",
    "chip_select": "<chip-select-pin-number-on-board>",
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
            "name": "current",
            "pin": "1",
            "spi_bus": "main",
            "chip_select": "24"
          },
          {
            "name": "pressure",
            "pin": "0",
            "spi_bus": "main",
            "chip_select": "24"
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
|`chip_select`| string | **Required** | The chip select index of the board's connection pin, wired to the ADC. |
|`spi_bus` | string | Optional | The index of the SPI bus connecting the ADC and board. |
| `average_over_ms` | int | Optional | Duration in milliseconds over which the rolling average of the analog input should be taken. |
|`samples_per_sec` | int | Optional | Sampling rate of the analog input in samples per second. |
