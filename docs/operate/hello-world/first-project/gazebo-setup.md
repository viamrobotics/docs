---
linkTitle: "Gazebo Simulation Setup"
title: "Gazebo Simulation Setup"
weight: 100
layout: "docs"
type: "docs"
description: "Set up the Gazebo simulation environment for the inspection tutorial."
date: "2025-01-30"
---

This guide walks you through setting up the Gazebo simulation used in the [Your First Project](../) tutorial.

**Time:** ~2 min

## Prerequisites

- **Docker Desktop** installed and running
- ~5GB disk space for the Docker image

## Step 1: Pull the Docker Image

The simulation runs in a Docker container with Gazebo Harmonic and viam-server pre-installed.

```bash
docker pull ghcr.io/viamrobotics/can-inspection-simulation:latest-local
```

This downloads the pre-built image, which takes about a minute depending on your internet connection.

## Step 2: Start the Container

```bash
docker run --name gz-station1 -d \
  -p 8080:8080 -p 8081:8081 -p 8443:8443 \
  ghcr.io/viamrobotics/can-inspection-simulation:latest-local
```

## Step 3: Verify the Simulation

Open your browser to `http://localhost:8081`

You should see two live camera feeds from the inspection station:

{{<imgproc src="/tutorials/first-project/sim-viewer.png" resize="x1100" declaredimensions=true alt="Simulation web viewer showing the Can Inspection Station with Overview Camera and Inspection Camera feeds." class="imgzoom shadow">}}

## Step 4: Create a Machine in Viam

1. Go to [app.viam.com](https://app.viam.com) and create a free account or log in
2. Click the **Locations** tab
3. Click **+ Add machine**, name it `inspection-station-1`, and click **Add machine**

   {{<imgproc src="/tutorials/first-project/fleet-add-machine.png" resize="x1100" declaredimensions=true alt="Viam app Fleet page showing First Location with no machines and the Add machine button." class="imgzoom shadow">}}

## Step 5: Configure Machine Credentials

1. In the Viam app, click the **Awaiting setup** button on your new machine and click **Machine cloud credentials** to copy the credentials JSON

   {{<imgproc src="/tutorials/first-project/awaiting-setup.png" resize="x1100" declaredimensions=true alt="Viam app showing the Awaiting setup dropdown with Machine cloud credentials option." class="imgzoom shadow">}}

2. In the simulation viewer, click the **Configuration** button in the upper right corner

   {{<imgproc src="/tutorials/first-project/sim-viewer-config-button.png" resize="x1100" declaredimensions=true alt="Simulation viewer showing the Configuration button in the upper right corner." class="imgzoom shadow">}}

3. Paste your machine's credentials into the **Viam Configuration (viam.json)** text area and click **Update and Restart**

   {{<imgproc src="/tutorials/first-project/sim-config-page.png" resize="x1100" declaredimensions=true alt="Simulation configuration page with machine cloud credentials pasted into the text area. Viam Server Status shows Stopped." class="imgzoom shadow">}}

   A green banner will confirm the configuration was updated successfully and the status indicator will change to **Running**.

   {{<imgproc src="/tutorials/first-project/sim-config-running.png" resize="x1100" declaredimensions=true alt="Simulation configuration page after restart, showing a green 'Configuration updated successfully' banner and Viam Server Status: Running." class="imgzoom shadow">}}

## Step 6: Verify Machine Connection

Go back to your machine's page in the Viam app.
The status indicator should now show **Live**.

{{<imgproc src="/tutorials/first-project/viam-app-live.png" resize="x1100" declaredimensions=true alt="Viam app showing inspection-station-1 with a green Live status indicator." class="imgzoom shadow">}}

## Ready to Continue

Once your machine shows **Live** in the Viam app, you're ready to continue with the tutorial.

**[Continue to Part 1: Vision Pipeline →](../part-1/)**
