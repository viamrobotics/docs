---
title: "Configure an esp32-camera (Micro-RDK)"
linkTitle: "esp32-camera (Micro-RDK)"
weight: 33
type: "docs"
description: "Configure a camera connected to an esp32 board, initialized and configured using esp-idf."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components", "Micro-RDK"]
component_description: "An `OV2640` or `OV3660` camera connected to an esp32 board."
micrordk_component: true
toc_hide: true
date: "2024-08-28"
aliases:
  - /components/camera/esp32-camera/
# updated: ""  # When the content was last entirely checked
# SMEs: Matt Perez, Micro-RDK team
---

`esp32-camera` is the camera model that supports all cameras that work with Espressif's [esp32-camera drivers](https://github.com/espressif/esp32-camera) including:

- `OV2640`

  - [Datasheet](https://www.uctronics.com/download/OV2640_DS.pdf)
  - 1600 x 1200, Color, ¼” lens
  - You can use a cam ribbon adapter to connect to your `esp32` board

- `OV3660`: an [m5 camera timer module](https://docs.m5stack.com/en/unit/timercam_f)
  - [Datasheet](https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/unit/OV3660_CSP3_DS_1.3_sida.pdf)
  - 2048 x 1536, Color, ⅕” lens

For example, the `OV2640` with a ribbon cable connected to an ESP32:

{{< imgproc src="/components/camera/esp32-camera-2640.png" alt="Fake Camera on the ESP32" resize="300x" class="shadow" >}}

{{< alert title="Software requirements" color="note" >}}
To use this model, you must follow the [Set up an ESP32 guide](/operate/install/setup-micro/#build-and-flash-custom-firmware), which enables you to install and activate the ESP-IDF.
When you create a new project with `cargo generate`, select the option to include camera module traits when prompted.
Finish building and flashing custom firmware, then return to this guide.
{{< /alert >}}

{{< alert title="Data management not supported" color="caution" >}}

The `esp32-camera` camera model does not currently support the [data management service](/data-ai/capture-data/capture-sync/).

{{< /alert >}}

First, connect your camera to your machine's microcontroller and turn the microcontroller on.
Then, configure your camera:

{{< tabs name="Configure a esp32-camera" >}}
{{% tab name="JSON Template" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Select **JSON** mode.
Copy and paste the following JSON into your existing machine configuration into the `"components"` array:

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "my-esp32camera",
    "api": "rdk:component:camera",
    "model": "esp32-camera",
    "attributes": {
        "pin_d4": <int>,
        "jpeg_quality": <int>,
        "frame_size": <int>,
        "pin_d5": <int>,
        "pin_d3": <int>,
        "pin_d6": <int>,
        "pin_vsync": <int>,
        "ledc_timer": <int>,
        "pin_d7": <int>,
        "pin_sccb_sda": <int>,
        "pin_href": <int>,
        "pin_sccb_scl": <int>,
        "sccb_i2c_port": <int>,
        "pin_d1": <int>,
        "pin_d0": <int>,
        "pin_xclk": <int>,
        "pin_reset": <int>,
        "pin_pclk": <int>,
        "pin_d2": <int>,
        "xclk_freq_hz": <int>,
        "ledc_channel": <int>
    }
}
```

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Example: OV2640" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my-esp32camera",
  "api": "rdk:component:camera",
  "model": "esp32-camera",
  "attributes": {
    "pin_pwdn": -1,
    "pin_reset": -1,
    "pin_xclk": 21,
    "pin_sccb_sda": 26,
    "pin_sccb_scl": 27,
    "pin_d7": 35,
    "pin_d6": 34,
    "pin_d5": 39,
    "pin_d4": 36,
    "pin_d3": 19,
    "pin_d2": 18,
    "pin_d1": 5,
    "pin_d0": 4,
    "pin_vsync": 25,
    "pin_href": 23,
    "pin_pclk": 22,
    "xclk_freq_hz": 20000000,
    "ledc_timer": 1,
    "ledc_channel": 1
  }
}
```

{{% /tab %}}
{{% tab name="JSON Example: OV3660" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my-esp32camera",
  "api": "rdk:component:camera",
  "model": "esp32-camera",
  "attributes": {
    "pin_d4": 39,
    "jpeg_quality": 32,
    "frame_size": 5,
    "pin_d5": 18,
    "pin_d3": 5,
    "pin_d6": 36,
    "pin_vsync": 22,
    "ledc_timer": 1,
    "pin_d7": 19,
    "pin_sccb_sda": 25,
    "pin_href": 26,
    "pin_sccb_scl": 23,
    "sccb_i2c_port": -1,
    "pin_d1": 35,
    "pin_d0": 32,
    "pin_xclk": 27,
    "pin_reset": 15,
    "pin_pclk": 21,
    "pin_d2": 34,
    "xclk_freq_hz": 20000000,
    "ledc_channel": 1
  }
}
```

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Note" color="note" %}}
While the following attributes marked as **Optional** do have defaults, it is recommended that you configure them according to your datasheet as your device may not align with the defaults which could cause damage to your board or camera.
{{% /alert %}}

The following attributes are available for `esp32-camera` cameras:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `pin_pwdn` | int | Optional | GPIO pin for camera power down line. <br> Default: -1 |
| `pin_reset` | int | Optional | GPIO pin for camera reset line. <br> Default: -1 |
| `pin_xclk` | int | Optional | GPIO pin for camera XCLK line. <br> Default: 21 |
| `pin_sccb_sda` | int | Optional | GPIO pin for camera SDA line. <br> Default: 26 |
| `pin_sccb_scl` | int | Optional | GPIO pin for camera SCL line. <br> Default: 27 |
| `pin_d7` | int | Optional | GPIO pin for camera D7 line. <br> Default: 35|
| `pin_d6` | int | Optional | GPIO pin for camera D6 line. <br> Default: 34 |
| `pin_d5` | int | Optional | GPIO pin for camera D5 line. <br> Default: 39 |
| `pin_d4` | int | Optional | GPIO pin for camera D4 line. <br> Default: 36 |
| `pin_d3` | int | Optional | GPIO pin for camera D3 line. <br> Default: 19 |
| `pin_d2` | int | Optional | GPIO pin for camera D2 line. <br> Default: 18 |
| `pin_d1` | int | Optional | GPIO pin for camera D1 line. <br> Default: 5 |
| `pin_d0` | int | Optional | GPIO pin for camera D0 line. <br> Default: 4 |
| `pin_vsync` | int | Optional | GPIO pin for camera VSYNC line. <br> Default: 25 |
| `pin_href` | int | Optional | GPIO pin for camera HREF line. <br> Default: 23 |
| `pin_pclk` | int | Optional | GPIO pin for camera PLCK line. <br> Default: 22 |
| `xclk_freq_hz` | int | Optional | Frequency of XCLK signal, in Hz. <br> Experimental: Set to 16MHz on ESP32-S2 or ESP32-S3 to enable EDMA mode. <br> Default: 20000000 |
| `ledc_timer` | int | Optional | LEDC timer to generate XCLK. <br> Default: 1 |
| `ledc_channel` | int | Optional | LEDC channel to generate XCLK. <br> Default: 1 |
| `frame_size` | int | Optional | Size of the output image. <br> Default: 1 |
| `jpeg_quality` | int | Optional | Quality of JPEG output. Lower means higher quality. <br> Range: 0-63 <br> Default: 32 |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/camera.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/camera/" customTitle="Camera API" noimage="true" %}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{< /cards >}}
