---
title: "Board API"
linkTitle: "Board"
weight: 20
type: "docs"
description: "Give commands for setting GPIO pins to high or low, setting PWM, and working with analog and digital interrupts."
icon: true
images: ["/icons/components/board.svg"]
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

The board API allows you to give commands to your [board components](/components/board/) for setting GPIO pins to high or low, setting PWM, and working with analog and digital interrupts.

The board component supports the following methods:

{{< readfile "/static/include/components/apis/generated/board-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by getting your `board` component from the machine with `FromRobot` and adding API method calls, as shown in the following examples.

The following examples assume you have a board called "my_board" configured as a component of your machine.
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

{{< readfile "/static/include/components/apis/generated/board.md" >}}
