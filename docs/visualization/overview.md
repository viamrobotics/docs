---
linkTitle: "Overview"
title: "Visualization"
weight: 1
layout: "docs"
type: "docs"
description: "Ways to visualize a Viam machine: the 3D scene, the standalone Viam visualizer, custom apps you build, and time-series dashboards."
---

A machine produces two kinds of data you can watch: spatial state (frames, geometries,
collisions, point clouds, motion plans) and time series readings (temperatures, speeds,
counts). For spatial state, use the 3D scene view in
the Viam app, or Viam Visualization, a standalone visualizer you run yourself. You can also
read this data from components with a Viam SDK and present it in a custom user interface you
build, which runs in a browser, on a phone, or on a server. For time series data, services
and modules push readings to the cloud, where the Viam app's Teleop workspaces and dashboards
show live information across a machine or fleet.

## The 3D scene

The **3D SCENE** tab on your machine's page renders an interactive 3D view of your
machine: component frames from the frame system, configured geometries, depth-camera
point clouds, and custom visuals a module publishes at runtime.

- Use it while configuring or debugging a machine, to see frames, geometry, and live poses
  with no code.
- Best for catching frame and obstacle misconfigurations and inspecting a motion plan in
  context. It runs right in the Viam app, ready to use.

{{< cards >}}
{{% card link="/visualization/visuals-and-collisions/" noimage="true" %}}
{{% card link="/visualization/publish-visuals-from-a-module/" noimage="true" %}}
{{% card link="/motion-planning/visualize-a-motion-plan/" noimage="true" %}}
{{% card link="/visualization/troubleshoot-the-3d-scene/" noimage="true" %}}
{{< /cards >}}

## Viam Visualization

Viam Visualization is a standalone 3D visualizer you run yourself to preview and debug
spatial data from a Go client. It shares the same `draw` library as the in-app 3D scene, so
the visuals you build work either way.

- Use it while developing, to preview spatial data such as a point cloud, detections, or a
  planned path straight from a script or test.
- Best when you want to iterate from Go quickly, without deploying a module or opening the
  Viam app.

{{< cards >}}
{{% card link="/visualization/viam-visualization/" noimage="true" %}}
{{< /cards >}}

## Custom apps

A custom app uses a Viam SDK to read your machine's data and present it however you design.
It runs outside the machine, in a browser, on a phone, or on a server, so you can build a
custom dashboard, an operator console, or a fleet view. A Svelte app can also
[embed the 3D scene's own renderer](https://viamrobotics.github.io/visualization/guides/embedding/)
as a component, so a custom UI gets the full 3D view alongside your own controls.

- Use it when operators or stakeholders need a tailored UI beyond the built-in scene.
- Best when you want to choose exactly which data to show and how, for one machine or a
  whole fleet.

{{< cards >}}
{{% card link="/build-apps/overview/" noimage="true" %}}
{{% card link="/build-apps/app-tutorials/tutorial-dashboard/" noimage="true" %}}
{{% card link="/build-apps/app-tutorials/tutorial-fleet/" noimage="true" %}}
{{% card link="/build-apps/app-tutorials/tutorial-flutter-app/" noimage="true" %}}
{{% card link="/build-apps/app-tutorials/tutorial-monitoring-service/" noimage="true" %}}
{{< /cards >}}

## Time series data

Services and modules push readings to the cloud, where you watch them live with Viam's
Teleop workspaces and dashboards.

- Use it for values that change over time: temperatures, speeds, counts, and sensor
  readings.
- Best for live monitoring and historical trends across a single machine or a whole fleet.

{{< cards >}}
{{% card link="/monitor/teleop-workspaces/" noimage="true" %}}
{{% card link="/monitor/dashboards/overview/" noimage="true" %}}
{{< /cards >}}
