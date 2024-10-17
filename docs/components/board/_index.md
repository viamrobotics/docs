---
title: "Board Component"
linkTitle: "Board"
childTitleEndOverwrite: "Board Component"
weight: 20
type: "docs"
no_list: true
description: "The signal wire hub of a machine, with GPIO pins for transmitting signals between the machine's computer and its other components."
tags: ["board", "components"]
icon: true
images: ["/icons/components/board.svg"]
modulescript: true
aliases:
  - "/components/board/"
  - "/micro-rdk/board/"
  - "/build/micro-rdk/board/"
hide_children: true
# SMEs: Gautham, Rand
---

The board component provides an API for setting GPIO pins to high or low, setting PWM, and working with analog and digital interrupts.

If you have GPIO pins you wish to control, use a board component.

Your GPIO pins can be present as:

- The GPIO pins on a single-board computer (SBC).
- A GPIO peripheral device that must connect to an external computer.
- A PWM peripheral device that must connect to an SBC that has a CPU and GPIO pins.

In other words, the board of a machine is its signal wire hub.
Signaling controls the flow of electricity to these pins to change their state between "high" (active) and "low" (inactive), and to send [digital signals](https://en.wikipedia.org/wiki/Digital_signal) to and from other hardware.

{{< alert title="Running viam-server" color="note" >}}

The board component allows you to use the pins on your board.
If there is no board model for your board:

- you can still run `viam-server` if your board [supports it](/installation/viam-server-setup/#platform-requirements)
- you can still access USB ports

{{< /alert >}}

## Configuration

To use GPIO pins, you need to add a board component to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your board.

The following list shows the available board models.
If your board is not among them, you may be able to use the pins on your board with an experimental [periph.io](https://periph.io/)-based [modular component](https://github.com/viam-labs/periph_board).
This works for boards such as the [RockPi S](https://wiki.radxa.com/RockpiS).

For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:board" type="board" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`esp32`](esp32/) | An ESP32 microcontroller |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The [board API](/appendix/apis/components/board/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/board-table.md" >}}

## Troubleshooting

If your board is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review your board model's documentation to ensure you have configured all required attributes.
1. Check that all wires are securely connected.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the board there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{% card link="/tutorials/get-started/blink-an-led" noimage="true" %}}
{{< /cards >}}
