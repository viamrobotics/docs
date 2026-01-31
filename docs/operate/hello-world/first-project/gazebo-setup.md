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

## Prerequisites

- **Docker Desktop** installed and running
- A free [Viam account](https://app.viam.com)
- ~5GB disk space for the Docker image

## Step 1: Build the Docker Image

The simulation runs in a Docker container with Gazebo Harmonic and viam-server pre-installed.

**Clone the simulation repository:**

```bash
git clone https://github.com/viamrobotics/can-inspection-simulation.git
cd can-inspection-simulation
```

**Build the Docker image:**

```bash
docker build -t gz-harmonic-viam .
```

This takes 5-10 minutes depending on your internet connection.

## Step 2: Create a Machine in Viam

1. Go to [app.viam.com](https://app.viam.com) and log in
2. Click the **Locations** tab
3. Click **+ Add machine**
4. Name it `inspection-station-1`
5. Click **Add machine**

## Step 3: Create a credentials file

1. Click the **Awaiting setup** button
2. Click **Machine cloud credentials** to copy your machine's credentials
3. In the `can-inspection-simulation` directory, create a file called `station1-viam.json`
4. Paste your machine's credentials into this file and save

## Step 4: Start the Container

{{< tabs >}}
{{% tab name="Mac/Linux" %}}

```bash
docker run --name gz-station1 -d \
  -p 8080:8080 -p 8081:8081 -p 8443:8443 \
  -v "$(pwd)/station1-viam.json:/etc/viam.json" \
  gz-harmonic-viam
```

{{% /tab %}}
{{% tab name="Windows (PowerShell)" %}}

```powershell
docker run --name gz-station1 -d `
  -p 8080:8080 -p 8081:8081 -p 8443:8443 `
  -v "${PWD}\station1-viam.json:/etc/viam.json" `
  gz-harmonic-viam
```

{{% /tab %}}
{{< /tabs >}}

## Step 5: Verify the Setup

**Check container logs:**

```bash
docker logs gz-station1
```

Look for:

- "Can Inspection Station 1 Running!"
- viam-server startup messages

**View the simulation:**

Open your browser to `http://localhost:8081`

You should see a web-based 3D view of the inspection station with:

- A conveyor belt
- Cans moving along the belt
- An overhead camera view

[SCREENSHOT: Gazebo web viewer showing the simulation]

**Verify machine connection:**

1. Go to [app.viam.com](https://app.viam.com)
2. Click on `inspection-station-1`
3. The status indicator should show **Live** (in green)

## Troubleshooting

{{< expand "Container won't start" >}}
**Check if ports are in use:**

{{< tabs >}}
{{% tab name="Mac/Linux" %}}

```bash
lsof -i :8080
lsof -i :8081
```

{{% /tab %}}
{{% tab name="Windows (PowerShell)" %}}

```powershell
netstat -ano | findstr :8080
netstat -ano | findstr :8081
```

{{% /tab %}}
{{< /tabs >}}

If something is using these ports, stop it or use different port mappings.
{{< /expand >}}

{{< expand "Machine shows Offline in Viam" >}}

1. Check container is running: `docker ps`
2. Check logs for errors: `docker logs gz-station1`
3. Verify credentials in your config file match the Viam app
4. Try restarting: `docker restart gz-station1`
   {{< /expand >}}

{{< expand "Simulation viewer is blank or slow" >}}

- The web viewer requires WebGL support
- Try a different browser (Chrome usually works best)
- Check your system has adequate resources (4GB+ RAM recommended)
  {{< /expand >}}

## Container Management

**Stop the container:**

```bash
docker stop gz-station1
```

**Start a stopped container:**

```bash
docker start gz-station1
```

**Remove the container (to recreate):**

```bash
docker rm gz-station1
```

**View logs:**

```bash
docker logs -f gz-station1
```

## Ready to Continue

Once your machine shows **Live** in the Viam app, you're ready to continue with the tutorial.

**[Continue to Part 1: Vision Pipeline →](../part-1/)**
