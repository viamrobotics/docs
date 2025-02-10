---
linkTitle: "Build & integrate"
title: "Build and integrate"
weight: 150
layout: "docs"
type: "docs"
no_list: true
open_on_desktop: true
overview: true
description: "To get started, install Viam on any device and integrate your hardware. Then you can control your device and any attached physical hardware securely from anywhere in the world."
aliases:
  - /build/
---

To get started, install Viam on any device and integrate your hardware. Then you can control your device and any attached physical hardware securely from anywhere in the world.

<!-- Need to use upside down logic because using Subsequent-sibling combinator -->
<div class="upside-down">

{{< how-to-expand "Intelligent actuation and motion planning" "5" "INTERMEDIATE" "" "hoverable-motion" >}}
{{< cards >}}
{{% card link="/operate/mobility/define-geometry/" noimage="true" %}}
{{% card link="/operate/mobility/define-obstacles/" noimage="true" %}}

{{% card link="/operate/mobility/move-base/" noimage="true" %}}
{{% card link="/operate/mobility/move-arm/" noimage="true" %}}
{{% card link="/operate/mobility/move-gantry/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Build apps" "3" "BEGINNER-FRIENDLY" "" "hoverable-apps" >}}
{{< cards >}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{% card link="/operate/control/mobile-app/" noimage="true" %}}
{{% card link="/operate/control/headless-app/" noimage="true" %}}

{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Connect devices" "3" "BEGINNER-FRIENDLY" "" "hoverable-connect" >}}
{{< cards >}}
{{% card link="/operate/get-started/setup/" noimage="true" %}}
{{% card link="/operate/get-started/supported-hardware/" noimage="true" %}}
{{% card link="/operate/get-started/other-hardware/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

<div class="img-overlay-wrap aligncenter">
  <img src="../platform/platform-all.svg" alt="Platform diagram" id="fleet-platform-all" class="aligncenter overview" style="width:800px" >
  <img src="../platform/platform-build-connect.svg" alt="Platform diagram with connect elements highlighted" class="aligncenter overlay" id="build-platform-connect" style="width:800px" loading="lazy" >
  <img src="../platform/platform-build-apps.svg" alt="Platform diagram with apps element highlighted" class="aligncenter overlay" id="build-platform-apps" style="width:800px" loading="lazy" >
  <img src="../platform/platform-build-motion.svg" alt="Platform diagram with motion elements highlighted" class="aligncenter overlay" id="build-platform-motion" style="width:800px" loading="lazy" >
</div>

</div>
