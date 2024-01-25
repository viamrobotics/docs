---
title: "Configure a Custom Linux Board"
linkTitle: "customlinux"
weight: 75
type: "docs"
description: "Configure a custom Linux board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
aliases:
  - "/components/board/customlinux/"
# SMEs: Alan, Olivia, Susmita
---

The `customlinux` board model supports boards like the [Mediatek Genio 500 Pumpkin](https://ologicinc.com/portfolio/mediateki500/) that run Linux operating systems and are not supported by other built-in Viam models.

To integrate a custom Linux board into your machine:

1. [Install `viam-server`](#install-viam-server) on your machine.
1. [Create a board definitions file](#create-a-board-definitions-file), specifying the mapping between your board's GPIO pins and connected hardware.
1. [Configure a `customlinux` board](#configure-your-board) on your machine, specifying the path to the definitions file in the board configuration.

## Install `viam-server`

{{< readfile "/static/include/install/install-linux-aarch.md" >}}

## Create a board definitions file

{{% alert title="Caution" color="caution" %}}

While some lines on a board are attached to GPIO pins, some lines are attached to other board hardware.
It is important to carefully determine your `line_number` values.
Randomly entering numbers may result in hardware damage.

{{% /alert %}}

The board definitions file describes the location of each GPIO pin on the board so that `viam-server` can access the pins correctly.

On your `customlinux` board, create a JSON file in the directory of your choice with and provide the mappings between your GPIO pins and connected hardware.
Use the template and example below to populate the JSON file with a single key, `"pins"`, whose value is a list of objects that each represent a pin on the board.

{{< tabs >}}
{{% tab name="Template" %}}

```json
{
  "pins": [
    {
      "name": "<pin-name>",
      "device_name": "<gpio-device-name>",
      "line_number": <integer>,
      "pwm_chip_sysfs_dir": "<pwm-device-name>"
      "pwm_id": <integer>
    },
    ...
  ]
}
```

{{% /tab %}}
{{% tab name="Pumpkin Board Example" %}}

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

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for each pin object:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `name` | string | **Required** | The name of the pin. This can be anything you want but it is convenient to use the physical board pin number. <br> Example: `"3"`. |
| `device_name` | string | **Required** | The name of the device in <file>/dev</file> that this pin is attached to. Multiple pins may be attached to the same GPIO chip.  See [GPIO info tips](#tips-for-finding-gpio-information) below. <br> Example: `"gpiochip0"`.
| `line_number` | integer | **Required** | The line on the chip that is attached to this pin. See [GPIO info tips](#tips-for-finding-gpio-information) below. <br> Example: `81`. |
| `pwm_chip_sysfs_dir` | string | Optional | Uniquely specifies which PWM device within [sysfs](https://en.wikipedia.org/wiki/Sysfs) this pin is connected to. See [PWM info tips](#tips-for-finding-pwm-information) below. <br> Example: `3290000.pwm`. |
| `pwm_id` | integer | Optional | The line number on the PWM chip. See [PWM info tips](#tips-for-finding-pwm-information) below. <br> Example: `0`. |

{{% alert title="Tip" color="tip" %}}

`pwm_chip_sysfs_dir` and `pwm_id` only apply to pins with hardware PWM supported and enabled.
If your board supports hardware PWM, you will need to enable it if it is not enabled by default.
This process depends on your specific board.

{{% /alert %}}

{{% alert title="Info" color="info" %}}

The current version of `viam-server` creates PWM functionality with software.
The implementation of hardware-based PWM for custom Linux boards is planned for release in the future, so we recommend that you add PWM information to your board now so that you do not need to update your config later.

{{% /alert %}}

### Tips for finding GPIO information

To see which chips exist and how many lines each chip has, run this command on your board:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo gpiodetect
```

Here is example output from this command on an Odroid C4:

```sh {id="terminal-prompt" class="command-line" data-output="1-10"}
gpiochip0 [aobus-banks] (16 lines)
gpiochip1 [periphs-banks] (86 lines)
```

This example output indicates that there are two GPIO chips on this board.
One has 16 lines, numbered 0-15.
The other has 86 lines, numbered 0-85.

To see info about every line on every GPIO chip, run this command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo gpioinfo
```

Here is example output from the `sudo gpioinfo` command on an Odroid C4:

```sh {id="terminal-prompt" class="command-line" data-output="1-10"}
...
  line  62:      unnamed       unused   input  active-high
  line  63:      unnamed       unused   input  active-high
  line  64:     "PIN_27"       unused   input  active-high
  line  65:     "PIN_28"       unused   input  active-high
  line  66:     "PIN_16"       unused   input  active-high
  line  67:     "PIN_18"       unused   input  active-high
  line  68:     "PIN_22"       unused   input  active-high
...
```

In this example, the human-readable names such as `"PIN_28"` indicate which physical board pin each line is attached to.
However, these names are not standardized.
Some boards have pin names like `"PH.03"`.
In either case, you need to look at the data sheet for your board and determine how the pin names map to the hardware.

### Tips for finding PWM information

Run the following command and look for unique strings within each [symlink](https://en.wikipedia.org/wiki/Symbolic_link).

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
ls -l /sys/class/pwm
```

Here is example output from this command on a Jetson Orin AGX:

```sh {id="terminal-prompt" class="command-line" data-output="1-10"}
total 0
lrwxrwxrwx 1 root root 0 Sep  8  2022 pwmchip0 -> ../../devices/3280000.pwm/pwm/pwmchip0
lrwxrwxrwx 1 root root 0 Sep  8  2022 pwmchip1 -> ../../devices/32a0000.pwm/pwm/pwmchip1
lrwxrwxrwx 1 root root 0 Sep  8  2022 pwmchip2 -> ../../devices/32c0000.pwm/pwm/pwmchip2
lrwxrwxrwx 1 root root 0 Sep  8  2022 pwmchip3 -> ../../devices/32f0000.pwm/pwm/pwmchip3
lrwxrwxrwx 1 root root 0 Sep  8  2022 pwmchip4 -> ../../devices/39c0000.tachometer/pwm/pwmchip4
```

Based on this example output, the values to use for `pwm_chip_sysfs_dir` are `328000.pwm`, `32a0000.pwm`, and so on.

Each of these directories contains a file named <file>npwm</file> containing a number.
The number in each file is the number of lines on the chip.
The `pwm_id` value will be between `0` and one less than the number of lines.
For example, if the <file>npwm</file> contains `"4"`, then the valid `pwm_id` values are `0`, `1`, `2`, and `3`.

Determining which specific chip and line are attached to each pin depends on the board.
Try looking at your board's data sheet and cross-referencing with the output from the commands above.

## Configure your board

{{< tabs name="Configure a customlinux board" >}}

{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `board` type, then select the `customlinux` model.
Enter a name for your `customlinux` board and click **Create**.

![An example configuration for a customlinux board in the Viam app Config Builder.](/components/board/customlinux-ui-config.png)

Copy and paste the following attribute template into your board's **Attributes** box.
Then edit the file path to use your [board definitions file](#create-a-board-definitions-file).

{{< tabs name="Configure attributes" >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board_defs_file_path": "<file_path>"
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "board_defs_file_path": "/home/root/board.json"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-customlinux-board>",
      "model": "customlinux",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "board_defs_file_path": "<file_path>"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

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

The following attributes are available for `customlinux` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board_defs_file_path` | string | **Required** | The path to the pin mappings. See [Create a board definitions file](#create-a-board-definitions-file). |
