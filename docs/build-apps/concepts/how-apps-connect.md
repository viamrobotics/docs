---
linkTitle: "Connection model"
title: "How Viam client apps connect"
weight: 10
layout: "docs"
type: "docs"
description: "The transport paths the SDK uses, the session safety mechanism, and what the SDK reconnects automatically."
date: "2026-04-10"
---

A Viam client application needs to reach a machine that may be on a different network, behind a NAT, or both. This page describes the transport paths the SDK uses, the session safety mechanism, and how the SDK reconnects when the network drops.

This page uses TypeScript SDK names for specific APIs (`createRobotClient`, `DialWebRTCConf`, `disableSessions`, and so on). The Flutter SDK provides equivalent APIs with different names; see [Flutter setup](/build-apps/setup/flutter/).

## Two transports

The SDK reaches a machine through one of two transports, selected by which configuration type you pass to `createRobotClient`:

**WebRTC** (`DialWebRTCConf`). The default path for machines deployed on Viam Cloud. The SDK contacts a signaling service, which brokers a peer-to-peer WebRTC connection between your app and the machine. Once the connection is established, data flows directly between the two endpoints. The signaling service is only needed for the initial handshake.

**Direct gRPC** (`DialDirectConf`). The SDK opens a gRPC connection directly to a host and port. Use this when you have direct network access to the machine and do not need NAT traversal, typically for local development against a machine on the same network or for an app running in the same cluster as the machine.

Both transports use gRPC as the application protocol. The difference is whether the gRPC bytes travel through a WebRTC data channel (NAT-friendly, goes through signaling) or through a direct TCP/HTTP2 connection (simpler, requires direct network reachability).

## WebRTC connection parameters

When you use the WebRTC transport, the SDK needs two pieces of configuration in addition to the machine host:

**Signaling address.** Required. The URL of the signaling service that brokers the WebRTC handshake. For machines deployed on Viam Cloud, the value is `https://app.viam.com:443`. The Viam app's CONNECT tab writes this literal string into the code sample it generates, so you copy it along with the rest of the connection code. For self-hosted or air-gapped setups, you point to a different signaling service.

**ICE servers.** Optional. The SDK needs ICE servers (STUN and optionally TURN) to traverse NATs. If you do not pass `iceServers`, the SDK defaults to Twilio's public STUN server at `stun:global.stun.twilio.com:3478`. Override `iceServers` if you have custom STUN or TURN requirements for your network.

Most apps never change either field. See [the connectivity reference](/reference/sdks/connectivity/) for advanced options like TURN-only relay mode, forced peer-to-peer, and custom TURN URI overrides.

## Sessions

A session is a client-server association that the SDK creates automatically when you connect. Sessions exist to stop actuators when a client disappears.

The mechanism is a heartbeat protocol. The SDK calls `StartSession` on the machine, which returns a heartbeat window (default 2 seconds, configurable between 30&nbsp;ms and 1 minute). The SDK sends heartbeats within that window. If the heartbeats stop, because your browser tab crashed, your laptop lost Wi-Fi, or your app closed without calling `close()`, the server stops any resources that are safety-monitored **and** where this session was the last caller.

The practical effect: if your app called `motor.setPower(1)` and then crashed, the server stops the motor within a heartbeat window of the crash. The machine does not continue running the last command indefinitely.

### Which methods are safety-monitored

Not every method triggers a session stop. Only methods marked with the `safety_heartbeat_monitored` proto extension participate. The components with safety-monitored methods today:

- `arm` (motion commands)
- `base` (drive commands)
- `button`
- `gantry`
- `gripper`
- `motor` (power and position commands)
- `servo`
- `switch`

Read-only methods like `sensor.getReadings()` or `camera.getImage()` are not safety-monitored. Reading state from a component does not trigger a session stop.

### Disabling sessions

Pass `disableSessions: true` in the connection options to disable session heartbeating. The session proto documentation calls this "acknowledging the safety risk": if you disable sessions, a crashed client leaves actuators in whatever state they were last commanded to. Disable sessions only for specific reasons, such as implementing your own crash-detection and cleanup logic.

See [the sessions API reference](/reference/apis/sessions/) for the full protocol details.

## Reconnection

When the network drops, the SDK reconnects automatically with exponential backoff. The relevant options on `DialWebRTCConf` and `DialDirectConf`:

- `reconnectMaxAttempts` — default 10, the number of retries before giving up
- `reconnectMaxWait` — default `Number.POSITIVE_INFINITY`, the maximum time between retries
- `noReconnect` — default `false`, set to `true` to disable reconnection

Reconnection is transparent to your application code. The `RobotClient` object stays valid across the drop, and in-flight method calls throw errors that your app can catch and retry after the reconnection completes.

What does _not_ happen automatically is your app's UI state. If you were showing a camera stream when the network dropped, the stream stops, and your UI has to rebuild the stream when the connection returns. If you were polling a sensor, the polling stops, and your UI has to resume polling. The SDK reconnects the transport; your app reconnects its own state.

Subscribe to `MachineConnectionEvent` to react to connection state changes. See [Handle disconnection and reconnection](/build-apps/tasks/handle-connection-state/) for the pattern.
