{{< alert title="Add support for other models" color="note" >}}
If none of the existing models fit your use case, you can create a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} to add support for it.

`viam-micro-server` works differently from the RDK, so creating modular resources for it is different.
Refer to the [Micro-RDK Module Template on GitHub](https://github.com/viamrobotics/micro-rdk/tree/main/templates/module) for information on how to create custom resources for your `viam-micro-server` machine.
You will need to [recompile and flash your ESP32 yourself](/installation/#install-viam-micro-server) instead of using Viam's prebuilt binary and installer.
{{< /alert >}}
