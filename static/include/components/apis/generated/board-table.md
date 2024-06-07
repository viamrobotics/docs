<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`SetGPIO`](/components/board/#setgpio) | Set the digital signal output of this pin to low (0V) or high (active, >0V). |
| [`GetGPIO`](/components/board/#getgpio) | Get if the digital signal output of this pin is high (active, >0V). |
| [`GetPWM`](/components/board/#getpwm) | Get the pin's pulse-width modulation (PWM) duty cycle: a float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state (active, >0V) relative to the interval period of the PWM signal (interval period being the mathematical inverse of the PWM frequency). |
| [`SetPWM`](/components/board/#setpwm) | Set the pin's Pulse-width modulation (PWM) duty cycle: a float [`0.0`, `1.0`] indicating the percentage of time the digital signal output of this pin is in the high state (active, >0V) relative to the interval period of the PWM signal (interval period being the mathematical inverse of the PWM frequency). |
| [`PWMFrequency`](/components/board/#pwmfrequency) | Get the PWM frequency of the GPIO pin. |
| [`SetPWMFrequency`](/components/board/#setpwmfrequency) | Set the pin to the given PWM `frequency` (in Hz). When `frequency` is 0, it will use the board’s default PWM frequency. |
| [`AnalogByName`](/components/board/#analogbyname) | Get an `AnalogReader` by `name`. |
| [`Write`](/components/board/#write) | Write an analog value to a pin on the board. |
| [`GetDigitalInterruptValue`](/components/board/#getdigitalinterruptvalue) | Get an `DigitalInterrupt` by `name`. |
| [`StreamTicks`](/components/board/#streamticks) | Start a stream of `DigitalInterrupt` ticks. |
| [`SetPowerMode`](/components/board/#setpowermode) | Set the board to the indicated `PowerMode`. |
| [`GetGeometries`](/components/board/#getgeometries) | Get all the geometries associated with the board in its current configuration, in the frame of the board. |
| [`Read`](/components/board/#read) | Read the current integer value of the digital signal output by the ADC. |
| [`Value`](/components/board/#value) | Get the current value of this interrupt. |
| [`AnalogReaderNames`](/components/board/#analogreadernames) | Get the name of every `AnalogReader` configured and residing on the board. |
| [`DigitalInterruptNames`](/components/board/#digitalinterruptnames) | Get the name of every `DigitalInterrupt` configured on the board. |
| [`GPIOPinByName`](/components/board/#gpiopinbyname) | Get a `GPIOPin` by {{< glossary_tooltip term_id="pin-number" text="pin number" >}}. |
| [`Reconfigure`](/components/board/#reconfigure) | Reconfigure this resource. |
| [`DoCommand`](/components/board/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. |
| [`Close`](/components/board/#close) | Safely shut down the resource and prevent further use. |
