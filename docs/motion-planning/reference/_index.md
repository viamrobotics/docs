---
linkTitle: "Reference"
title: "Motion planning reference"
weight: 200
layout: "docs"
type: "docs"
description: "Configuration, API, and technical reference for the motion service."
---

The motion service turns a high-level "move to this pose" request into a
collision-free joint trajectory. This reference documents what you
configure, what the API exposes, and the formats and algorithms it uses
under the hood. For conceptual background, see
[How motion planning works](/motion-planning/how-planning-works/); for
task-based guidance, start from the [section landing](/motion-planning/).

**Configuration and API**: where most readers start.

{{< cards >}}
{{% card link="/motion-planning/reference/motion-service/" noimage="true" %}}
{{% card link="/motion-planning/reference/motion-configuration/" noimage="true" %}}
{{% card link="/motion-planning/reference/api/" noimage="true" %}}
{{% card link="/motion-planning/reference/cli-commands/" noimage="true" %}}
{{% card link="/motion-planning/reference/plan-monitoring/" noimage="true" %}}
{{< /cards >}}

**Formats and machinery**: the underlying schemas the service operates on.

{{< cards >}}
{{% card link="/motion-planning/reference/frame-system-api/" noimage="true" %}}
{{% card link="/motion-planning/reference/kinematics/" noimage="true" %}}
{{% card link="/motion-planning/reference/orientation-vectors/" noimage="true" %}}
{{% card link="/motion-planning/reference/algorithms/" noimage="true" %}}
{{< /cards >}}
