Move the servo to the desired angle in degrees.

{{% alert title="Stability Notice" color="note" %}}
Support for continuous servos with the GPIO servo model is experimental.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

If you are using a continuous rotation servo, you can use the `Move` command, but instead of moving to a given position, the servo will start moving at a set speed.

The speed will be related to the "angle" you pass in as a linear approximation.
90 degrees represents stop, 91 to 180 represents counter-clockwise rotation from slowest to fastest, and 89 to 1 represents clockwise from slowest to fastest.
It is recommended that you test your servo to determine the desired speed.

{{% /alert %}}
