{{% alert title="BETA" color="note" %}}
The micro-RDK is in beta mode and many features supported by the RDK are still being added to the micro-RDK.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

The micro-RDK is a lightweight version of the {{% glossary_tooltip term_id="rdk" text="Robot Development Kit (RDK)"%}} which can run on resource-limited embedded systems that cannot run the fully-featured [`viam-server`](/get-started/viam/).

The only microcontroller the micro-RDK currently supports is the [ESP32](https://www.espressif.com/en/products/socs/esp32).

[Client API](/program/apis/) usage with the micro-RDK currently supports the following {{< glossary_tooltip term_id="resource" text="resources" >}}:

{{< cards >}}
{{% card link="/micro-rdk/base/" %}}
{{% card link="/micro-rdk/board/" %}}
{{% card link="/micro-rdk/encoder/" %}}
{{% card link="/micro-rdk/movement-sensor/" %}}
{{% card link="/micro-rdk/motor/" %}}
{{% card link="/micro-rdk/sensor/" %}}
{{% card link="/micro-rdk/servo/" %}}
{{% card link="/micro-rdk/generic/" %}}
{{< /cards >}}

Click on each supported resource to see supported models, API methods, and configuration info.

See [GitHub](https://github.com/viamrobotics/micro-rdk) for code examples and more information on the micro-RDK.
