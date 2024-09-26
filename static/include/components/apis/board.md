<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`AnalogByName`](/appendix/apis/components/board/#analogbyname) | Get a configured `Analog` by `name`.
[`GetDigitalInterruptValue`](/appendix/apis/components/board/#getdigitalinterruptvalue) | Get a `DigitalInterrupt` by `name`.
[`GetGPIO`](/appendix/apis/components/board/#getgpio) | Get a `GPIOPin` by its {{< glossary_tooltip term_id="pin-number" text="pin number" >}}.
[`SetGPIO`](/appendix/apis/components/board/#setgpio) | Set a `GPIOPin` by its {{< glossary_tooltip term_id="pin-number" text="pin number" >}}.
[`AnalogNames`](/appendix/apis/components/board/#analognames) | Get the `name` of every configured `Analog`.
[`DigitalInterruptNames`](/appendix/apis/components/board/#digitalinterruptnames) | Get the `name` of every configured `DigitalInterrupt`.
[`SetPWM`](/appendix/apis/components/board/#setpwm) | Set the board to the indicated power mode.
[`StreamTicks`](/appendix/apis/components/board/#streamticks) | Start a stream of configured `DigitalInterrupt` ticks.
[`GetGeometries`](/appendix/apis/components/board/#getgeometries) | Get all the geometries associated with the board in its current configuration, in the [frame](/services/frame-system/) of the board.
[`DoCommand`](/appendix/apis/components/board/#docommand) | Send or receive model-specific commands.
[`Close`](/appendix/apis/components/board/#close) | Safely shut down the resource and prevent further use.
