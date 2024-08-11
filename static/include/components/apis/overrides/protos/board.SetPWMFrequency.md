Set the pin to the given PWM `frequency` (in Hz). When `frequency` is 0, it will use the board’s default PWM frequency.

{{< alert title="Note" color="note" >}}
If you attempt to set an unsupported PWM frequency on an `esp32`, the frequency will revert to the last valid frequency.
This may restart the PWM signal.
{{< /alert >}}
