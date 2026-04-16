---
linkTitle: "Add a remote part"
title: "Add a remote part"
weight: 20
layout: "docs"
type: "docs"
description: "Connect to another machine's resources by adding it as a remote part with an address and API key."
date: "2026-04-16"
---

A remote part is a connection you configure yourself between two machines.
You supply the address and authentication.
Unlike a sub-part, the two machines stay separate in the Viam app, can live in different organizations, and the connection can run in either direction (or both).
If you have not chosen between a sub-part and a remote part yet, start at the [multi-machine overview](/hardware/multi-machine/).

## Before you start

- Both machines exist and are online. Each one shows as **Live** on its machine page.
- You have access to the machine you want to connect to. You need enough access to view its **CONNECT** tab and generate an API key.

## 1. Get the remote's connection info

On the machine you want to connect to:

1. Open the machine's page and go to the **CONNECT** tab.
2. Click **Configure as a remote part** in the left-hand menu.
3. Toggle **Include API key** on.
4. Copy the entire JSON snippet. It looks like:

```json
{
  "name": "warehouse-cam",
  "address": "your-remote-main.abc123.viam.cloud:8080",
  "auth": {
    "credentials": {
      "type": "api-key",
      "payload": "<api-key-payload>"
    },
    "entity": "<api-key-id>"
  }
}
```

The `entity` field is the API key's ID, separate from the secret payload.
Authentication requires both.
Treat the payload like a password: anyone with it can connect to that machine.

## 2. Add the remote on your machine

On the machine initiating the connection:

1. Go to the **CONFIGURE** tab.
2. Click the **+** icon next to your part's name and select **Remote part**.
3. You have two options:
   - **Pick from a list** (both machines are in the same organization): select the remote machine from the list.
   - **Add empty remote**: click this, scroll to the new card, click **{}** (Switch to advanced), and paste the JSON snippet from step 1.
4. Click **Save**.

The remote part is now part of your machine's configuration.

## 3. Optional: set a prefix

If you connect multiple remotes and some export components with the same names, add a `prefix` to the remote config.
The prefix is prepended to every resource name coming from that remote.

Prefixes are concatenated directly, with no separator.
To keep names readable, end your prefix with `-` or `_`:

```json
{
  "name": "line-cam-3",
  "address": "...",
  "auth": {
    "credentials": { "type": "api-key", "payload": "..." },
    "entity": "..."
  },
  "prefix": "line-cam-3-"
}
```

A component named `camera` on that remote becomes `line-cam-3-camera` rather than `line-cam-3camera`.

## 4. Confirm the connection

Within a few seconds of saving, the remote's resources appear in your machine's resource list.
Unreachable remote resources are marked as such rather than disappearing, so you can tell the difference between a misconfigured connection and a remote that is currently offline.

If resources do not appear:

- Verify the address field matches the remote machine's current address (shown on its **CONNECT** tab).
- Confirm the API key has not been revoked on the remote machine.
- Check that the remote machine is still **Live**.

## Bidirectional access

A remote connection is one-way.
If machine A adds machine B as a remote, A can access B's resources, but B cannot access A's.

For both sides to see each other, repeat steps 1 and 2 with the roles reversed: go to machine A's **CONNECT** tab, copy its remote config, and add it to machine B's configuration.
The result is two independent one-way connections, not one two-way connection.

## From your code

Resources on a remote part use the same `from_robot` call as local components:

```python
gripper = Gripper.from_robot(machine, "gripper")              # local
camera = Camera.from_robot(machine, "line-cam-3-camera")      # remote with prefix
```

If the remote is disconnected when you call one of its resources, the call raises an error.
The connection reconnects automatically in the background, so subsequent calls may succeed once the remote is reachable again.

## Frames

By default, a remote's resources attach at the world origin of your machine's frame tree.
For spatial setups where the remote's hardware has a known physical offset, configure the remote's `frame` field.
See [Frames across machines](/hardware/multi-machine/cross-machine-frames/).
