---
linkTitle: "Quickstarts"
title: "Quickstart tutorials"
weight: 5
layout: "docs"
type: "docs"
description: "Short end-to-end tutorials that take a first-time user from zero to a working motion example. Each tutorial uses fake components so it runs without specific hardware."
---

These tutorials take a first-time user from zero to a working arm or
frame-system example. Each one uses fake components so you can run it
on any machine that has `viam-server` installed; swapping in real
hardware later is a configuration change, not a code change.

{{< cards >}}
{{% card link="/motion-planning/quickstarts/first-arm/" noimage="true" %}}
{{% card link="/motion-planning/quickstarts/frame-system/" noimage="true" %}}
{{< /cards >}}

For base motion and GPS waypoint navigation, fake components cannot
localize or drive, so a first-time walkthrough needs real hardware.
The corresponding how-tos cover those flows end-to-end:

{{< cards >}}
{{% card link="/motion-planning/motion-how-to/drive-a-base/" noimage="true" %}}
{{% card link="/navigation/how-to/navigate-to-waypoint/" noimage="true" %}}
{{< /cards >}}
