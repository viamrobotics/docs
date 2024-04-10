### Hardware requirements

You need an Espressif ESP32 microcontroller to use the micro-RDK.
Viam recommends purchasing the ESP32 with a [development board](https://www.espressif.com/en/products/devkits).
The following ESP32 microcontrollers are supported:

- [ESP32-WROOM Series](https://www.espressif.com/en/products/modules/esp32)
- [ESP32-WROVER Series](https://www.espressif.com/en/products/modules/esp32)

Your microcontroller should have the following resources available to work with the micro-RDK:

- 2 Cores + 384kB SRAM + 4MB Flash

{{< alert title="Tip" color="tip" >}}
The main difference between the WROOM and WROVER is that the WROVER has additional RAM with the SPIRAM chip.
If you would like to allow more than one concurrent connection to your device we recommend using the WROVER.
{{< /alert >}}
