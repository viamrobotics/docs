---
linkTitle: "Overview"
title: "Visualization"
weight: 1
layout: "docs"
type: "docs"
description: "Ways to visualize a Viam machine: the 3D scene, the standalone Viam Visualization app, component data in apps, and time-series dashboards."
---

There are several approaches to visualizing information in Viam. For things like motion,
visualizing frames, checking the robot state, reviewing collisions, and viewing live perception
data, you can use the 3D scene view or an offline visualizer called Viam Visualization. This
data can be retrieved from components and used in Viam apps or custom user applications.
For time series data, services and modules can push data to the cloud to be visualized with
Viam's Teleop workspaces and dashboards to get live information across a machine or fleet.

## The 3D scene

The **3D SCENE** tab on your machine's page renders an interactive 3D view of your
machine: component frames from the frame system, configured geometries, depth-camera
point clouds, and custom visuals a module publishes at runtime. Use it to check spatial
configuration and watch live data in context.

{{< cards >}}
{{% card link="/visualization/visuals-and-collisions/" noimage="true" %}}
{{% card link="/visualization/publish-visuals-from-a-module/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/debug-motion-plan/" noimage="true" %}}
{{< /cards >}}

## Viam Visualization

Viam Visualization is a standalone 3D app you run yourself to preview and debug spatial
data from a Go client, without deploying a module or opening the Viam app. It shares the
same `draw` library as the in-app 3D scene, so the visuals you build work either way.

{{< cards >}}
{{% card link="/visualization/drawing-library/" noimage="true" %}}
{{< /cards >}}

## Component data in your applications

Components report spatial data, geometries and poses, through their APIs. Read it with an
SDK and render or process it yourself in a Viam app or a custom application.

{{< cards >}}
{{% card link="/build-apps/" noimage="true" %}}
{{< /cards >}}

## Time series data

Services and modules push readings to the cloud, where you watch them live with Viam's
Teleop workspaces and dashboards across a single machine or a whole fleet.

{{< cards >}}
{{% card link="/monitor/teleop-workspaces/" noimage="true" %}}
{{% card link="/monitor/dashboards/overview/" noimage="true" %}}
{{< /cards >}}
