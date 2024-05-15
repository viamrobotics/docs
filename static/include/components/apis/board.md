<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`ReadAnalog`](/machine/components/board/#readanalog) | Get an [`Analog`](/machine/components/board/#analogs) by `name`.
[`GetDigitalInterruptValue`](/machine/components/board/#getdigitalinterruptvalue) | Get a [`DigitalInterrupt`](/machine/components/board/#digital_interrupts) by `name`.
[`GetGPIO`](/machine/components/board/#getgpio) | Get a `GPIOPin` by its {{< glossary_tooltip term_id="pin-number" text="pin number" >}}.
[`SetGPIO`](/machine/components/board/#setgpio) | Set a `GPIOPin` by its {{< glossary_tooltip term_id="pin-number" text="pin number" >}}.
[`AnalogNames`](/machine/components/board/#analognames) | Get the `name` of every [`Analog`](/machine/components/board/#analogs).
[`DigitalInterruptNames`](/machine/components/board/#digitalinterruptnames) | Get the `name` of every [`DigitalInterrupt`](/machine/components/board/#digital_interrupts).
[`SetPWM`](/machine/components/board/#setpwm) | Set the board to the indicated power mode.
[`WriteAnalog`](/machine/components/board/#writeanalog) | Write an analog value to a pin on the board.
[`StreamTicks`](/machine/components/board/#streamticks) | Start a stream of [`DigitalInterrupt`](/machine/components/board/#digital_interrupts) ticks.
[`GetGeometries`](/machine/components/board/#getgeometries) | Get all the geometries associated with the board in its current configuration, in the [frame](/machine/services/frame-system/) of the board.
[`DoCommand`](/machine/components/board/#docommand) | Send or receive model-specific commands.
[`Close`](/machine/components/board/#close) | Safely shut down the resource and prevent further use.
