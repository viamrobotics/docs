---
linkTitle: "What is Viam?"
title: "What is Viam?"
weight: 10
layout: "docs"
type: "docs"
images: ["/general/understand.png"]
imageAlt: "Viam platform overview"
no_list: false
description: "Viam is a software platform for building, deploying, and managing robotics applications."
aliases:
  - /operate/modules/basics/
  - /operate/hello-world/quickstart/
date: "2025-01-30"
---

Viam is a software platform for building, deploying, and managing robotics applications.

With Viam, you declare the hardware and services you need in a JSON config. Viam installs the drivers and any additional software modules required to support your configuration.
Vision, motion planning, and most other capabilities you need are built in or available in the Viam module Registry, all with well-defined APIs to support your use case.
Application code versioning, deployment, and rollback are native to the Viam platform.
It's the development workflow you're used to, applied to physical devices.

Viam brings software engineering practices to robotics: version control, remote monitoring and diagnostics, staged rollouts, and a registry of modules and models you can build on.

## Viam fundamentals

Every Viam machine starts with `viam-server`, Viam's service and package manager. 
Install `viam-server` with a single command.
Then declare what hardware is connected and what services you need in a JSON config.
`viam-server` pulls the necessary drivers from the Viam Registry, launches required processes, and keeps them running to support all the services your application requires.
`viam-server` also manages networking and data sync.

The [Viam Registry](/operate/modules/configure-modules/) is a central repository of modules, ML models, and training scripts maintained by Viam and the robotics community.
All registry assets support semantic versioning, enabling controlled deployment to individual robots and across your fleet.

Registry modules provide drivers for cameras, motors, sensors, arms, and other hardware, plus services like object detection.
`viam-server` also includes built-in services such as motion planning and data management.
For machine learning, the Registry includes pretrained models for common tasks. You can also train and use your own models.

Viam supports reusable configuration through [fragments](/manage/fleet/reuse-configuration/).
Define a combination of components, services, and modules once, then apply that configuration across any number of machines.
Use fragments to configure a camera-arm combination, a camera-to-object-detection pipeline, or an entire work cell.
Fragments support variable substitution and per-machine overwrites, so you can deploy the same base configuration to hundreds of machines while accommodating site-specific settings.

## Viam capabilities

{{< alert title="In this section" color="note" >}}

