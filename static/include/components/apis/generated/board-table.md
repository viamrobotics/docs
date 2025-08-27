<!-- prettier-ignore -->
| Method Name | Description | `viam-micro-server` Support |
| ----------- | ----------- | --------------------------- |
| [`SetGPIO`](/dev/reference/apis/components/board/#setgpio) | Set the digital signal output of this pin to low (0V) or high (active, >0V). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetGPIO`](/dev/reference/apis/components/board/#getgpio) | Get if the digital signal output of this pin is high (active, >0V). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetPWM`](/dev/reference/apis/components/board/#getpwm) | Get the pin's pulse-width modulation (PWM) duty cycle: a float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state (active, >0V) relative to the interval period of the PWM signal (interval period being the mathematical inverse of the PWM frequency). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`SetPWM`](/dev/reference/apis/components/board/#setpwm) | Set the pin's Pulse-width modulation (PWM) duty cycle: a float [`0.0`, `1.0`] indicating the percentage of time the digital signal output of this pin is in the high state (active, >0V) relative to the interval period of the PWM signal (interval period being the mathematical inverse of the PWM frequency). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`PWMFrequency`](/dev/reference/apis/components/board/#pwmfrequency) | Get the PWM frequency of the GPIO pin. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`SetPWMFrequency`](/dev/reference/apis/components/board/#setpwmfrequency) | Set the pin to the given PWM `frequency` (in Hz). When `frequency` is 0, it will use the board’s default PWM frequency. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetDigitalInterruptValue`](/dev/reference/apis/components/board/#getdigitalinterruptvalue) | Get the current value of a configured digital interrupt. |  |
| [`ReadAnalogReader`](/dev/reference/apis/components/board/#readanalogreader) | Read the current integer value of the digital signal output by the ADC. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`WriteAnalog`](/dev/reference/apis/components/board/#writeanalog) | Write an analog value to a pin on the board. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`StreamTicks`](/dev/reference/apis/components/board/#streamticks) | Start a stream of `DigitalInterrupt` ticks. |  |
| [`SetPowerMode`](/dev/reference/apis/components/board/#setpowermode) | Set the board to the indicated `PowerMode`. |  |
| [`AnalogByName`](/dev/reference/apis/components/board/#analogbyname) | Get a configured `Analog` by `name`. |  |
| [`DigitalInterruptByName`](/dev/reference/apis/components/board/#digitalinterruptbyname) | Get a DigitalInterrupt by `name`. |  |
| [`GPIOPinByName`](/dev/reference/apis/components/board/#gpiopinbyname) | Get a `GPIOPin` by {{< glossary_tooltip term_id="pin-number" text="pin number" >}}. |  |
| [`GetGeometries`](/dev/reference/apis/components/board/#getgeometries) | Get all the geometries associated with the board in its current configuration, in the frame of the board. |  |
| [`Reconfigure`](/dev/reference/apis/components/board/#reconfigure) | Reconfigure this resource. |  |
| [`DoCommand`](/dev/reference/apis/components/board/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetResourceName`](/dev/reference/apis/components/board/#getresourcename) | Get the `ResourceName` for this board. |  |
| [`Close`](/dev/reference/apis/components/board/#close) | Safely shut down the resource and prevent further use. |  |
