{{% alert title="ALPHA" color="note" %}}
The micro-RDK is in alpha mode and many features supported by the RDK are still being added to the micro-RDK.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

The micro-RDK is a lightweight version of the {{% glossary_tooltip term_id="rdk" text="Robot Development Kit (RDK)"%}} which can run on resource-limited embedded systems.

The only microcontroller the micro-RDK currently supports is the [ESP32](https://www.espressif.com/en/products/socs/esp32).

To use Viam on a microcontroller, you need to both:

- Run the micro-RDK on your microcontroller
- Run the full-featured `viam-server` on another machine

To run both the micro-RDK and `viam-server`, you currently need two robots: one controlling robot which runs `viam-server` and a worker robot which runs the micro-RDK on your microcontroller.
This second "robot" can be as simple as an instance of `viam-server` running on your development machine.

{{< imgproc alt="The control robot runs viam-server and connects to the microcontroller which runs the micro-RDK" src="/installation/microcontroller/micro-rdk-overview.png" resize="800x" declaredimensions=true >}}

The micro-RDK currently only supports:

- GPIO pins
- Analog readers
- Motors
- Encoders

See [GitHub](https://github.com/viamrobotics/micro-rdk) for code examples and more information about the micro-RDK.
