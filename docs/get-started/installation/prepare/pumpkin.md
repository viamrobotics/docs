---
title: "Pumpkin Board Setup Guide"
linkTitle: "Pumpkin Board Setup"
weight: 25
type: "docs"
images: ["/get-started/installation/thumbnails/pumpkin.png"]
imageAlt: "Pumpkin board"
description: "Configure the pin mappings to use a pumpkin board."
no_list: true
aliases:
  - /installation/prepare/pumpkin/
#SMEs: Matt Dannenberg
---

To use a [Mediatek Genio 500 Pumpkin single-board computer](https://ologicinc.com/portfolio/mediateki500/) with Viam:

1. [Install `viam-server`](#install-viam-server) on your machine.
1. [Create a board definitions file](#create-a-board-definitions-file), specifying the mapping between your board's GPIO pins and connected hardware.
1. [Configure a `customlinux` board](#configure-a-customlinux-board) on your machine, specifying the path to the definitions file in the board configuration.

## Install `viam-server`

{{< readfile "/static/include/install/install-linux-aarch.md" >}}

## Create a board definitions file

The board definitions file describes the location of each GPIO pin on the board so that `viam-server` can access the pins correctly.

On your Pumpkin board, create a JSON file in the <file>/home/root</file> directory named <file>board.json</file>, and provide the mappings between your GPIO pins and connected hardware.
Use the template and example below to populate the JSON file with a single key, `"pins"`, whose value is a list of objects that each represent a pin on the board.

```json
{
  "pins": [
    {
      "name": "3",
      "device_name": "gpiochip0",
      "line_number": 81,
      "pwm_id": -1
    },
    {
      "name": "5",
      "device_name": "gpiochip0",
      "line_number": 84,
      "pwm_id": -1
    },
    {
      "name": "7",
      "device_name": "gpiochip0",
      "line_number": 150,
      "pwm_id": -1
    },
    {
      "name": "11",
      "device_name": "gpiochip0",
      "line_number": 173,
      "pwm_id": -1
    },
    {
      "name": "13",
      "device_name": "gpiochip0",
      "line_number": 152,
      "pwm_id": -1
    },
    {
      "name": "15",
      "device_name": "gpiochip0",
      "line_number": 94,
      "pwm_id": -1
    },
    {
      "name": "19",
      "device_name": "gpiochip0",
      "line_number": 163,
      "pwm_id": -1
    },
    {
      "name": "21",
      "device_name": "gpiochip0",
      "line_number": 161,
      "pwm_id": -1
    },
    {
      "name": "23",
      "device_name": "gpiochip0",
      "line_number": 164,
      "pwm_id": -1
    },
    {
      "name": "27",
      "device_name": "gpiochip0",
      "line_number": 82,
      "pwm_id": -1
    },
    {
      "name": "29",
      "device_name": "gpiochip0",
      "line_number": 98,
      "pwm_id": -1
    },
    {
      "name": "31",
      "device_name": "gpiochip0",
      "line_number": 12,
      "pwm_id": -1
    },
    {
      "name": "33",
      "device_name": "gpiochip0",
      "line_number": 101,
      "pwm_id": -1
    },
    {
      "name": "35",
      "device_name": "gpiochip0",
      "line_number": 171,
      "pwm_id": -1
    },
    {
      "name": "37",
      "device_name": "gpiochip0",
      "line_number": 169,
      "pwm_id": -1
    },
    {
      "name": "8",
      "device_name": "gpiochip0",
      "line_number": 115,
      "pwm_id": -1
    },
    {
      "name": "10",
      "device_name": "gpiochip0",
      "line_number": 121,
      "pwm_id": -1
    },
    {
      "name": "12",
      "device_name": "gpiochip0",
      "line_number": 170,
      "pwm_id": -1
    },
    {
      "name": "16",
      "device_name": "gpiochip0",
      "line_number": 165,
      "pwm_id": -1
    },
    {
      "name": "18",
      "device_name": "gpiochip0",
      "line_number": 1,
      "pwm_id": -1
    },
    {
      "name": "22",
      "device_name": "gpiochip0",
      "line_number": 2,
      "pwm_id": -1
    },
    {
      "name": "24",
      "device_name": "gpiochip0",
      "line_number": 162,
      "pwm_id": -1
    },
    {
      "name": "26",
      "device_name": "gpiochip0",
      "line_number": 0,
      "pwm_id": -1
    },
    {
      "name": "28",
      "device_name": "gpiochip0",
      "line_number": 83,
      "pwm_id": -1
    },
    {
      "name": "32",
      "device_name": "gpiochip0",
      "line_number": 97,
      "pwm_id": -1
    },
    {
      "name": "36",
      "device_name": "gpiochip0",
      "line_number": 151,
      "pwm_id": -1
    },
    {
      "name": "38",
      "device_name": "gpiochip0",
      "line_number": 174,
      "pwm_id": -1
    },
    {
      "name": "40",
      "device_name": "gpiochip0",
      "line_number": 172,
      "pwm_id": -1
    }
  ]
}
```

## Configure a `customlinux` board

Configure your board as a [`customlinux`](/components/board/customlinux/) board to use your board definitions file:

{{< tabs name="Configure a customlinux board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `customlinux` model.
Enter a name for your `customlinux` board and click **Create**.

![An example configuration for a customlinux board in the Viam app Config Builder.](/components/board/customlinux-ui-config.png)

Copy and paste the following json object into your board's **Attributes** box.

```json {class="line-numbers linkable-line-numbers"}
{
  "board_defs_file_path": "/home/root/board.json"
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "myCustomBoard",
      "model": "customlinux",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "board_defs_file_path": "/home/root/board.json"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Next steps

{{< cards >}}
{{% card link="/build/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/build/program/" %}}
{{< /cards >}}

## Need assistance?

{{< snippet "social.md" >}}
