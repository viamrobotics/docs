---
title: "Phase 1: Platform mental model"
linkTitle: "1. Platform mental model"
type: "docs"
slug: "platform-mental-model"
weight: 10
description: "Understand how the Viam cloud, agent, and server fit together, and configure your first resource, the arm."
workshop: "pick-and-place"
toc_hide: true
phase: 1
phase_total: 6
time_estimate: "20 minutes"
next: "/tutorials/pick-and-place/configure-resources/"
languages: ["python"]
---

This phase gives you the mental map you need before the rest of the workshop: what happens when you make an API call, why config changes appear instantly on the robot, and how Python code on your laptop talks to hardware across the room. You configure your first resource, the arm, as you go.

## Three questions to consider

By the end of this phase you should be able to answer these three questions. Keep them in mind as you read, and check yourself against them again at the end.

1. What are the three layers of a Viam machine, and which one does your Python code actually talk to?
2. What is the difference between a component and a service?
3. Why does adding the arm trigger a module download?

You will not write any code in this phase, but you will configure your first resource, the arm, so the concepts below have something real to point at. Open your own machine in the Viam app and follow along.

## The three layers

<!-- ASSET P0 diagram-three-layers (DIAGRAM): cloud app (source of truth) -> viam-server pulls config; viam-agent supervises; SDK arrow to viam-server. See plans/2026-07-02-pick-and-place-shot-list.md -->

A Viam machine is made of three layers that each do one job:

- **The Viam cloud app** is the source of truth for configuration. When you add a component, change an attribute, or wire up a service, you are editing a JSON document stored in the cloud. The app never controls your robot directly; it describes what should run.
- **viam-agent** is a service that runs on the computer controlling the arm. viam-agent manages `viam-server`: it installs, updates, and keeps `viam-server` running, restarts the server if it crashes, and provides the initial bootstrap credentials viam-server needs to reach the cloud. Think of viam-agent as the process supervisor, not as the source of your resource config, and not as something you interact with directly during this workshop.
- **viam-server** pulls the machine resource configuration from the cloud app, starts every component and service that configuration describes, and exposes the components and services over an API. This is the layer that handles the modules that drive the arm, reads the camera, and runs the vision pipeline.

Open your machine's overview page in the Viam app now and find the status indicator that shows the machine is live. That indicator reflects viam-agent keeping viam-server running and connected to the cloud app, the handoff between all three layers happening continuously in the background.

## How your SDK connects

When a Python script imports the Viam SDK and connects to your machine, the connection goes to `viam-server`, not to the cloud app. The cloud app helps your script locate the machine and authenticate, but once the connection is established, every control API call goes directly to `viam-server` on the robot: moving the arm, reading the camera, calling the vision service. You will write exactly this kind of script later in the workshop.

This matters because it explains why your script keeps working even if your laptop briefly loses its connection to the internet at large but keeps a path to the robot: the cloud app is not in the request path for control, only for discovery and configuration delivery.

Open the **CONNECT** tab on your machine's page in the Viam app and look at the code sample it generates. The address and API key shown there are exactly what your Phase 4 script will use to reach `viam-server`.

## Configuration is the source of truth

Whatever you set in the app's **CONFIGURE** tab is what the machine runs. There is no separate step to "deploy" a change: when you save an edit, the cloud app updates the config document, and `viam-server` picks up the new config and applies it, typically within seconds, without a restart for most changes.

This is why the workshop asks you to make changes in the app rather than by editing a file on the robot directly. The app's CONFIGURE tab is the only place you need to look to know what a machine will do.

Open the **CONFIGURE** tab now and find the JSON view toggle near the top of the panel. Switching to JSON shows you the exact document that `viam-server` receives. Your machine has no resources configured yet, so the document is nearly empty; it fills in as you add resources, starting in the next section.

## Resources: configure your first one

Everything a Viam machine does, hardware and software alike, is modeled as a **resource**. Each resource has a name you choose (like `arm-1`), an API that describes what kind of thing it is (an arm, a camera, a vision service), and a model that identifies the specific implementation. The fastest way to understand a resource is to configure one, so add the arm now.

On the **CONFIGURE** tab, click the **+** icon and select **Blocks**. Search for `xArm6`, select the `viam:ufactory:xArm6` result, and name the component `arm-1`.

<!-- ASSET P0 configure-add-component (UI+): add-component dialog, "xArm6" searched, viam:ufactory:xArm6 result highlighted. See plans/2026-07-02-pick-and-place-shot-list.md -->

{{<imgproc src="/tutorials/pick-and-place/configure-add-component.png" resize="1200x" declaredimensions=true alt="The add-component dialog with xArm6 searched and the ufactory/xArm6 result selected.">}}

Set the following attributes:

```json
{
  "host": "",
  "speed_degs_per_sec": 30
}
```

`host` is the only required attribute; it can be found on the arm's control box. Setting `speed_degs_per_sec` to `30` keeps the arm moving slowly enough to stay safe while you work near it.

