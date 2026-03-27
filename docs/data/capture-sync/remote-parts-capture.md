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

Once the remote part is added, its components appear on the main machine's **CONFIGURE** tab. Configure data capture on them the same way you would for local components:

1. Find the remote component in the **CONFIGURE** tab (it appears under the remote part's section).
2. Scroll to the **Data capture** section on the component card.
3. Click **+ Add method**.
4. Select the capture method (for example, **GetImages** for a camera, **Readings** for a sensor).
5. Set the capture frequency.
6. Click **Save**.

The main part handles capture and sync for the remote component. Data is written to the main part's capture directory and synced from there.

## 3. Verify data is being captured

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

**Raspberry Pi configuration (the remote part):**

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

**Main part configuration (arm machine that captures from the Pi):**

The main machine has an arm and adds the Pi as a remote. After adding the remote through the UI, you configure data capture on the remote's camera from the **CONFIGURE** tab, or in JSON:

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
