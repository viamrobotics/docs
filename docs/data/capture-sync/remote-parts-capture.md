---
linkTitle: "Capture from remote parts"
title: "Capture from remote parts"
weight: 15
layout: "docs"
type: "docs"
description: "Capture data from components on a remote machine part and sync it through the main part."
date: "2025-02-10"
---

Capture data from components on a machine part that you can't or don't want to run data capture on directly. You add the remote part to your main machine, then configure data capture on the main part for resources on the remote. The main part handles capture and sync; the remote part just provides access to its components.

This is useful when:

- You want to centralize data capture on your main compute instead of configuring it on every part
- The remote part is a Raspberry Pi with a camera at a different location, and your main machine handles capture and sync
- The remote part has limited resources or unreliable connectivity

## Prerequisites

- A main machine with `viam-server` running and connected to the Viam app
- A remote machine part running `viam-server` or `viam-micro-server` with at least one configured component
- Both parts must be able to reach each other over the network

## 1. Add the remote part to your main machine

1. In the [Viam app](https://app.viam.com), go to your main machine's **CONFIGURE** tab.
2. Click the **+** button next to the main part's name.
3. Select **Remote part**.
4. Select the machine and part you want to add as a remote. The Viam app shows available parts automatically.
5. Click **Save**.

The main machine can now access all components on the remote part. You can verify this on the **CONTROL** tab, where the remote's components should appear.

For more details on configuring remotes, including authentication and manual JSON configuration, see [Machine architecture: parts](/operate/reference/architecture/parts/).

## 2. Configure data capture on the remote's components

Remote part capture is configured in JSON. Switch to **JSON** mode in the **CONFIGURE** tab.

Find the `remotes` array in your main part's configuration. Add a `service_configs` block inside the remote object with the capture methods you want:

```json
{
  "remotes": [
    {
      "name": "my-remote",
      "address": "my-remote-main.abc123.viam.cloud",
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "name": "rdk:component:sensor/my-sensor",
                "method": "Readings",
                "capture_frequency_hz": 0.5,
                "additional_params": {},
                "disabled": false
              }
            ]
          }
        }
      ]
    }
  ]
}
```

Key fields:

- **`name`**: the fully qualified resource name on the remote part, in the format `rdk:component:<type>/<name>`. This must match the component's API and name exactly.
- **`method`**: the capture method. See [Supported resources](/data/reference/#supported-resources) for available methods per component type.
- **`capture_frequency_hz`**: how often to capture, in hertz.

You can add multiple capture methods for different components on the same remote.

## 3. Make sure the data management service is configured

Your main part needs the data management service to handle capture and sync. If you already have data capture configured on the main part, this is already set up.

If not, add the data management service to your main part's `services` array:

```json
{
  "services": [
    {
      "name": "data_manager",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
      "attributes": {
        "sync_interval_mins": 0.1,
        "capture_dir": "",
        "sync_disabled": false
      }
    }
  ]
}
```

Click **Save**.

## 4. Verify data is being captured

Wait 30 seconds to a minute, then:

1. Click the **DATA** tab in the Viam app.
2. Filter by the main machine's name.
3. You should see data appearing from the remote part's components. The `component_name` will match the name on the remote part.

If no data appears, check:

- The remote part is online and accessible from the main part (verify on the **CONTROL** tab).
- The fully qualified resource name in the capture config matches the component exactly.
- The data management service is enabled with sync turned on.

## Example: capture camera images from a remote Pi

Your main machine runs an arm for pick-and-place operations. A Raspberry Pi at a different location has a camera monitoring the workspace. You want to capture images from the Pi's camera through the main machine so all data flows through one capture pipeline.

{{< expand "Raspberry Pi configuration (the remote part)" >}}

The Pi runs `viam-server` with a webcam configured:

```json
{
  "components": [
    {
      "name": "workspace-cam",
      "api": "rdk:component:camera",
      "model": "webcam",
      "attributes": {
        "video_path": "video0"
      }
    }
  ]
}
```

{{< /expand >}}

{{< expand "Main part configuration (arm machine that captures from the Pi)" >}}

The main machine has an arm and adds the Pi as a remote. Data capture on the remote's camera is configured in the `service_configs` block inside the `remotes` array:

```json
{
  "components": [
    {
      "name": "my-arm",
      "api": "rdk:component:arm",
      "model": "ur5e",
      "attributes": {}
    }
  ],
  "services": [
    {
      "name": "data_manager",
      "api": "rdk:service:data_manager",
      "model": "rdk:builtin:builtin",
      "attributes": {
        "capture_dir": "",
        "sync_disabled": false,
        "sync_interval_mins": 0.5,
        "tags": ["workspace-monitoring"]
      }
    }
  ],
  "remotes": [
    {
      "name": "pi-workspace",
      "address": "pi-workspace-main.abc123.viam.cloud",
      "service_configs": [
        {
          "type": "data_manager",
          "attributes": {
            "capture_methods": [
              {
                "name": "rdk:component:camera/workspace-cam",
                "method": "GetImages",
                "capture_frequency_hz": 0.5,
                "additional_params": {},
                "disabled": false
              }
            ]
          }
        }
      ]
    }
  ]
}
```

The main machine captures one image every 2 seconds from the Pi's camera and syncs it to the cloud alongside any data captured from local components.

{{< /expand >}}
