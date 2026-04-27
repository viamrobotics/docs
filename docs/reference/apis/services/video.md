---
title: "Video service API"
linkTitle: "Video"
weight: 55
type: "docs"
tags: ["video", "services", "rtsp", "camera"]
description: "Stream stored video from an RTSP camera between specified timestamps."
date: "2026-04-23"
---

The video service API allows you to stream recorded video from an RTSP camera between two timestamps, and to manage stored video segments.

The [Video service](/reference/services/video/) supports the following methods:

<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetVideo`](#getvideo) | Stream video chunks between two timestamps. |
| [`DoCommand`](#docommand) | Execute model-specific commands, including `save`, `fetch`, and `get-storage-state`. |

## API

### GetVideo

Stream video chunks between two timestamps.

**Parameters:**

- `start_time` [(timestamp)](https://pkg.go.dev/time#Time): Start of the video range, in RFC 3339 format.
- `end_time` [(timestamp)](https://pkg.go.dev/time#Time): End of the video range, in RFC 3339 format.
- `video_codec` (string): Requested video codec. Currently ignored; the server chooses the codec.
- `video_container` (string): Container format. `mp4` for progressive playback or `fmp4` for streaming playback. Defaults to `mp4`.

**Returns:**

- A channel of `Chunk` objects. Each chunk has the following fields:

<!-- prettier-ignore -->
| Field | Type | Description |
| ----- | ---- | ----------- |
| `data` | bytes | Video chunk data. |
| `container` | string | Container format of the chunk (`mp4` or `fmp4`). |

**Container formats:**

<!-- prettier-ignore -->
| Format | Description |
| ------ | ----------- |
| `mp4` | Standard MP4 with the `faststart` flag. The `moov` atom is placed at the beginning for progressive playback. Best for downloading complete files. |
| `fmp4` | Fragmented MP4 with the `frag_keyframe+default_base_moof` flags. Optimized for streaming playback. Best for live or real-time consumption. |

### DoCommand

Execute model-specific commands.

The `viam:viamrtsp:video-service` model supports the following commands:

<!-- prettier-ignore -->
| Command | Description |
| ------- | ----------- |
| `save` | Concatenate and save video clips to the configured `upload_path`. |
| `fetch` | Retrieve video bytes directly. |
| `get-storage-state` | Get storage status and available video ranges. |

For request and response formats, see the [viamrtsp module README](https://github.com/viam-modules/viamrtsp).

**Parameters:**

- `command` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
