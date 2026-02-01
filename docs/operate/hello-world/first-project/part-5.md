---
linkTitle: "Part 5: Scale"
title: "Part 5: Scale"
weight: 50
layout: "docs"
type: "docs"
description: "Add a second inspection station using fragments for configuration reuse."
date: "2025-01-30"
---

**Goal:** Add a second inspection station using fragments.

**Skills:** Configuration reuse with fragments, fleet basics.

**Time:** ~10 min

## 5.1 Create a Fragment

You have one working inspection station. Now imagine you need 10 more—or 100. Manually copying configuration to each machine would be tedious and error-prone.

Viam solves this with _fragments_: reusable configuration blocks that can be applied to any machine. Think of a fragment as a template. Define your camera, vision service, data capture, and triggers once, then apply that template to as many machines as you need.

**Export your machine configuration:**

1. Go to your `inspection-station-1` machine in the Viam app
2. Click the **Configure** tab
3. Click **JSON** (top right) to see the raw configuration
4. Click **Copy** to copy the entire JSON to your clipboard

[SCREENSHOT: JSON configuration view with copy button]

**Create the fragment:**

1. In the Viam app, click **Fragments** in the left sidebar
2. Click **+ Create fragment**
3. Name it `inspection-station`
4. Paste your configuration into the fragment editor
5. Click **Save**

[SCREENSHOT: Fragment editor with pasted configuration]

## 5.2 Parameterize the Camera ID

Your fragment now contains everything—but one value is specific to each machine: the camera ID. Station 1 uses `/inspection_camera`, but Station 2 uses `/station_2_camera`. Hardcoding this value would break the fragment's reusability.

Viam fragments support _variables_ for exactly this purpose.

**Find the camera configuration in your fragment:**

Look for the camera component in the JSON. It looks like this:

```json
{
  "name": "inspection-cam",
  "type": "camera",
  "model": "viam:camera:gazebo",
  "attributes": {
    "id": "/inspection_camera"
  }
}
```

**Replace the hardcoded topic with a variable:**

Change the `id` attribute to use the `$variable` syntax:

```json
{
  "name": "inspection-cam",
  "type": "camera",
  "model": "viam:camera:gazebo",
  "attributes": {
    "id": {
      "$variable": {
        "name": "camera_id"
      }
    }
  }
}
```

Click **Save** to update the fragment.

Now when you apply this fragment to a machine, you'll provide the actual `camera_id` value for that specific station.

{{< alert title="What to parameterize" color="tip" >}}
Camera IDs, device paths (`/dev/video0`), IP addresses, serial numbers—anything that varies between physical machines. Configuration like detection thresholds, capture frequency, and module versions should stay in the fragment so they're consistent across your fleet.
{{< /alert >}}

## 5.3 Stop Station 1

Before starting the second station, stop the first one to free up system resources. The simulation is CPU-intensive, so running both simultaneously isn't practical on most machines.

{{< tabs >}}
{{% tab name="Mac/Linux" %}}

```bash
docker stop gz-station1
```

{{% /tab %}}
{{% tab name="Windows (PowerShell)" %}}

```powershell
docker stop gz-station1
```

{{% /tab %}}
{{< /tabs >}}

Your `inspection-station-1` machine will show as offline in the Viam app—that's expected.

## 5.4 Start Station 2

Station 2 is a visually distinct simulation with different camera IDs. You'll notice yellow rails, an orange reject bin, and a blue output chute—so you can easily tell which station you're viewing.

{{< tabs >}}
{{% tab name="Mac/Linux" %}}

```bash
docker run --name gz-station2 -d \
  -p 8080:8080 -p 8081:8081 -p 8443:8443 \
  --entrypoint /entrypoint_station2.sh \
  gz-harmonic-viam
```

{{% /tab %}}
{{% tab name="Windows (PowerShell)" %}}

```powershell
docker run --name gz-station2 -d `
  -p 8080:8080 -p 8081:8081 -p 8443:8443 `
  --entrypoint /entrypoint_station2.sh `
  gz-harmonic-viam
```

{{% /tab %}}
{{< /tabs >}}

Wait about 20 seconds for the simulation to initialize, then open the web viewer:

`http://localhost:8081`

You should see the Station 2 simulation with its distinct color scheme: yellow rails, orange reject bin, and blue output chute.

[SCREENSHOT: Station 2 web viewer showing distinct color scheme]

## 5.5 Create the Second Machine

Now create a machine in Viam for Station 2:

1. In the Viam app, click **+ Add machine**
2. Name it `inspection-station-2`
3. Click **Create**

**Copy the viam-server install command** from the **Setup** tab. You'll need the machine credentials to configure viam-server.

## 5.6 Configure viam-server for Station 2

