You need an Espressif ESP32 microcontroller to use `viam-micro-server`.
Viam recommends purchasing the ESP32 with a [development board](https://www.espressif.com/en/products/devkits).
The following ESP32 microcontrollers are supported:

- [ESP32-WROVER Series](https://www.espressif.com/en/products/modules/esp32)
- [ESP32-WROOM Series](https://www.espressif.com/en/products/modules/esp32) (until v0.1.7)

You will also need a data cable to connect the microcontroller to your development machine.

Your microcontroller should have at least the following resources available to work with `viam-micro-server`:

- 2 Cores + 384kB SRAM + 2MB PSRAM + 4MB Flash

{{< alert title="Tip" color="tip" >}}
The main difference between the WROOM and WROVER is that the WROVER has additional RAM with the SPIRAM chip.
If you would like to allow more than one concurrent connection to your device we recommend using the WROVER.
The WROVER allows a max of 3 incoming gRPC connections (whether over HTTP2 or WebRTC).
You can change this max by [building your own version of `viam-micro-server`](/installation/viam-micro-server-dev/).
{{< /alert >}}
