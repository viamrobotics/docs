---
linkTitle: "Set up an ESP32"
title: "Set up an ESP32"
weight: 25
layout: "docs"
type: "docs"
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
no_list: false
description: "Install the lightweight version of the software that drives hardware and connects your device to the cloud."
aliases:
  - /installation/microcontrollers/
  - /installation/prepare/microcontrollers/
  - /installation/prepare/microcontrollers/
  - /build/micro-rdk/
  - /get-started/installation/microcontrollers/
  - /installation/viam-micro-server-setup/
---

Get started by installing the open-source software that drives your hardware and connects your device to the cloud.
The easiest way to do this is through the Viam app, so that your machines are automatically connected to configuration and remote operation tools.

## Supported microcontrollers

ESP32 microcontrollers must have at least 2 cores, 384kB SRAM, 2MB PSRAM and 8MB flash to work with Viam.

- [ESP32-WROVER Series](https://www.espressif.com/en/products/modules/esp32)

## Quickstart

To get started quickly with the pre-built binary for your microcontroller, follow these steps:

1. Create a [Viam app](https://app.viam.com) account.
   The Viam app is the online hub for configuring and managing devices as well as viewing data.

1. Add a new _{{< glossary_tooltip term_id="machine" text="machine" >}}_ using the button in the top right corner of the **LOCATIONS** tab in the app.
   A machine represents your device.

1. From your machine's page in the Viam app, follow the setup instructions to install `viam-micro-server` on your device and connect it to the cloud.
   [`viam-micro-server`](/operate/reference/viam-micro-server/) is the lightweight version of [`viam-server`](/operate/reference/viam-server/) for microcontrollers.

1. Use the **+** button on your machine's **CONFIGURE** tab to add [supported hardware components](/operate/get-started/supported-hardware/) so that `viam-micro-server` can control your specific hardware.
   The following hardware components are supported by the pre-built `viam-micro-server` binary:

   - [`gpio`](/operate/reference/components/servo/gpio-micro-rdk/): A servo controlled by GPIO pins.
   - [`two_wheeled_base`](/operate/reference/components/base/two_wheeled_base/): A robotic base with differential steering.
   - [`free_heap_sensor`](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src): Reports the amount of free heap memory on the microcontroller.
   - [`wifi_rssi_sensor`](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src): Reports the signal strength of the ESP32's WiFi connection.<br><br>

1. [Data capture and sync](/data-ai/capture-data/capture-sync/) is supported for microcontrollers.
   You can click the **Add method** button on any component's config card to configure data capture for that component.

As soon as you configure each component and save the configuration, you can use the **TEST** panel of the component's config card to, for example, view your camera's stream or turn your motor.

## Advanced setup

The steps above install the pre-built binary for your microcontroller, which includes support for a default set of {{< glossary_tooltip term_id="module" text="modules" >}}.

If you are using your ESP32 with resources that are not supported by the pre-built binary, you can build your own firmware with the Micro-RDK and your choice of modules.

See [Create or use a Micro-RDK module](/operate/get-started/other-hardware/micro-module/) to install required software and build custom firmware.
