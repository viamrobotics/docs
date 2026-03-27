---
linkTitle: "Capture from remote parts"
title: "Capture from remote parts"
weight: 15
layout: "docs"
type: "docs"
description: "Capture data from resources on remote machine parts that lack the OS or resources to run viam-server."
date: "2025-02-10"
---

Capture data from {{< glossary_tooltip term_id="resource" text="resources" >}} on {{< glossary_tooltip term_id="remote-part" text="remote parts" >}}. This is useful when a part lacks the OS or resources to run `viam-server`. You add it as a remote and capture its data from the main part.

Remote part capture is configured in JSON only.
Add a `service_config` with `type: data_manager` inside the `remote` object in the `remotes` array.

## Capture method fields

Each capture method object takes the following fields:

<!-- prettier-ignore -->
| Key | Type | Description |
| --- | ---- | ----------- |
| `name` | string | Fully qualified resource name. Example: `"rdk:component:sensor/spacesensor"`. |
| `method` | string | Depends on the component or service type. See [Supported resources](/data/reference/#supported-resources). Individual tabular readings larger than 4&nbsp;MB are rejected at upload time. |
| `capture_frequency_hz` | float | Frequency in hertz. |
| `additional_params` | object | Method-specific parameters. |
| `disabled` | boolean | Whether capture is disabled for this method. |
| `cache_size_kb` | float | `viam-micro-server` only. Max storage (KB) per data collector. Default: `1`. |

## Examples

{{< expand "ESP32 remote part configuration" >}}

The following is the configuration for the ESP32 board itself (the remote part).
This config is the same as any non-remote part. The remote connection is established by the main part.

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "my-esp32",
      "model": "esp32",
      "api": "rdk:component:board",
      "attributes": {
        "pins": [27],
        "analogs": [
          {
            "pin": "34",
            "name": "A1"
          },
          {
            "pin": "35",
            "name": "A2"
          }
        ]
      },
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Analogs",
                "additional_params": {
                  "reader_name": "A1"
                },
                "cache_size_kb": 10,
                "capture_frequency_hz": 10
              },
              {
                "method": "Analogs",
                "additional_params": {
                  "reader_name": "A2"
                },
                "cache_size_kb": 10,
                "capture_frequency_hz": 10
              }
            ]
          }
        }
      ]
    }
  ]
}
```

{{< /expand >}}

{{< expand "Main part capturing from an ESP32 remote (analog readers and GPIO)" >}}

This main part configuration captures data from two analog readers and pin 27 of the GPIO on the ESP32 configured above:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "name": "data_manager",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
      "attributes": {
        "capture_dir": "",
        "sync_disabled": true,
        "sync_interval_mins": 5,
        "tags": ["tag1", "tag2"]
      }
    }
  ],
  "remotes": [
    {
      "name": "esp-home",
      "address": "esp-home-main.33vvxnbbw9.viam.cloud:80",
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "method": "Analogs",
                "capture_frequency_hz": 1,
                "cache_size_kb": 10,
                "name": "rdk:component:board/my-esp32",
                "additional_params": { "reader_name": "A1" },
                "disabled": false
              },
              {
                "method": "Analogs",
                "capture_frequency_hz": 1,
                "cache_size_kb": 10,
                "name": "rdk:component:board/my-esp32",
                "additional_params": { "reader_name": "A2" },
                "disabled": false
              },
              {
                "method": "Gpios",
                "capture_frequency_hz": 1,
                "cache_size_kb": 10,
                "name": "rdk:component:board/my-esp32",
                "additional_params": {
                  "pin_name": "27"
                },
                "disabled": false
              }
            ]
          }
        }
      ],
      "secret": "REDACTED"
    }
  ]
}
```

{{< /expand >}}

{{< expand "Main part capturing from a remote camera" >}}

This main part configuration captures from the `GetImages` method of a camera on a remote part:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "name": "data_manager",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
      "attributes": {
        "capture_dir": "",
        "sync_disabled": true,
        "sync_interval_mins": 5,
        "tags": []
      }
    }
  ],
  "remotes": [
    {
      "name": "pi-test-main",
      "address": "pi-test-main.vw3iu72d8n.viam.cloud",
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "capture_frequency_hz": 1,
                "name": "rdk:component:camera/cam",
                "disabled": false,
                "method": "GetImages",
                "additional_params": {
                  "filter_source_names": ["color"],
                  "reader_name": "cam1"
                }
              }
            ]
          }
        }
      ],
      "secret": "REDACTED"
    }
  ]
}
```

{{< /expand >}}
