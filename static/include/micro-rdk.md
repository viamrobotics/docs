{{% alert title="ALPHA" color="note" %}}
The micro-RDK is in alpha mode and many features supported by the RDK are still being added to the micro-RDK.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

The micro-RDK is a lightweight version of the {{% glossary_tooltip term_id="rdk" text="Robot Development Kit (RDK)"%}} which can run on resource-limited embedded systems.

The only microcontroller the micro-RDK currently supports is the [ESP32](https://www.espressif.com/en/products/socs/esp32).

The micro-RDK currently only supports client API integration for the following resources:

- [GPIO Pin](/components/board/#gpiopin-api)
- Analog readers
- Motors
- Encoders
- [Base](/components/base/)

See [GitHub](https://github.com/viamrobotics/micro-rdk) for code examples and more information about the micro-RDK.
