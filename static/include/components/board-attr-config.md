Copy and paste the following attribute template into your board's **Attributes** box.
Then remove and fill in the attributes as applicable to your board, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "analogs": [
    {
      "chip_select": "<chip-select-pin-number-on-board>",
      "name": "<your-analog-reader-name>",
      "pin": "<pin-number-on-adc>",
      "spi_bus": "<your-spi-bus-name>",
      "average_over_ms": <int>,
      "samples_per_sec": <int>
    }
  ],
  "digital_interrupts": [
    {
      "name": "<your-digital-interrupt-name>",
      "pin": "<pin-number>",
      "type": "< basic | servo >"
    }
  ],
  "spis": [
    {
      "name": "<your-bus-name>",
      "bus_select": "<your-bus-index>"
    }
  ],
  "i2cs": [
    {
      "name": "<your-bus-name>",
      "bus": "<your-bus-index>"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "digital_interrupts": [
    {
      "name": "your-interrupt-1",
      "pin": "15"
    },
    {
      "name": "your-interrupt-2",
      "pin": "16"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}
