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

A _board_ component represents your machine's general purpose input/output [(GPIO)](https://www.howtogeek.com/787928/what-is-gpio/) pins: a collection of pins on the motherboard of a computer that can receive electrical signals.

In other words, the board of a machine is its signal wire hub.
The board communicates with the other [components](/components/) of the machine.

Many single-board computers (SBCs) have GPIO pins built into them.
If you are running `viam-server` on an SBC but are not using any of its GPIO pins, you do not need to configure a board component.
However, if you want to access the GPIO pins, you need to configure a board component.

A board can be:

- The GPIO pins on a single-board computer (SBC).
- A GPIO peripheral device that must connect to an external computer.
- A PWM peripheral device that must connect to an SBC that has a CPU and GPIO pins.

Signaling is overseen by a computer running `viam-server` which allows you to control the flow of electricity to these pins to change their state between "high" (active) and "low" (inactive), and to send [digital signals](https://en.wikipedia.org/wiki/Digital_signal) to and from other hardware.

{{% figure src="/components/board/board-comp-options.png" alt="Image showing two board options: First, running viam-server locally and second, running via a peripheral plugged into the USB port of a computer that is running the viam-server." title="Two different board options: a single-board computer with GPIO pins running `viam-server` locally, or a GPIO peripheral plugged into a desktop computer's USB port, with the computer running `viam-server`." %}}

## Available models

{{< alert title="Running viam-server" color="note" >}}

The board component allows you to use the pins on your board.
If there is no board model for your board:

- you can still run `viam-server` if your board [supports it](/installation/#platform-requirements)
- you can still access USB ports

For some SBCs, for example the [RockPi S](https://wiki.radxa.com/RockpiS), you can use the pins on your board with an experimental [periph.io](https://periph.io/) based [modular component](https://github.com/viam-labs/periph_board).

{{< /alert >}}

To use your board component, check whether one of the following models supports it.

For configuration information, click on the model name:

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

## Control your board with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by getting your `board` component from the machine with `FromRobot` and adding API method calls, as shown in the following examples.

These examples assume you have a board called "my_board" configured as a component of your machine.
If your board has a different name, change the `name` in the code.

Be sure to import the board package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.board import Board
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/board"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The board component supports the following methods:

{{< readfile "/static/include/components/apis/generated/board-table.md" >}}

{{< readfile "/static/include/components/apis/generated/board.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/get-started/blink-an-led" %}}
{{% card link="/tutorials/projects/guardian" %}}
{{< /cards >}}
