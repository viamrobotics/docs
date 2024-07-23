<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`AnalogByName`](/components/board/#analogbyname) | Get an [`Analog`](#analogs) by `name`.
[`GetDigitalInterruptValue`](/components/board/#getdigitalinterruptvalue) | Get a [`DigitalInterrupt`](#digital_interrupts) by `name`.
[`GetGPIO`](/components/board/#getgpio) | Get a `GPIOPin` by its {{< glossary_tooltip term_id="pin-number" text="pin number" >}}.
[`SetGPIO`](/components/board/#setgpio) | Set a `GPIOPin` by its {{< glossary_tooltip term_id="pin-number" text="pin number" >}}.
[`AnalogNames`](/components/board/#analognames) | Get the `name` of every [`Analog`](#analogs).
[`DigitalInterruptNames`](/components/board/#digitalinterruptnames) | Get the `name` of every [`DigitalInterrupt`](#digital_interrupts).
[`SetPWM`](/components/board/#setpwm) | Set the board to the indicated power mode.
[`StreamTicks`](/components/board/#streamticks) | Start a stream of [`DigitalInterrupt`](#digital_interrupts) ticks.
[`GetGeometries`](/components/board/#getgeometries) | Get all the geometries associated with the board in its current configuration, in the [frame](/services/frame-system/) of the board.
[`DoCommand`](/components/board/#docommand) | Send or receive model-specific commands.
[`Close`](/components/board/#close) | Safely shut down the resource and prevent further use.
