---
title: "NVIDIA Jetson Nano Setup Guide"
linkTitle: "Jetson Nano Setup"
weight: 20
type: "docs"
image: "/installation/thumbnails/jetson-nano-dev-kit.png"
imageAlt: "Jetson Nano"
images: ["/installation/thumbnails/jetson-nano-dev-kit.png"]
description: "Set up the Jetson Nano Developer Kit to prepare your NVIDIA Jetson Nano or Orin Nano for viam-server installation."
no_list: true
# SMEs: Pete Garafano
---

The [Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano) from [NVIDIA](https://www.nvidia.com/) is a small computer that is built for embedded applications and is capable of supporting modern AI workloads.
Follow this guide to set up the [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit) to prepare your NVIDIA Jetson Nano for `viam-server` installation. This installation also works with the newer model [Jetson Orin Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin).

<div class="td-max-width-on-larger-screens text-center">
{{<imgproc src="installation/thumbnails/jetson-nano-dev-kit.png" resize="400x" alt="The front of the NVIDIA Jetson Nano single-board computer development kit.">}}
</div>

{{% alert title="Stability Notice" color="note" %}}

Support for this board is experimental.
Stability is not guaranteed.

{{% /alert %}}

{{% alert title="Important" color="note" %}}

This guide assumes that you have a Jetson Nano Developer Kit with a Jetson module and reference carrier board.
If you want to use a different carrier board to incorporate your Nano into your robot, the type of carrier board you use will affect your hardware requirements.

{{% /alert %}}

## Hardware Requirements

You need the following hardware, tools, and software to install `viam-server` on a Jetson Nano:

**Initial Setup with Display Attached:**

1. A [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)
2. A microSD card (32GB UHS-1 minimum recommended)
3. A computer display (HDMI or DP) with a USB keyboard and mouse
4. A way to connect the microSD card to the computer (like a microSD slot or microSD reader)
5. Ethernet cable and/or Wifi dongle, to establish network connection on the Nano
6. 5V-2A DC with barrel jack connector and/or Micro-USB power supply, to power the Nano

**Initial Setup in Headless Mode:**

1. A [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)
2. A microSD card (32GB UHS-1 minimum recommended)
3. An internet-connected computer
4. A way to connect the computer to the Nano (like a USB 2.0 A-Male to Micro B Cable)
5. A way to connect the microSD card to the computer (like a microSD slot or microSD reader)
6. Ethernet cable and/or Wifi dongle, to establish network connection on the Nano
7. 5V-2A DC with barrel jack connector power supply, to power the Nano (Micro-USB port will be taken by the cable connection to computer)

## Jetson Nano Setup Guide

1. Follow the instructions in [Getting Started with Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit).
   Once you have reached *Next Steps*, return to the Viam docs.
2. Your Jetson Nano now has a Viam-compatible operating system installed.
   Continue to [install viam-server](/installation/#install-viam-server).
   Note that the Jetson Nano has aarch64 CPU architecture.

{{< alert title="Tip: <code>viam-server</code> installation with <code>curl</code>" color="tip" >}}

If `curl` is not installed on your Orin, run `sudo apt install curl` before downloading the `viam-server` binary.

If this command fails, try using `wget https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-aarch64.AppImage` to download the `viam-server` binary.

{{% /alert %}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