Create a Viam configuration file for Station 2. Replace the placeholder values with your actual machine credentials from the Setup tab:

{{< tabs >}}
{{% tab name="Mac/Linux" %}}

Create the config file:

```bash
cat > ~/viam/config/station2-viam.json << 'EOF'
{
  "cloud": {
    "id": "YOUR_MACHINE_ID",
    "secret": "YOUR_MACHINE_SECRET",
    "app_address": "https://app.viam.com:443"
  }
}
EOF
```

Stop and restart the container with the config mounted:

```bash
docker stop gz-station2 && docker rm gz-station2

docker run --name gz-station2 -d \
  -p 8080:8080 -p 8081:8081 -p 8443:8443 \
  -v ~/viam/config/station2-viam.json:/etc/viam.json \
  --entrypoint /entrypoint_station2.sh \
  gz-harmonic-viam
```

{{% /tab %}}
{{% tab name="Windows (PowerShell)" %}}

Create the config file (replace the placeholder values):

```powershell
@"
{
  "cloud": {
    "id": "YOUR_MACHINE_ID",
    "secret": "YOUR_MACHINE_SECRET",
    "app_address": "https://app.viam.com:443"
  }
}
"@ | Out-File -FilePath "$env:USERPROFILE\viam\config\station2-viam.json" -Encoding UTF8
```

Stop and restart the container with the config mounted:

```powershell
docker stop gz-station2; docker rm gz-station2

docker run --name gz-station2 -d `
  -p 8080:8080 -p 8081:8081 -p 8443:8443 `
  -v "$env:USERPROFILE\viam\config\station2-viam.json:/etc/viam.json" `
  --entrypoint /entrypoint_station2.sh `
  gz-harmonic-viam
```

{{% /tab %}}
{{< /tabs >}}

Wait for the machine to come online in the Viam app (check the **Setup** tab—the status indicator turns green when connected).

## 5.7 Apply the Fragment

Now apply your fragment to Station 2 with the correct camera ID:

1. On `inspection-station-2`, go to the **Configure** tab
2. Click **+** and select **Insert fragment**
3. Search for and select `inspection-station`
4. Click **Add**

The fragment appears in your configuration. Notice the **Variables** section—this is where you provide machine-specific values.

**Set the camera ID for Station 2:**

In the fragment's **Variables** section, enter:

```json
{
  "camera_id": "/station_2_camera"
}
```

Click **Save**.

[SCREENSHOT: Fragment with camera_id variable configured]

Within seconds, the machine reloads its configuration. It now has the camera (pointing to Station 2's ID), vision service, inspector module, data capture, and alerting—all from the fragment, customized for this specific station.

## 5.8 Verify It Works

1. Go to the **Control** tab
2. Find the `inspection-cam` camera panel
3. Verify you see the Station 2 camera feed (top-down view of cans on the conveyor with yellow rails visible in the overview)
4. Click **Run detection** on the vision service to verify defect detection works

[SCREENSHOT: Station 2 control tab showing camera feed and detection]

You now have two machines using the same fragment with different camera IDs. If you were to restart Station 1 and apply the fragment with `"camera_id": "/inspection_camera"`, both stations would run identical inspection logic.

## 5.9 Fleet Management Capabilities

With fragments in place, you have the foundation for managing fleets at any scale. Here's what's possible:

**Push updates across your fleet:**

- **Configuration changes**—Edit the fragment, and all machines using it receive the update automatically within seconds
- **ML model updates**—Change which model the vision service uses; all machines switch to the new version
- **Module updates**—Deploy new versions of your inspection logic across the fleet
- **Capture settings**—Adjust data capture frequency, enable/disable components fleet-wide

**Monitor and maintain remotely:**

- **Fleet dashboard**—View all machines' status, last seen, and health from one screen
- **Aggregated data**—Query inspection results across all stations ("How many FAILs across all machines this week?")
- **Remote diagnostics**—View live camera feeds, check logs, and test components without physical access
- **Alerts**—Get notified when any machine goes offline or exhibits anomalies

**Handle machine-specific variations:**

- **Fragment variables**—Parameterize camera IDs, device paths, IP addresses—anything that differs between physical machines
- **Per-machine overrides**—Add machine-specific configuration on top of fragments when needed
- **Hardware flexibility**—Same inspection logic works whether a station uses USB cameras, CSI cameras, or IP cameras

This same pattern scales from 2 machines to 2,000. The fragment is your single source of truth; Viam handles the distribution.

**Checkpoint:** You've created a fragment from your working configuration, parameterized the camera ID, and deployed it to a second station. This is the same pattern used to manage fleets of hundreds or thousands of machines.

**[Continue to Part 6: Productize →](../part-6/)**
