<!-- prettier-ignore -->
| Method Name | Description | micro-RDK Support |
| ----------- | ----------- | ----------------- |
| [`SetGPIO`](/components/board/#setgpio) | Set the digital signal output of this pin to low (0V) or high (active, >0V). | Yes |
| [`GetGPIO`](/components/board/#getgpio) | Get if the digital signal output of this pin is high (active, >0V). | Yes |
| [`GetPWM`](/components/board/#getpwm) | Get the pin's pulse-width modulation (PWM) duty cycle: a float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state (active, >0V) relative to the interval period of the PWM signal (interval period being the mathematical inverse of the PWM frequency). | Yes |
| [`SetPWM`](/components/board/#setpwm) | Set the pin's Pulse-width modulation (PWM) duty cycle: a float [`0.0`, `1.0`] indicating the percentage of time the digital signal output of this pin is in the high state (active, >0V) relative to the interval period of the PWM signal (interval period being the mathematical inverse of the PWM frequency). | Yes |
| [`PWMFrequency`](/components/board/#pwmfrequency) | Get the PWM frequency of the GPIO pin. | Yes |
| [`SetPWMFrequency`](/components/board/#setpwmfrequency) | Set the pin to the given PWM `frequency` (in Hz). When `frequency` is 0, it will use the board’s default PWM frequency. | Yes |
| [`AnalogNames`](/components/board/#analognames) | Get the name of every `Analog` configured and residing on the board. | No |
| [`AnalogByName`](/components/board/#analogbyname) | Get an `Analog` by `name`. | No |
| [`Write`](/components/board/#write) | Write an analog value to a pin on the board. | Yes |
| [`GetDigitalInterruptValue`](/components/board/#getdigitalinterruptvalue) | Get an `DigitalInterrupt` by `name`. | No |
| [`StreamTicks`](/components/board/#streamticks) | Start a stream of `DigitalInterrupt` ticks. | No |
| [`SetPowerMode`](/components/board/#setpowermode) | Set the board to the indicated `PowerMode`. | No |
| [`GetGeometries`](/components/board/#getgeometries) | Get all the geometries associated with the board in its current configuration, in the frame of the board. | No |
| [`Read`](/components/board/#read) | Read the current integer value of the digital signal output by the ADC. | Yes |
| [`Value`](/components/board/#value) | Get the current value of this interrupt. | No |
| [`DigitalInterruptNames`](/components/board/#digitalinterruptnames) | Get the name of every `DigitalInterrupt` configured on the board. | No |
| [`GPIOPinByName`](/components/board/#gpiopinbyname) | Get a `GPIOPin` by {{< glossary_tooltip term_id="pin-number" text="pin number" >}}. | No |
| [`Reconfigure`](/components/board/#reconfigure) | Reconfigure this resource. | No |
| [`DoCommand`](/components/board/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. | Yes |
| [`FromRobot`](/components/board/#fromrobot) | Get the resource from the provided robot with the given name. | No |
| [`Name`](/components/board/#name) | Get the name of the digital interrupt. | No |
| [`GetResourceName`](/components/board/#getresourcename) | Get the `ResourceName` for this board with the given name. | No |
| [`Close`](/components/board/#close) | Safely shut down the resource and prevent further use. | No |
