---
linkTitle: "Simulation Setup"
title: "Simulation Setup"
weight: 100
layout: "docs"
type: "docs"
description: "Set up the hosted simulation environment for the inspection tutorial."
date: "2025-01-30"
---

This guide walks you through setting up the Gazebo simulation used in the [Your First Project](../) tutorial.

If you run into trouble getting this working, reach out on discord or at **TODO**@viam.com.

## Step 1: Start a Simulation Environment

Visit [cans.viam-labs.com](https://cans.viam-labs.com), and follow the prompts to log in. Wait for your instance to start.

## Step 2: Verify the Simulation

When your instance is finished starting, you should see two live camera feeds from the inspection station:

{{<imgproc src="/tutorials/first-project/sim-viewer.png" resize="x1100" declaredimensions=true alt="Simulation web viewer showing the Can Inspection Station with Overview Camera and Inspection Camera feeds." class="imgzoom shadow">}}

## Step 3: Create a Machine in Viam

1. Go to [app.viam.com](https://app.viam.com) and create a free account or log in
2. Click the **Locations** tab
3. Click **+ Add machine**, name it `inspection-station-1`, and click **Add machine**

   {{<imgproc src="/tutorials/first-project/fleet-add-machine.png" resize="x1100" declaredimensions=true alt="Viam app Fleet page showing First Location with no machines and the Add machine button." class="imgzoom shadow">}}

## Step 4: Configure Machine Credentials

1. In the Viam app, click the **Awaiting setup** button on your new machine and click **Machine cloud credentials** to copy the credentials JSON

   {{<imgproc src="/tutorials/first-project/awaiting-setup.png" resize="x1100" declaredimensions=true alt="Viam app showing the Awaiting setup dropdown with Machine cloud credentials option." class="imgzoom shadow">}}

2. In the simulation viewer, click the **Configuration** button in the upper right corner

   {{<imgproc src="/tutorials/first-project/sim-viewer-config-button.png" resize="x1100" declaredimensions=true alt="Simulation viewer showing the Configuration button in the upper right corner." class="imgzoom shadow">}}

3. Paste your machine's credentials into the **Viam Configuration (viam.json)** text area and click **Update and Restart**

   {{<imgproc src="/tutorials/first-project/sim-config-page.png" resize="x1100" declaredimensions=true alt="Simulation configuration page with machine cloud credentials pasted into the text area. Viam Server Status shows Stopped." class="imgzoom shadow">}}

   A green banner will confirm the configuration was updated successfully and the status indicator will change to **Running**.

   {{<imgproc src="/tutorials/first-project/sim-config-running.png" resize="x1100" declaredimensions=true alt="Simulation configuration page after restart, showing a green 'Configuration updated successfully' banner and Viam Server Status: Running." class="imgzoom shadow">}}

## Step 5: Verify Machine Connection

Go back to your machine's page in the Viam app.
The status indicator should now show **Live**.

{{<imgproc src="/tutorials/first-project/viam-app-live.png" resize="x1100" declaredimensions=true alt="Viam app showing inspection-station-1 with a green Live status indicator." class="imgzoom shadow">}}

## Ready to Continue

Once your machine shows **Live** in the Viam app, you're ready to continue with the tutorial.

**[Continue to Part 1: Vision Pipeline →](../part-1/)**
