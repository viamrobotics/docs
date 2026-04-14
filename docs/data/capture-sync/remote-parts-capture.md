---
linkTitle: "Multi-part capture"
title: "Capture data from multi-part machines"
weight: 15
layout: "docs"
type: "docs"
description: "Capture and sync data from components on sub-parts and remote parts of a multi-part machine."
date: "2025-02-10"
---

Viam machines can be split across multiple computers. When that happens, data capture behaves differently depending on whether the additional computer is a sub-part or a remote part. Understanding which pattern you have is the key to configuring capture correctly.

## Terminology

- **Sub-part**: an additional part of the _same_ machine. Each sub-part runs its own `viam-server` with its own configuration and its own filesystem.
- **Remote part**: a part of a _different_ machine that yours accesses over the network. A remote part is itself a separate machine in the Viam app.

## How capture differs

|                                       | Sub-part                                     | Remote part                |
| ------------------------------------- | -------------------------------------------- | -------------------------- |
| Data manager lives on                 | The sub-part itself                          | The main part              |
| `.capture` files are written to       | The sub-part's filesystem                    | The main part's filesystem |
| Sync uploads from                     | The sub-part                                 | The main part              |
| Where you configure capture           | The sub-part's section of the machine config | The main machine's config  |
| Captured metadata `part_id` is set to | The sub-part's `part_id`                     | The main part's `part_id`  |

All captured data from a multi-part _machine_ shares the same `robot_id` (machine UUID), so you can query across all parts of one multi-part machine in a single SQL or MQL query. Data from a remote part that belongs to a different machine has a different `robot_id`.

## Sub-parts

Each sub-part is an independent `viam-server` instance with its own configuration and dependency graph. The main part's data manager cannot reach into a sub-part to capture its resources; the sub-part needs its own data manager service.

### Configure data capture on a sub-part

1. In the Viam app, navigate to the sub-part's section of your machine's **CONFIGURE** tab.
2. Find the component on the sub-part that you want to capture from.
3. Click **+** on the component's **Data Capture** card.
4. If you see a "Data management service missing" banner, click
   **Create data management service**, click **Save**, navigate back to
   the component, and click **+** on the **Data Capture** card again.
5. Select the capture method and frequency as you would for a local component.
6. Click **Save**.

The sub-part's `viam-server` writes `.capture` files to its own local capture directory and syncs them to the cloud from there. In the **DATA** tab, the rows appear under the main machine, but the captured metadata carries the sub-part's `part_id`.

## Remote parts

Remote parts appear in the main part's dependency graph, and the main part's data manager can be configured to capture from them exactly like local resources. All capture and sync happens on the main part's host.

### 1. Add the remote part to your main machine

1. In the Viam app, navigate to your main machine's **CONFIGURE** tab.
2. Click the **+** button next to the main part's name.
3. Select **Remote part**.
4. Select the machine and part you want to add as a remote. The Viam app lists parts you have access to.
5. Click **Save**.

The main machine can now access all components on the remote part. You can verify this on the **CONTROL** tab, where the remote's components appear under the remote's section.

For more details on remote part configuration, including authentication and manual JSON, see the Viam app's **CONFIGURE** tab for your machine.

### 2. Configure data capture on the remote's components

Once the remote part is added, its components appear on the main machine's **CONFIGURE** tab under the remote's section. Configure data capture through the main machine's config, not through the remote machine's config:

1. Find the remote component in the main machine's **CONFIGURE** tab.
2. Click **+** on the component's **Data Capture** card.
3. Select the capture method (for example, **GetImages** for a camera, **Readings** for a sensor).
4. Set the capture frequency.
5. Click **Save**.

The main part captures and syncs the remote's data. Files are written to the main part's capture directory and uploaded to the cloud from there.

{{< alert title="Do not configure capture on both parts" color="caution" >}}
If the remote part also has its own data management service with capture enabled on the same components, you will get duplicate `.capture` files and duplicate rows in the cloud. Configure capture on the main part only, and confirm that the remote machine's data manager does not have overlapping capture methods.
{{< /alert >}}

### 3. Verify data is being captured

Wait 30 seconds to a minute, then:

1. Click the **DATA** tab in the Viam app.
2. Filter by the main machine's name.
3. For cameras, captured images appear under **Images**. For sensors, click **Sensors** to see the latest reading per resource.
4. The captured `component_name` matches the name the component has on the remote part.

If no data appears, check:

- The remote part is online and reachable from the main part (verify on the **CONTROL** tab).
- The data management service on the main part has capture and sync enabled.
- The capture method is configured on the remote component in the **main machine's** config, not the remote machine's config.

## Example: capture camera images from a remote Pi

Your main machine runs an arm for pick-and-place operations. A Raspberry Pi at a different location has a camera monitoring the workspace and is registered as its own Viam machine. You want to capture images from the Pi's camera through the main arm machine so all data flows through one capture pipeline.

1. Configure the Pi as its own Viam machine with a webcam component.
2. On your main arm machine, add the Pi's machine part as a remote part (see [Add the remote part](#1-add-the-remote-part-to-your-main-machine)).
3. On the main machine's **CONFIGURE** tab, find the Pi's `workspace-cam` component under the remote part section.
4. Add data capture on `workspace-cam` with method **GetImages** at 0.5 Hz (one image every 2 seconds).
5. Click **Save**.

The main machine captures images from the Pi's camera and syncs them to the cloud alongside any data captured from its own local components. The Pi itself does not need a data management service for this flow.
