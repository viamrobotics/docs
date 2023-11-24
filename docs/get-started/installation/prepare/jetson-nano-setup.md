---
title: "NVIDIA Jetson Nano and Orin Nano Setup Guide"
linkTitle: "Jetson Nano and Orin Nano Setup"
weight: 20
type: "docs"
image: "/get-started/installation/thumbnails/jetson-nano-dev-kit.png"
imageAlt: "Jetson Nano"
images:
  ["/get-started/installation/thumbnails/jetson-nano-dev-kit.png"]
description: "Prepare your Jetson Nano or Jetson Orin Nano for viam-server installation."
no_list: true
aliases:
  - /installation/prepare/jetson-nano-setup/
# SMEs: Pete Garafano
---

The [Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano) and [Jetson Orin Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin) from [NVIDIA](https://www.nvidia.com/) are small computers built for embedded applications and capable of supporting modern AI workloads.
Follow this guide to set up the [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit) or the [Jetson Orin Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-agx-orin-developer-kit) to prepare your NVIDIA Jetson Nano for `viam-server` installation.

<div class="td-max-width-on-larger-screens text-center">
{{<imgproc src="get-started/installation/thumbnails/jetson-nano-dev-kit.png" resize="200x" alt="The front of the NVIDIA Jetson Nano single-board computer development kit.">}}
{{<imgproc src="get-started/installation/thumbnails/jetson-orin-nano.jpeg" resize="200x" alt="The front of the NVIDIA Jetson Orin Nano single-board computer development kit.">}}
</div>

{{% alert title="Important" color="note" %}}

This guide assumes that you have a Jetson Nano Developer Kit or a Jetson Orin Nano Developer Kit with a Jetson module and reference carrier board.
If you want to use a different carrier board to incorporate your Nano into your robot, the type of carrier board you use will affect your hardware requirements.

{{% /alert %}}

{{% alert title="CAUTION: Use 3.3V inputs and outputs" color="caution" %}}

The GPIO pins on Jetson boards are rated 3.3V signals. 5V signals from encoders and sensors can cause damage to a pin. We recommend selecting hardware that can operate 3.3V signals or lower. For details, see pages 1-3 of the [Jetson Nano Developer Kit 40-Pin Expansion Header GPIO Usage Considerations Applications Note](https://developer.nvidia.com/jetson-nano-developer-kit-40-pin-expansion-header-gpio-usage-considerations-applications-note).

{{% /alert %}}

## Hardware Requirements

You need the following hardware, tools, and software to install `viam-server` on a Jetson Nano or Jetson Orin Nano:

**Initial Setup with Display Attached:**

1. A [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit) or [Jetson Orin Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-agx-orin-developer-kit)
2. A microSD card (32GB UHS-1 minimum recommended)
3. A computer display (HDMI or DP) with a USB keyboard and mouse
4. A way to connect the microSD card to the computer (like a microSD slot or microSD reader)
5. Ethernet cable and/or Wifi dongle, to establish network connection on the Nano
6. 5V-2A (Nano) or 9-19V (Orin Nano) DC power supply with barrel jack connector

**Initial Setup in Headless Mode:**

1. A [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit) or [Jetson Orin Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-agx-orin-developer-kit)
2. A microSD card (32GB UHS-1 minimum recommended)
3. An internet-connected computer
4. A way to connect the computer to the Nano (like a USB 2.0 A-Male to Micro B Cable)
5. A way to connect the microSD card to the computer (like a microSD slot or microSD reader)
6. Ethernet cable and/or Wifi dongle, to establish network connection on the Nano
7. 5V-2A (Nano) or 9-19V (Orin Nano) DC power supply with barrel jack connector

## Nano Setup Guide

Follow the instructions in [Getting Started with Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit) or [Getting Started with Jetson Orin Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit).
Once you have reached _Next Steps_, return to the Viam docs.

## Install `viam-server`

{{< alert title="Tip: <code>viam-server</code> installation with <code>curl</code>" color="tip" >}}

If `curl` is not installed on your Orin, run `sudo apt install curl` before downloading the `viam-server` binary.

If this command fails, try using `wget https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-aarch64.AppImage` to download the `viam-server` binary.

{{% /alert %}}

{{< readfile "/static/include/install/install-linux-aarch.md" >}}

## Serial Communication Protocol Tips

To change the pins that are in use for modes of serial communication, launch <file>jetson-io.py</file> with the following commands:

```sh { class="command-line" data-prompt="$"}
cd ~
sudo /opt/nvidia/jetson-io/jetson-io.py
```

In the interactive menu that opens, select **Configure Jetson 40 Pin Header** and **Configure header pins manually** to select and deselect pins to enable use.
For a Jetson Orin Nano, reference the following:

<!-- prettier-ignore -->
| GPIO Header Pin | Viam Bus ID | `jetson-io.py` ID |
| ---------------| ----------- | ----------------- |
| 3, 5 | `7` | `i2c2` |
| 27, 28 | `1` | `i2c8` |
| 19, 21, 23, 24, 26 | `0` | `spi1` |
| 13, 16, 18, 22, 37 | `2` | `spi3` |
| 15 | | `pwm1` |
| 33 | | `pwm5` |

Note that I2C buses do not need to be configured through <file>jetson-io.py</file>.
See NVIDIA's documentation on [Configuring the Jetson Expansion Headers](https://docs.nvidia.com/jetson/archives/r35.1/DeveloperGuide/text/HR/ConfiguringTheJetsonExpansionHeaders.html) for more information.

## Next Steps

{{< cards >}}
{{% card link="/build/configure/configuration/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/build/program/" %}}
{{< /cards >}}

## Troubleshooting

Make sure the polarity on your barrel jack power supply is matched when powering your robot.
See the last step of your appropriate [initial setup guide](#hardware-requirements) for instructions on choosing the correct power supply for your Nano board.

If you do not see an interactive menu after launching <file>jetson-io.py</file>, try resizing your window to a large size.

You can find additional assistance in the [Troubleshooting section](/reference/appendix/troubleshooting/).

{{< snippet "social.md" >}}
