---
title: Flash
id: flash
full_link:
short_description: The process of writing an operating system or firmware to a device's storage medium.
aka:
  - flashed
  - flashing
type: "page"
---

**Flashed** (or **flashing**) refers to the process of writing an operating system, firmware, or other software directly to a device's non-volatile storage medium, such as an SD card, eMMC storage, or flash memory.

In the context of robotics and the Viam platform, flashing is commonly performed when:

- Setting up a new {{< glossary_tooltip term_id="pi" text="Raspberry Pi" >}} with an operating system
- Installing the Viam Micro-RDK on supported microcontrollers

The flashing process typically involves:

1. Downloading an image file (OS or firmware)
2. Using specialized software to write the image to the target device
3. Verifying the write was successful
4. Booting or resetting the device to load the new software

For example, when setting up a Raspberry Pi for use with Viam, you would "flash" Raspberry Pi OS to an SD card using the [Raspberry Pi Imager](/operate/reference/prepare/rpi-setup/#install-raspberry-pi-os) or similar software.

Flashing is different from regular software installation because it involves writing directly to storage at a low level, often replacing everything on the target storage medium.
