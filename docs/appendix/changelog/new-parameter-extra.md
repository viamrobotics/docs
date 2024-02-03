---
title: New parameter `extra`
date: "2022-11-01"
color: "added"
---

A new API method parameter, `extra`, allows you to extend {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} functionality by implementing the new field according to whatever logic you choose.
`extra` has been added to the following APIs: arm, data management, gripper, input controller, motion, movement sensor, navigation, pose tracker, sensor, SLAM, vision.

{{% alert title="IMPORTANT: Breaking change" color="note" %}}

Users of the Go SDK _must_ update code to specify `extra` in the arguments that pass into each request.

`extra` is an optional parameter in the Python SDK.

{{% /alert %}}
