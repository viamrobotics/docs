---
linkTitle: "Stream video"
title: "Stream video"
weight: 60
layout: "docs"
type: "docs"
description: "Display live camera feeds in a client app. Covers single-camera and multi-camera streaming, resolution tradeoffs, and bandwidth considerations."
date: "2026-04-10"
---

Display a live camera feed from a Viam machine in your client app. The TypeScript and Flutter SDKs use WebRTC for video streaming, which gives low latency suitable for teleoperation. Python, Go, and C++ access camera data through single-frame methods (`get_images`, `GetImages`) rather than WebRTC streams; for live video in those languages, poll `get_images` on a timer. This page focuses on the WebRTC streaming path available in TypeScript and Flutter.

## Prerequisites

- A project with an active machine connection (see [Connect to a machine](./connect-to-machine/))
- A camera component configured on the machine. Any camera model will work, including `fake:camera` for testing without real hardware.

## Stream one camera

{{< tabs >}}
{{% tab name="TypeScript" %}}

Create a `StreamClient` from your `RobotClient` and call `getStream(name)` to get a `MediaStream`. Attach it to an HTML `<video>` element:

```html
<video id="camera" autoplay playsinline muted></video>
```

```ts
import * as VIAM from "@viamrobotics/sdk";

const streamClient = new VIAM.StreamClient(machine);
const mediaStream = await streamClient.getStream("my_camera");

const videoEl = document.getElementById("camera") as HTMLVideoElement;
videoEl.srcObject = mediaStream;
```

`getStream` waits up to 5 seconds for the first video track to arrive, then resolves with a `MediaStream`. The `<video>` element must have `autoplay`, `playsinline`, and `muted` attributes to play a `MediaStream` without user interaction in most browsers.

To stop a stream, call `remove` with the camera name:

```ts
await streamClient.remove("my_camera");
```

{{% /tab %}}
{{% tab name="Flutter" %}}

The Flutter SDK ships a `ViamCameraStreamView` widget that handles the WebRTC renderer internally. Obtain a `Camera` component and a `StreamClient` from your `RobotClient`, then pass both to the widget:

```dart
import 'package:flutter/material.dart';
import 'package:viam_sdk/viam_sdk.dart';
import 'package:viam_sdk/widgets.dart';

class CameraView extends StatelessWidget {
  final RobotClient robot;
  const CameraView({super.key, required this.robot});

  @override
  Widget build(BuildContext context) {
    final camera = Camera.fromRobot(robot, 'my_camera');
    final streamClient = robot.getStream('my_camera');
    return ViamCameraStreamView(
      camera: camera,
      streamClient: streamClient,
    );
  }
}
```

`ViamCameraStreamView` manages the underlying `RTCVideoRenderer`, tears it down in `dispose()`, and displays an error state if the stream fails.

{{% /tab %}}
{{< /tabs >}}

## Stream multiple cameras

Multiple cameras work the same way as one: call `getStream` (TypeScript) or `robot.getStream` plus `ViamCameraStreamView` (Flutter) once per camera name.

{{< tabs >}}
{{% tab name="TypeScript" %}}

```ts
const streamClient = new VIAM.StreamClient(machine);

const frontStream = await streamClient.getStream("front_camera");
const rearStream = await streamClient.getStream("rear_camera");

(document.getElementById("front") as HTMLVideoElement).srcObject = frontStream;
(document.getElementById("rear") as HTMLVideoElement).srcObject = rearStream;
```

A single `StreamClient` can manage multiple streams. You do not need one client per camera.

{{% /tab %}}
{{% tab name="Flutter" %}}

The Flutter SDK also ships a `ViamMultiCameraStreamView` widget for multi-camera layouts, which handles the stream management for several cameras at once. See the [Flutter SDK reference](https://flutter.viam.dev/) for the widget's parameters.

{{% /tab %}}
{{< /tabs >}}

### Hardware and bandwidth limits

Streaming more than two or three cameras at once from the same machine is unreliable on typical hardware. Reported failure modes from practitioners:

- **USB bandwidth ceilings.** Stacking several USB cameras on the same host saturates the bus before the WebRTC encoder does. Cameras appear to connect but deliver corrupt or empty frames.
- **WebRTC peer connection limits.** Some host hardware cannot negotiate more than three simultaneous WebRTC video tracks. The third or fourth `getStream` call hangs or times out.
- **Cellular bandwidth cost.** A single 720p camera stream can use 1-3 Mbps sustained. On a cellular deployment, two or three simultaneous streams can burn through a monthly data cap in days.

If you need more than two cameras in one UI, drop resolution first, then consider whether you can show one camera at a time and let the user switch.

## Resolution and bandwidth

Lower resolutions use less bandwidth and CPU on both ends. The TypeScript SDK exposes resolution control on `StreamClient`:

```ts
// See what resolutions the camera advertises
const options = await streamClient.getOptions("my_camera");
console.log(options);

// Set a specific resolution (width, height in pixels)
await streamClient.setOptions("my_camera", 640, 480);

// Reset to the camera's default
await streamClient.resetOptions("my_camera");
```

`setOptions` takes effect on the next `getStream` call for that camera. If you change the resolution while a stream is active, remove and re-add the stream to apply the change.

Practical guidance:

- **Teleoperation of a vehicle or arm.** Prioritize framerate and latency over resolution. 640x480 at 30 fps is usually better than 1920x1080 at 5 fps.
- **Inspection dashboards where the user stares at one feed.** Higher resolution helps. Use the camera's native resolution unless bandwidth is a hard constraint.
- **Multi-camera fleet overviews.** Drop every stream to the lowest useful resolution. The user is scanning, not inspecting.

## Reconnection behavior

The TypeScript SDK's `StreamClient` tracks open streams and automatically re-adds them when the `RobotClient` reconnects. Your app does not need to re-call `getStream`, but the HTML `<video>` element may still need its `srcObject` reattached because the old `MediaStream` object becomes invalid. A simple pattern is to re-run the `getStream` and `videoEl.srcObject = mediaStream` assignment inside your connection-state handler.

In the Flutter SDK, `StreamClient` does not explicitly re-add streams on reconnect. If a stream becomes inactive after a disconnection, tear down the `ViamCameraStreamView` and recreate it, or listen for connection-state changes and restart the stream manually.

See [Handle disconnection and reconnection](./handle-connection-state/) for the connection-event pattern.

## Next

- [Handle disconnection and reconnection](./handle-connection-state/) for the rebuild-after-reconnect pattern
- [Query captured data](./query-data/) for reading captured data alongside live streams
- [Camera component reference](/reference/components/camera/) for per-model configuration
