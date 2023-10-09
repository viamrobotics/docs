---
title: "Configure a customlinux board"
linkTitle: "customlinux"
weight: 75
type: "docs"
description: "Configure a customlinux board."
images: ["/icons/components/board.svg"]
tags: ["board", "components"]
# SMEs: Susmita
---

Configure a `customlinux` board to integrate linux boards like the [Pumpkin i500](https://ologicinc.com/portfolio/mediateki500/) into your robot.

Complete the following setup requirements, then move on to configuring your board in the [Viam app](https://app.viam.com):

## Setup requirements

- Create a new robot in the [Viam app](https://app.viam.com) and follow the steps on the [setup tab](/installation/#installation-steps) to [install `viam-server`](/installation/) on your `customlinux` board and connect your board to the Viam app.
- On your `customlinux` board, create a file in your <file>/home/root</file> directory called <file>board.json</file> with your board's pin mappings:

{{< tabs >}}
{{% tab name="Template" %}}

```json
{
  "pins": [
    {
      "name": "<pin-name>",
      "device_name": "<device-name>",
      "line_number": <integer>,
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

The following parameters are available for pin mappings:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `name` | string | **Required** | The name of the pin. <br> Example: `"3"`. |
| `device_name` | string | **Required** | The device name. <br> Example: `"gpiochip0"`. |
| `line_number` | integer | **Required** | The line number of the pin. <br> Example: `81`. |
| `pwm_id` | integer | **Required** | The power management id of the pin. Example: `-1`. |

## Configure your board

{{< tabs name="Configure a customlinux board" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `board` type, then select the `customlinux` model.
Enter a name for your `customlinux` board and click **Create**.

![An example configuration for a customlinux board in the Viam app Config Builder.](/components/board/customlinux-ui-config.png)

Copy and paste the following attribute template into your board's **Attributes** box.
Then edit the attribute as applicable to your board, according to the table below.

{{< tabs >}}
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

The following attributes are available for `board/customlinux` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board_defs_file_path` | string | **Required** | The path to the pin mappings. See [Setup requirements](#setup-requirements). |
