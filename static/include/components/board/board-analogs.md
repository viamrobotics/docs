An [analog-to-digital converter](https://www.electronics-tutorials.ws/combination/analogue-to-digital-converter.html) (ADC) takes a continuous voltage input (analog signal) and converts it to an discrete integer output (digital signal).

ADCs are useful when building a robot, as they enable your board to read the analog signal output by most types of [sensors](/components/sensor/) and other hardware components.

To integrate an ADC into your machine, you must first physically connect the pins on your ADC to your board.

Then, integrate `analogs` into the `attributes` of your board by following the **Config Builder** instructions or by adding the following to your board's JSON configuration:

{{< tabs name="Configure an Analog Reader" >}}
{{% tab name="Config Builder" %}}

On your board's panel, click **Show more**, then select **Add analog**.
Assign a name to your analog and then fill in the required properties outlined below.

![An example configuration for analogs in the Viam app Config Builder.](/components/board/analogs-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
"analogs": [
  {
    "name": "<your-analog-reader-name>",
    "pin": "<pin-number-on-adc>",
    "spi_bus": "<your-spi-bus-index>",
    "chip_select": "<chip-select-index>",
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
            "spi_bus": "1",
            "chip_select": "0"
          },
          {
            "name": "pressure",
            "pin": "0",
            "spi_bus": "1",
            "chip_select": "0"
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
|`spi_bus` | string | **Required** | The index of the SPI bus connecting the ADC and board. |
| `average_over_ms` | int | Optional | Duration in milliseconds over which the rolling average of the analog input should be taken. |
|`samples_per_sec` | int | Optional | Sampling rate of the analog input in samples per second. |

#### Test `analogs`

Once you have configured your analogs, navigate to the **CONTROL** tab to monitor analog values.
The numbers displayed next to each analog name represent the digital signal received from the analog inputs.

![Analogs in the control tab.](/components/board/analogs-control-tab.png)
