---
title: "Phase 6: Inline module"
linkTitle: "6. Inline module"
type: "docs"
slug: "inline-module"
weight: 60
description: "Optional: package your working script as an inline module that runs on the robot."
workshop: "pick-and-place"
toc_hide: true
phase: 6
phase_total: 6
time_estimate: "20 minutes"
prev: "/tutorials/pick-and-place/perception-guided-picking/"
languages: ["python"]
---

This phase is optional: if you want the pick-and-sort cycle to run on the robot without a laptop connection, you can package your Phase 5 script as an inline module using the Viam app's built-in editor.

{{< workshop-phases >}}

## Script versus module

<!-- TODO: contrast a standalone script (requires a laptop) with a module (runs as a managed service on the robot) from slides Phase 5. -->

## The inline module editor

<!-- TODO: show how to open the inline module editor in the Viam app and paste in the script skeleton from slides Phase 5 / plan page 05. -->

## Dependency injection

<!-- TODO: explain how the module framework injects component dependencies via the constructor from slides Phase 5 / plan page 05. -->
<!-- TODO: access transform_pose inside the module via a FrameSystemClient injected dependency, NOT a second RobotClient connection. -->

## do_command and a scheduled job

<!-- TODO: describe the do_command handler pattern and how to wire it to a recurring scheduled job from slides Phase 5. -->

{{< workshop-nav >}}
