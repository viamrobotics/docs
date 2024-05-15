[Interrupts](https://en.wikipedia.org/wiki/Interrupt) are a method of signaling precise state changes.
Configuring digital interrupts to monitor GPIO pins on your board is useful when your application needs to know precisely when there is a change in GPIO value between high and low.

- When an interrupt configured on your board processes a change in the state of the GPIO pin it is configured to monitor, it ticks to record the state change.
  You can stream these ticks with the board API's [`StreamTicks()`](/machine/components/board/#streamticks), or get the current value of the digital interrupt with [`Value()`](/machine/components/board/#value).
- Calling [`GetGPIO()`](/machine/components/board/#getgpio) on a GPIO pin, which you can do without configuring interrupts, is useful when you want to know a pin's value at specific points in your program, but is less precise and convenient than using an interrupt.

Integrate `digital_interrupts` into your machine in the `attributes` of your board by following the **Config Builder** instructions, or by adding the following to your board's JSON configuration:

{{< tabs name="Configure a Digital Interrupt" >}}
{{% tab name="Config Builder" %}}

On your board's panel, click **Show more**, then select **Add digital interrupt**.
Assign a name to your digital interrupt and then enter a pin number.

![An example configuration for digital interrupts in the Viam app Config Builder.](/machine/components/board/digital-interrupts-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
"digital_interrupts": [
  {
    "name": "<your-digital-interrupt-name>",
    "pin": "<pin-number>"
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
|`type`| string | Optional | _Only applies to `pi` model boards._ <ul><li>`basic`: Recommended. Tracks interrupt count. </li> <li>`servo`: For interrupts configured for a pin controlling a [servo](/machine/components/servo/). Tracks pulse width value. </li></ul> |

#### Test `digital_interrupts`

{{< readfile "/static/include/components/board/test-board-digital-interrupts.md" >}}
