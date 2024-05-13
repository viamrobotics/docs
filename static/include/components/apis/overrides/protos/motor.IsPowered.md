Returns whether or not the motor is currently running, and the portion of max power (between 0 and 1; if the motor is off the power will be 0).
Stepper motors will report `true` if they are being powered while holding a position, as well as when they are turning.
