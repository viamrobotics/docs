<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------- |
| `trigger_pin` | string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the [board's](/components/board/) GPIO pin that you have wired [the ultrasonic's trigger pin](https://www.sparkfun.com/products/15569) to. |
| `echo_interrupt_pin` | string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the pin [the ultrasonic's echo pin](https://www.sparkfun.com/products/15569) is wired to on the board. If you have already created a [digital interrupt](#digital_interrupts) for this pin in the [board's configuration](/components/board/), use that digital interrupt's `name` instead. |
| `board`  | string | **Required** | The `name` of the [board](/components/board/) the ultrasonic is wired to. |
| `timeout_ms`  | int | Optional | Time to wait in milliseconds before timing out of requesting to get ultrasonic distance readings. <br> Default: `1000`. |
