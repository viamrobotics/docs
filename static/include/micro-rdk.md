{{% alert title="ALPHA" color="note" %}}
The micro-RDK is in alpha mode and many features supported by the RDK are still being added to the micro-RDK.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

The micro-RDK is a lightweight version of the {{% glossary_tooltip term_id="rdk" text="Robot Development Kit (RDK)"%}} which can run on resource-limited embedded systems that can not run the fully-featured [`viam-server`](/viam/).

The only microcontroller the micro-RDK currently supports is the [ESP32](https://www.espressif.com/en/products/socs/esp32).

[Client API](/program/apis/) usage with the Micro-RDK is currently limited to the following supported {{< glossary_tooltip term_id="resource" text="resources" >}}:

- [Motor](/components/motor/)
- [Encoder](/components/encoder/)
- [Base](/components/base/)
- [GPIO Pin](/components/board/#gpiopin-api)
- [Analog Reader](/components/board/#analogreader-api)

See [GitHub](https://github.com/viamrobotics/micro-rdk) for code examples and more information on the micro-RDK.
