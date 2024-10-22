---
title: "How-to Guides"
linkTitle: "How-to Guides"
weight: 200
type: "docs"
images: ["/registry/module-puzzle-piece.svg"]
#layout: "howto"
description: "Follow instructions for common tasks and workflows."
no_list: true
notoc: true
hide_children: true
sitemap:
  priority: 1.0
aliases:
  - /use-cases/
date: "2024-09-17"
howtojs: true
# updated: ""  # When the content was last entirely checked
---

<div class="max-page">
<p>
The guides on this page provide solutions for common tasks and workflows. Browse the guides on this page or filter by product area:
</p>

<div id="tutorial-menu" class="lozad">
  <div id="resource-list" style="display:none;"></div>
  <div id="platformarea-list" data-parent="#tutorial-menu"></div>
</div>
<div class="search-panel__results guides card-container lozad">
    <div id="hits" class="row-no-margin"></div>
    <div id="pagination"></div>
</div>

<div id="how-to-paths">

{{< how-to-expand title="Get started with Viam basics" tasks="4" level="BEGINNER-FRIENDLY" >}}
{{< cards >}}
{{% card link="/how-tos/drive-rover/" noimage="true" %}}
{{% card link="/how-tos/control-motor/" noimage="true" %}}
{{% card link="/how-tos/detect-people/" noimage="true" %}}
{{% card link="/how-tos/collect-data/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Configure a fleet, starting with one machine" "4" "BEGINNER-FRIENDLY" >}}
{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/one-to-many/" noimage="true" %}}
{{% card link="/how-tos/provision-setup/" noimage="true" %}}
{{% card link="/how-tos/provision/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Work with sensor data" "3" "INTERMEDIATE" >}}
{{< cards >}}
{{% card link="/how-tos/collect-sensor-data/" noimage="true" %}}
{{% card link="/how-tos/sensor-data-visualize/" noimage="true" %}}
{{% card link="/how-tos/sensor-data-query-with-third-party-tools/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Collect images and train machine learning models" "3" "INTERMEDIATE" >}}
{{< cards >}}
{{% card link="/how-tos/collect-data/" noimage="true" %}}
{{% card link="/how-tos/train-deploy-ml/" noimage="true" %}}
{{% card link="/how-tos/create-custom-training-scripts/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Manage a large fleet of machines" "2" "INTERMEDIATE" >}}
{{< cards >}}
{{% card link="/how-tos/manage-fleet/" noimage="true" %}}
{{% card link="/how-tos/deploy-packages/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Create and manage modular resources" "5" "INTERMEDIATE" >}}

{{< cards >}}
{{% card link="/how-tos/hello-world-module/" noimage="true" %}}
{{% card link="/how-tos/sensor-module/" noimage="true" %}}
{{% card link="/how-tos/create-module/" noimage="true" %}}
{{% card link="/how-tos/upload-module/" noimage="true" %}}
{{% card link="/how-tos/manage-modules/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

</div>

<p>If you're looking for examples of how Viam is being used in the world, have a look at <a href="https://www.viam.com/customers">customer stories</a>, follow our <a href="../tutorials/">step-by-step tutorials</a>, or browse our <a href="https://www.viam.com/blog?categories=Tutorials">blog posts</a>.</p>
</div>
