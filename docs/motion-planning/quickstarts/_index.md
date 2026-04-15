---
linkTitle: "Quickstarts"
title: "Quickstart tutorials"
weight: 5
layout: "docs"
type: "docs"
description: "Short end-to-end tutorials that take a first-time user from zero to a working motion example. Each tutorial uses fake components so it runs without specific hardware."
---

Each quickstart takes you from zero to a working example in about 10 to 15 minutes, using fake components so nothing depends on specific hardware. When you swap in a real arm or camera later, the change is in machine configuration, not in your code.

{{< cards >}}
{{% card link="/motion-planning/quickstarts/first-arm/" noimage="true" %}}
{{% card link="/motion-planning/quickstarts/frame-system/" noimage="true" %}}
{{< /cards >}}

For base motion and GPS waypoint navigation, fake components cannot
localize or drive, so a first-time walkthrough needs real hardware.
The corresponding how-tos cover those flows end-to-end:

{{< cards >}}
{{% card link="/navigation/how-to/drive-a-base/" noimage="true" %}}
{{% card link="/navigation/how-to/navigate-to-waypoint/" noimage="true" %}}
{{< /cards >}}
