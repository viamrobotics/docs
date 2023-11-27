---
title: "Pumpkin Board Setup Guide"
linkTitle: "Pumpkin Board Setup"
weight: 25
type: "docs"
image: "/get-started/installation/thumbnails/pumpkin.png"
imageAlt: "Pumpkin board"
images: ["/get-started/installation/thumbnails/pumpkin.png"]
description: "Configure the pin mappings to use a pumpkin board."
no_list: true
aliases:
  - /installation/prepare/pumpkin/
#SMEs: Matt Dannenberg
---

To use a [Mediatek Genio 500 Pumpkin single-board computer](https://ologicinc.com/portfolio/mediateki500/) with Viam:

1. [Install `viam-server`](#install-viam-server)
2. [Create a pin mappings file](#create-pin-mappings-file)
3. [Configure a customlinux board](#configure-a-customlinux-board)

## Install `viam-server`

{{< readfile "/static/include/install/install-linux-aarch.md" >}}

## Create a board definitions file

{{% alert title="Caution" color="caution" %}}

While some lines on a board are attached to GPIO pins, some lines are attached to other board hardware.
It is important to carefully determine your `line_number` values.
Randomly entering numbers may result in hardware damage.

{{% /alert %}}

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

### Upload your board definitions file

Once you have created your board definitions file, you can choose to upload it to the Viam app using the [Viam CLI](/fleet/cli/).

Uploading your definitions file allows you to store it centrally on the Viam app, and to deploy it your machines without needing to create it again for each one.

For example:

- The following command uploads a board definitions file named `my-board-def-file.json` that contains pin mappings for a configured [board](/components/board/) named `my-board`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam board upload --name='my-board' --organization='abcdef12-abcd-abcd-abcd-abcdef123456' --version=1.0.0 my-board-def-file.json
   ```

- The following command downloads a previously-uploaded board definitions file stored as `my-board` from the Viam app:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam board download --name='my-board' --organization='abcdef12-abcd-abcd-abcd-abcdef123456' --version=1.0.0
   ```

For more information, see the [`viam board` CLI command](/fleet/cli/#board).

## Configure a `customlinux` board

Configure your board as a [`customlinux`](/build/configure/components/board/customlinux/) board to use your pin mappings file:

{{< tabs name="Configure a customlinux board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `customlinux` model.
Enter a name for your `customlinux` board and click **Create**.

![An example configuration for a customlinux board in the Viam app Config Builder.](/build/configure/components/board/customlinux-ui-config.png)

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

## Next Steps

{{< cards >}}
{{% card link="/build/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/build/program/" %}}
{{< /cards >}}

## Need assistance?

{{< snippet "social.md" >}}
