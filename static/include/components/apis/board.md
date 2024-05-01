<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`AnalogByName`](/components/board/#analogbyname) | Get an [`Analog`](/components/board/#analogs) by `name`.
[`GetDigitalInterruptValue`](/components/board/#getdigitalinterruptvalue) | Get a [`DigitalInterrupt`](/components/board/#digital_interrupts) by `name`.
[`GetGPIO`](/components/board/#getgpio) | Get a `GPIOPin` by its {{< glossary_tooltip term_id="pin-number" text="pin number" >}}.
[`SetGPIO`](/components/board/#setgpio) | Set a `GPIOPin` by its {{< glossary_tooltip term_id="pin-number" text="pin number" >}}.
[`AnalogNames`](/components/board/#analognames) | Get the `name` of every [`Analog`](/components/board/#analogs).
[`DigitalInterruptNames`](/components/board/#digitalinterruptnames) | Get the `name` of every [`DigitalInterrupt`](/components/board/#digital_interrupts).
[`SetPWM`](/components/board/#setpwm) | Set the board to the indicated power mode.
[`WriteAnalog`](/components/board/#writeanalog) | Write an analog value to a pin on the board.
[`StreamTicks`](/components/board/#streamticks) | Start a stream of [`DigitalInterrupt`](/components/board/#digital_interrupts) ticks.
[`GetGeometries`](/components/board/#getgeometries) | Get all the geometries associated with the board in its current configuration, in the [frame](/mobility/frame-system/) of the board.
[`DoCommand`](/components/board/#docommand) | Send or receive model-specific commands.
[`Close`](/components/board/#close) | Safely shut down the resource and prevent further use.
