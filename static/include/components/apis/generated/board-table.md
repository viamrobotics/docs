<!-- prettier-ignore -->
| Method Name | Description | `viam-micro-server` Support |
| ----------- | ----------- | --------------------------- |
| [`SetGPIO`](/appendix/apis/components/board/#setgpio) | Set the digital signal output of this pin to low (0V) or high (active, >0V). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetGPIO`](/appendix/apis/components/board/#getgpio) | Get if the digital signal output of this pin is high (active, >0V). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetPWM`](/appendix/apis/components/board/#getpwm) | Get the pin's pulse-width modulation (PWM) duty cycle: a float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state (active, >0V) relative to the interval period of the PWM signal (interval period being the mathematical inverse of the PWM frequency). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`SetPWM`](/appendix/apis/components/board/#setpwm) | Set the pin's Pulse-width modulation (PWM) duty cycle: a float [`0.0`, `1.0`] indicating the percentage of time the digital signal output of this pin is in the high state (active, >0V) relative to the interval period of the PWM signal (interval period being the mathematical inverse of the PWM frequency). | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`PWMFrequency`](/appendix/apis/components/board/#pwmfrequency) | Get the PWM frequency of the GPIO pin. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`SetPWMFrequency`](/appendix/apis/components/board/#setpwmfrequency) | Set the pin to the given PWM `frequency` (in Hz). When `frequency` is 0, it will use the board’s default PWM frequency. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`AnalogByName`](/appendix/apis/components/board/#analogbyname) | Get a configured `Analog` by `name`. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`Write`](/appendix/apis/components/board/#write) | Write an analog value to a pin on the board. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`GetDigitalInterruptValue`](/appendix/apis/components/board/#getdigitalinterruptvalue) | Get a configured `DigitalInterrupt` by `name`. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`StreamTicks`](/appendix/apis/components/board/#streamticks) | Start a stream of `DigitalInterrupt` ticks. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`SetPowerMode`](/appendix/apis/components/board/#setpowermode) | Set the board to the indicated `PowerMode`. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`GetGeometries`](/appendix/apis/components/board/#getgeometries) | Get all the geometries associated with the board in its current configuration, in the frame of the board. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`Read`](/appendix/apis/components/board/#read) | Read the current integer value of the digital signal output by the ADC. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`Value`](/appendix/apis/components/board/#value) | Get the current value of this interrupt. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`DigitalInterruptNames`](/appendix/apis/components/board/#digitalinterruptnames) | Get the name of every configured `DigitalInterrupt` on the board. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`GPIOPinByName`](/appendix/apis/components/board/#gpiopinbyname) | Get a `GPIOPin` by {{< glossary_tooltip term_id="pin-number" text="pin number" >}}. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`Reconfigure`](/appendix/apis/components/board/#reconfigure) | Reconfigure this resource. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`DoCommand`](/appendix/apis/components/board/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| [`Name`](/appendix/apis/components/board/#name) | Get the name of the digital interrupt. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`GetResourceName`](/appendix/apis/components/board/#getresourcename) | Get the `ResourceName` for this board with the given name. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
| [`Close`](/appendix/apis/components/board/#close) | Safely shut down the resource and prevent further use. | <p class="center-text"><i class="fas fa-times" title="no"></i></p> |
