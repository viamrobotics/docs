[Interrupts](https://en.wikipedia.org/wiki/Interrupt) are a method of signaling precise state changes.
Configuring digital interrupts to monitor GPIO pins on your board is useful when your application needs to know precisely when there is a change in GPIO value between high and low.

- When an interrupt configured on your board processes a change in the state of the GPIO pin it is configured to monitor, it calls [`Tick()`](/components/board/#tick) to record the state change and notify any interested [callbacks](/components/board/#addcallback) to "interrupt" the program.
- Calling [`GetGPIO()`](/components/board/#getgpio) on a GPIO pin, which you can do without configuring interrupts, is useful when you want to know a pin's value at specific points in your program, but is less precise and convenient than using an interrupt.

Integrate `digital_interrupts` into your machine in the `attributes` of your board by adding the following to your board's JSON configuration:

{{< tabs name="Configure a Digital Interrupt" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
"digital_interrupts": [
  {
    "name": "<your-digital-interrupt-name>",
    "pin": "<pin-number>",
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
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following properties are available for `digital_interrupts`:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`name` | string | **Required** | Your name for the digital interrupt. |
|`pin`| string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the board's GPIO pin that you wish to configure the digital interrupt for. |
|`type`| string | Optional | _Only applies to `pi` model boards._ <ul><li>`basic`: Recommended. Tracks interrupt count. </li> <li>`servo`: For interrupts configured for a pin controlling a [servo](/components/servo/). Tracks pulse width value. </li></ul> |