- [Get hardware running in minutes](#get-hardware-running-in-minutes)
- [Operate from anywhere](#operate-from-anywhere)
- [Capture data from edge to cloud](#capture-data-from-edge-to-cloud)
- [Train and deploy models](#train-and-deploy-models)
- [Develop code remotely](#develop-code-remotely)
- [Manage software deployments](#manage-software-deployments)
- [Scale easily](#scale-easily)
- [Productize with Viam apps](#productize-with-viam-apps)

{{< /alert >}}

### Get hardware running in minutes

Add a camera, motor, arm, or sensor to your JSON config with a few parameters: model, connection type, any device-specific settings.
`viam-server` handles the rest—pulls the driver, initializes the device, and exposes it through a consistent API.
You don't have to write device drivers or worry about dependencies.

- **Consistent APIs across hardware:** All cameras expose the same interface regardless of manufacturer. Same for motors, sensors, arms, and other component types. Your code doesn't change when hardware does.
- **Swap hardware without changing code:** Replace an Intel RealSense with an Orbbec Astra camera, or swap one motor controller for another—update the config and your application keeps working.
- **Drivers for hundreds of devices:** The Registry includes modules for most common hardware. If yours isn't supported, write a module once and reuse it everywhere.

### Operate from anywhere

Connect to your machine from anywhere.
No VPN, no port forwarding, no firewall configuration.
Viam handles NAT traversal automatically.
The web app, SDKs, and CLI all use the same connection infrastructure, so you can debug from your laptop and monitor from the Viam web app.

- **Stream logs remotely:** View machine logs in the web app, filtered by level, keyword, or time range.
- **Run code against remote hardware:** Write scripts on your laptop that connect to a machine over the network. Inspect component state, run diagnostics, or test behavior without deploying code.
- **View live camera and sensor data:** See camera feeds and sensor readings in the web app's TEST panel for each component.
- **Teleoperate from the browser:** Drive a base with keyboard controls, move an arm to specific positions, or reposition a gantry, all from the web UI.
- **Visualize in 3D:** See a live 3D view of your machine showing component positions, camera feeds, and point clouds. Move components and watch the visualization update in real time.

### Capture data from edge to cloud

Configure [data capture](/data-ai/capture-data/) in JSON: which components, how often, what to keep.
Viam handles the pipeline.
Data syncs to the cloud when connectivity allows, survives network interruptions and restarts, and queues locally on devices with constrained bandwidth.
No custom sync logic, no managing local storage, no worrying about edge cases.

- **Capture from any component:** Record images from cameras, readings from sensors, or custom data from your own modules—all with configuration, no code required.
- **Sync automatically:** Data syncs when bandwidth is available. If your machine goes offline, data queues locally and syncs when connectivity returns.
- **Filter at the edge:** Reduce bandwidth and storage costs by filtering before sync. Keep only images with detections, sensor readings outside normal ranges, or samples at specified intervals.
- **Query across your fleet:** Find data by machine, location, time range, component, or tags. Export for analysis or training.
- **Manage storage automatically:** Set retention policies to delete old data. Configure local storage limits for edge devices with constrained disk space.

### Train and deploy models

[Train models](/data-ai/train/) on data you've captured, or bring models trained elsewhere.
Deploy to your fleet with the same versioning and update mechanisms as code.

- **Train in Viam:** Select captured data, annotate, choose a model architecture, and start a training job. No GPU provisioning, no training pipeline setup. Viam handles it.
- **Bring your own model:** Import models trained in TensorFlow, PyTorch, ONNX, or other frameworks. Upload to the Registry and deploy like any other versioned asset.
- **Deploy to your fleet:** Push a model to the Registry and configure machines to pull it. Pin to specific versions or allow automatic updates—same as modules.
- **Run inference on device:** The ML model service runs on the machine. Inference happens locally without round-trips to the cloud.

### Develop code remotely

Traditional robotics development means standing next to the robot or SSH'ing into it.
Viam lets you treat your robot like a machine in the cloud.
Develop and test from your laptop.
Your code connects to your robot machine over the network, through firewalls and NAT, without VPN.

- **Iterate from your IDE:** Write code on your laptop, run it against your robot hardware over the network. No copying files, no deploy step. Just run and see results.
- **Run on the robot machine when latency matters:** For tight control loops, run scripts directly on your robot machine. Same code, same APIs—just a different execution environment.
- **Package as a module for production:** When you're ready, package your code as a module that `viam-server` manages: starts on boot, restarts on failure, reconfigures when settings change.
- **Call built-in services from your code:** Motion planning, computer vision, navigation, and data capture are available as services you call from any SDK.

### Manage software deployments

Package your control logic as a [module](/operate/modules/control-logic/) and deploy through the Viam Registry for version control, remote updates, and fleet-wide rollouts.
No cross-compiling.
Viam handles everything.

- **Managed lifecycle:** `viam-server` manages dependencies and ensures your application code starts on boot and restarts when necessary.
- **Reconfigure on the fly:** Tune the application parameters you define with configuration updates in the Viam app. Changes apply within seconds. No restarts or redeployment.
- **Version control:** Pin machines to exact versions for stability, or allow automatic updates at the patch, minor, or major level.
- **OTA updates:** Push new versions to the registry with the CLI; machines pull updates automatically per their update policies.

### Scale easily

Your prototype configuration becomes your production configuration.
Turn a working machine setup into a [fragment](/manage/fleet/reuse-configuration/) and apply it to several, dozens, or even hundreds of machines.
No deployment scripts, no copying files, no per-machine setup.

- **Create a fragment from your prototype:** Once your machine works, export the configuration as a fragment. That exact setup is now reusable across any number of machines. Viam handles provisioning.
- **Update configurations fleet-wide:** Change a fragment and every machine using it pulls the update. No scripting, no SSH loops.
- **Override per-machine differences:** If some machines have a different camera model or site-specific parameter value, override for just those machines without forking the base fragment.
- **Roll out changes incrementally:** Deploy configuration changes, module versions, or ML models to a subset of machines first. Validate before rolling out fleet-wide.
- **Roll back with one change:** Viam maintains configuration history. Revert to a previous version of a fragment, module, or model with a single update.

### Productize with Viam apps

Building a robotics product means building customer infrastructure—auth systems, dashboards, billing.
Viam provides these so you can focus on your product.

- **White-label authentication:** Customers authenticate through a login screen with your logo and branding, not Viam's.
- **Build customer-facing apps:** Use the TypeScript SDK for web dashboards or the Flutter SDK for iOS and Android apps. Both handle authentication and provide access to all component and service APIs.
- **Built-in billing:** Define pricing tiers—per-machine fees, data costs, or both. Viam handles invoicing and payment collection.

## Next steps

Now you know about the most important concepts for using Viam.

We recommend putting these concepts into practice by following the [Desk Safari tutorial](/operate/hello-world/tutorial-desk-safari/) to build your first machine.

If you'd like to learn more about Viam and how it works, see [Viam architecture](/operate/reference/architecture/).

For more information on cloud capabilities like fleet management and provisioning, see [Monitor Air Quality with a Fleet of Sensors](/tutorials/control/air-quality-fleet/).