<!-- ASSET P2 arm-controller-host (PHOTO): the xArm controller box with its IP address label -->

{{<imgproc src="/tutorials/pick-and-place/arm-controller-host.jpeg" resize="1200x" declaredimensions=true alt="The xArm controller box; the IP address to use for the host attribute is printed on a label.">}}

Save the config, then open the **LOGS** tab and watch what happens: a log line for a module download, then one for the module starting, then `arm-1` coming online, usually well under a minute. You just set the module system in motion; the [Builtin resources and modules](#builtin-resources-and-modules) section below explains what you saw.

<!-- ASSET P0 logs-xarm-module-start (UI+): LOGS showing the viam:ufactory module download + start (the module-download moment) -->

{{<imgproc src="/tutorials/pick-and-place/logs-xarm-module-start.png" resize="1200x" declaredimensions=true alt="The LOGS tab showing the viam:ufactory module downloading and starting.">}}

Back on the **CONFIGURE** tab, look at the `arm-1` card. Next to the name, it shows the model as `ufactory/xArm6`, the family and model name, with `from ufactory` marking the module it came from. That is the short form. The model's full name is a **triplet**, `namespace:family:name`, which you can see written out as `viam:ufactory:xArm6` if you switch to the JSON view. The triplet tells `viam-server` exactly which code to run for this resource: who published it (`namespace`, here `viam`), the family of models it belongs to (`family`, here `ufactory`), and the specific model name (`name`, here `xArm6`).

<!-- ASSET P1 configure-arm1-triplet (UI+): arm-1 card showing the ufactory/xArm6 model label and "from ufactory", plus the full viam:ufactory:xArm6 triplet in the JSON model field -->

{{<imgproc src="/tutorials/pick-and-place/configure-arm1-triplet.png" resize="1200x" declaredimensions=true alt="The arm-1 resource card showing its ufactory/xArm6 model and from ufactory module label.">}}

You will configure the gripper and camera the same way in Phase 2. Each is a resource too, with its own name, API, and model, even though one drives a gripper and the other reads a depth camera.

## Components and services

Resources split into two kinds:

- **Components** represent physical hardware. `arm-1` is a component, and so are the `gripper-1` and `cam-1` you add in Phase 2: each one wraps a piece of hardware and exposes a standard API for it (an arm API with move commands, a camera API that returns images, and so on).
- **Services** represent software tasks or capabilities. A motion service plans collision-free paths for an arm. Later, in Phase 5, you configure a `shape-detector` vision service that reads frames from `cam-1` and finds blocks by shape, and a `vision-segment` service (model `detections-to-segments`) that takes those detections and turns them into point cloud segments the motion planner can grasp. Neither service is a physical thing; each one composes other resources into a new capability.

Open the **CONTROL** tab. Because `arm-1` is the only resource you have configured so far, you see a single card, for the arm; it lets you interact with the hardware directly. In Phase 2, adding the gripper and camera gives each its own card, and any service you add later gets a card that exercises a capability built on top of that hardware.

## Builtin resources and modules

Some resources are **builtin**: `viam-server` (also called the RDK, the robot development kit) ships with support for common APIs and a handful of default models out of the box. Most of the interesting functionality on a real machine, though, comes from **modules**: packages that `viam-server` downloads and runs to add support for a specific model.

The `viam:ufactory:xArm6` arm you just added is module-provided. That is what the LOGS activity was when you saved it: `viam-server` recognized it does not have `viam:ufactory:xArm6` built in, so it downloaded the module that provides it from the Viam registry and started it. Every other module-provided resource you add follows the same pattern.

You can read this straight off the namespace. `arm-1`'s namespace is `viam`, a third-party namespace, which is why it arrived as a module. A namespace of `rdk` would mean the model ships inside `viam-server` itself and needs no download; any other namespace, like `viam` or `erh`, means the model comes from a module.

## The resource dependency graph

<!-- ASSET P0 diagram-dependency-graph (DIAGRAM): cam-1 -> shape-detector -> vision-segment; arm-1 -> gripper-1 + five pose switches; motion service -->

Resources can depend on each other. A gripper attaches to an arm, so `gripper-1`'s config points at `arm-1`. A vision service reads from a camera, so it depends on `cam-1`. `viam-server` reads these dependencies out of your config and builds a dependency graph, then starts resources in an order that respects it: a resource cannot start until everything it depends on has started.

This is the same pattern you will see again in Phase 5: `vision-segment` depends on `shape-detector`, which depends on `cam-1`. Neither can produce meaningful output until the resource beneath it is running.

Open the **LOGS** tab and look at the startup sequence the next time the machine restarts (you do not need to trigger one now). The order resources come online in the log follows the dependency graph, not the order they appear in the config file.

{{< alert title="Check yourself" color="note" >}}
Before moving to Phase 2, make sure you can answer the three questions from the top of this page: name the three layers and which one your code talks to, what separates a component from a service, and why adding the arm triggers a module download. If any answer feels shaky, re-skim the relevant section above.
{{< /alert >}}

{{< workshop-nav >}}
