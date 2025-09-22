You need an Espressif ESP32 microcontroller to use `viam-micro-server`.
Viam recommends purchasing the ESP32 with a [development board](https://www.espressif.com/en/products/devkits).
The following ESP32 microcontrollers are supported:

- [ESP32-WROVER Series](https://www.espressif.com/en/products/modules/esp32)

You will also need a data cable to connect the microcontroller to your development machine, though subsequent firmware updates can be made remotely with the [over-the-air (OTA) service](/operate/install/setup-micro/#configure-over-the-air-updates).

Your microcontroller should have at least the following resources available to work with `viam-micro-server`:

- 2 Cores + 384kB SRAM + 2MB PSRAM + 8MB Flash

{{< alert title="Tip" color="tip" >}}
The WROVER allows only a small number of incoming gRPC connections (1-5, depending on resources), whether over HTTP2 or WebRTC.
You can change this max by [building your own firmware](/operate/install/setup-micro/#build-and-flash-custom-firmware).
{{< /alert >}}
