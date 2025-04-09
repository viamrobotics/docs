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
prev: "/operate/get-started/basics/"
aliases:
  - /installation/microcontrollers/
  - /installation/prepare/microcontrollers/
  - /installation/prepare/microcontrollers/
  - /build/micro-rdk/
  - /get-started/installation/microcontrollers/
  - /installation/viam-micro-server-setup/
  - /operate/reference/viam-micro-server/viam-micro-server-troubleshooting/
---

Viam maintains a [lightweight version of `viam-server`](/operate/reference/viam-micro-server/) for microcontrollers.

## Supported microcontrollers

ESP32 microcontrollers must have at least 2 cores, 384kB SRAM, 2MB PSRAM and 8MB flash to work with Viam.
The following microcontrollers have been tested with Viam:

- [ESP32-WROVER Series](https://www.espressif.com/en/products/modules/esp32)

## About ESP32 microcontroller setup

Because microcontrollers do not run operating systems and are instead flashed with firmware, the setup process is different than for regular computers and SBCs.

To use an ESP32 controller with custom hardware, you build a firmware version from the Micro-RDK and modules to support your hardware.

To quickly try out Viam for microcontrollers, you can use the pre-built binary `viam-micro-server` which supports the following components:

- [`gpio`](/operate/reference/components/servo/gpio-micro-rdk/): A servo controlled by GPIO pins.
- [`two_wheeled_base`](/operate/reference/components/base/two_wheeled_base/): A robotic base with differential steering.
- [`free_heap_sensor`](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src): Reports the amount of free heap memory on the microcontroller.
- [`wifi_rssi_sensor`](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src): Reports the signal strength of the ESP32's WiFi connection.

## Quickstart

To get started quickly with the pre-built `viam-micro-server` binary, follow these steps:

1. Create a [Viam app](https://app.viam.com) account.
   The Viam app is the online hub for configuring and managing devices as well as viewing data.

1. Add a new _{{< glossary_tooltip term_id="machine" text="machine" >}}_ using the button in the top right corner of the **LOCATIONS** tab in the app.
   A machine represents your device.

1. From your machine's page in the Viam app, follow the setup instructions to install `viam-micro-server` on your device and connect it to the cloud.

   A secure connection is automatically established between your machine and the Viam app.
   When you update your machine's configuration, `viam-micro-server` automatically gets the updates.

   You are ready to [configure](/operate/get-started/supported-hardware/) any of the components listed above on your machine.

## Advanced setup

If you are using your ESP32 with resources that are not supported by the pre-built binary, you can build your own firmware with the Micro-RDK and your choice of {{< glossary_tooltip term_id="module" text="modules" >}}.

See [Create or use a Micro-RDK module](/operate/get-started/other-hardware/micro-module/) to build custom firmware for your ESP32.
