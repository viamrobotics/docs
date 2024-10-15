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
# updated: ""  # When the content was last entirely checked
---

<p>
    Click on one of the following guides that provide solutions for common tasks and workflows.
</p>
<p>
    What area would you like to explore?
</p>

<div id="tutorial-menu" class="lozad">
  <div id="resource-list" style="display:none;"></div>
  <div id="platformarea-list" data-parent="#tutorial-menu"></div>
</div>
<div id="how-to-paths">
</div>
<div class="search-panel__results card-container lozad">
    <div id="hits" class="row-no-margin"></div>
    <div id="pagination"></div>
</div>
<!-- if no javascript show the how-tos -->
<noscript>
    <div class="alert alert-caution" role="alert">
        <h4 class="alert-heading">Javascript</h4>
        <p>Please enable javascript to see all how-to guides.</p>
    </div>
    <div class="card-container">
        <div class="row-no-margin">
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/configure/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/develop-app/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/image-data/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/deploy-ml/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/collect-sensor-data/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/sensor-data-query-with-third-party-tools/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/sensor-data-query-sdk/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/sensor-data-visualize/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/create-module/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/sensor-module/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/upload-module/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/manage-modules/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/navigate/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/one-to-many/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/provision-setup/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/provision/") }}
            {{ partial "tutorialcard-no-js.html" (dict "link" "/how-tos/manage-fleet/") }}
        </div>
    </div>
</noscript>

<div id="how-to-paths">

{{< how-to-expand title="Get started with Viam basics" tasks="4" level="BEGINNER-FRIENDLY" >}}
{{< cards >}}
{{% card link="/how-tos/drive-rover/" %}}
{{% card link="/how-tos/control-motor/" %}}
{{% card link="/how-tos/detect-people/" %}}
{{% card link="/how-tos/collect-data/" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Configure a fleet, starting with one machine" "4" "BEGINNER-FRIENDLY" >}}
{{< cards >}}
{{% card link="/how-tos/configure/" %}}
{{% card link="/how-tos/one-to-many/" %}}
{{% card link="/how-tos/provision-setup/" %}}
{{% card link="/how-tos/provision/" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Manage a large fleet of machines" "2" "INTERMEDIATE" >}}
{{< cards >}}
{{% card link="/how-tos/manage-fleet/" %}}
{{% card link="/how-tos/deploy-packages/" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Work with data across machines" "4" "INTERMEDIATE" >}}
{{< cards >}}
{{% card link="/how-tos/collect-sensor-data/" %}}
{{% card link="/how-tos/sensor-data-visualize/" %}}
{{% card link="/how-tos/sensor-data-query-sdk/" %}}
{{% card link="/how-tos/sensor-data-query-with-third-party-tools/" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Create and manage modular resources" "4" "INTERMEDIATE" >}}
{{< cards >}}
{{% card link="/how-tos/sensor-module/" %}}
{{% card link="/how-tos/create-module/" %}}
{{% card link="/how-tos/upload-module/" %}}
{{% card link="/how-tos/manage-modules/" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Collect images and train machine learning models" "3" "INTERMEDIATE" >}}
{{< cards >}}
{{% card link="/how-tos/collect-data/" %}}
{{% card link="/how-tos/create-custom-training-scripts/" %}}
{{% card link="/how-tos/deploy-ml/" %}}
{{< /cards >}}
{{< /how-to-expand >}}

</div>

<p>If you're looking for examples of how Viam is being used in the world, have a look at <a href="https://www.viam.com/customers">customer stories</a>, follow our <a href="../tutorials/">step-by-step tutorials</a>, or browse our <a href="https://www.viam.com/blog?categories=Tutorials">blog posts</a>.</p>
