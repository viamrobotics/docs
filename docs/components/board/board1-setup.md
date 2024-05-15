---
title: "<board-series-model> Setup Guide"
linkTitle: "<board-series-model> Setup"
weight: 16
type: "docs"
description: "Flash an <storage-medium> for the <board-series-model> to prepare it for viam-server installation."
images: ["/get-started/installation/thumbnails/<board-series-model>.png"]
imageAlt: "<board-series-model>"
no_list: true
draft: true
---

The [<board-series-model>](http://www.<board-series-model>) from <manufacturer/organization> is a <brief board description of features and specifications>.
It supports <operating-systems-or-distributions> and is ideal for <use-cases-or-applications>.
Follow this guide to set up your <board-series-model> and prepare it for `viam-server` installation.

{{<imgproc src="get-started/installation/thumbnails/orange-pi-zero2.png" alt="The <board-series-model> single-board computer." resize="350x" declaredimensions=true >}}

## Hardware requirements

- Development machine: laptop or computer workstation
- An [<board-series-model>](http://www.<board-series-model>) board
- ...

## Install OS

The <board-series-model> boots from a <storage-medium>.
You need to install an operating system on the <storage-medium> that you will use with your <board-series-model>:

<Viam-specific-OS-installation-instructions OR link-to-companys-board-OS-installation guide>

## Power your <board-series-model>

To power your <board-series-model>, connect your power adapter to the boards <port-type> port.
The LED should light up, which indicates that the board is powered.

{{% alert title="Tip" color="tip" %}}
If your board's LED does not light up when powered, try re-flashing your <storage-medium> or using a different <storage-medium>.
{{% /alert %}}

To connect to a display, connect the <HDMI/micro-HDMI> end of your HDMI cable to the <board> and the other end to your monitor.
Then, to connect the keyboard and mouse, plug the two devices into your computer's USB hub and connect the USB hub to your <board-series-model>'s <USB-type> port.

## Establish a network connection

You can plug the ethernet cable into your <board-series-model> for a wired internet connection.
For a wireless connection, you can <alternative-wireless-network-connection-methods>.

### Update your <board-series-model>

Once you're connected to your board, you can verify all packages are up to date by running the following command:

`sudo apt update && sudo apt dist-upgrade && sudo reboot`

## Install `viam-server`

{{< readfile "/static/include/install/install-linux.md" >}}

## Troubleshooting

If you experience any issues getting Viam working on your <board-series-model, consult the [BeagleBone documentation](https://docs.<board-series-model-documentation>).

{{< snippet "social.md" >}}

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

## Next steps

{{< cards >}}
{{% card link="/build/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/get-started/try-viam/" %}}
{{< /cards >}}
