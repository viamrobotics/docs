1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review this base model's documentation to ensure you have configured all required attributes.
1. Review your configuration for any motors that are components of the base.
Check that the names of the motor components match the list of motors you configured on the base.
1. If a motor is spinning in an unexpected direction, try using the `dir_flip` attribute in its config, or try swapping the wires running to the motor to change its direction.
1. Check that all wires are securely attached to the correct pins.
1. If you are using a battery to power the base, check that it is adequately charged.
   If the motors are drawing more power than the battery can supply, the single-board computer may be power cycling.
   Consider using a wall power supply for testing purposes to rule out this issue.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the base there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.