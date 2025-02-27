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

## Supported microcontrollers

ESP32 microcontrollers must have at least 2 cores, 384kB SRAM, 2MB PSRAM and 8MB flash to work with Viam.
The following microcontrollers have been tested with Viam:

- [ESP32-WROVER Series](https://www.espressif.com/en/products/modules/esp32)

## About ESP32 microcontroller setup

Because microcontrollers do not run operating systems and are instead flashed with firmware, the setup process is different than for other devices running Viam.

You can choose to use the pre-built binary for `viam-micro-server` which supports the following components:

- [`gpio`](/operate/reference/components/servo/gpio-micro-rdk/): A servo controlled by GPIO pins.
- [`two_wheeled_base`](/operate/reference/components/base/two_wheeled_base/): A robotic base with differential steering.
- [`free_heap_sensor`](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src): Reports the amount of free heap memory on the microcontroller.
- [`wifi_rssi_sensor`](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src): Reports the signal strength of the ESP32's WiFi connection.

Or, you can build your own firmware with the Micro-RDK (the software development kit for microcontrollers from which `viam-micro-server` is built) and your choice of modules.

## Quickstart

To get started quickly with the pre-built `viam-micro-server` binary, follow these steps:

1. Create a [Viam app](https://app.viam.com) account.
   The Viam app is the online hub for configuring and managing devices as well as viewing data.

1. Add a new _{{< glossary_tooltip term_id="machine" text="machine" >}}_ using the button in the top right corner of the **LOCATIONS** tab in the app.
   A machine represents your device.

1. From your machine's page in the Viam app, follow the setup instructions to install `viam-micro-server` on your device and connect it to the cloud.

   A secure connection is automatically established between your machine and the Viam app.
   When you update your machine's configuration, `viam-micro-server` automatically gets the updates.

1. Use the **+** button on your machine's **CONFIGURE** tab to add any of the supported components listed above.

1. [Data capture and sync](/data-ai/capture-data/capture-sync/) is supported for microcontrollers.
   You can click the **Add method** button on any component's config card to configure data capture for that component.

As soon as you configure each component and save the configuration, you can use the **TEST** panel of the component's config card to, for example, view your camera's stream or turn your motor.

## Advanced setup

If you are using your ESP32 with resources that are not supported by the pre-built binary, you can build your own firmware with the Micro-RDK and your choice of {{< glossary_tooltip term_id="module" text="modules" >}}.

See [Create or use a Micro-RDK module](/operate/get-started/other-hardware/micro-module/) to install required software and build custom firmware.
