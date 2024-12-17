---
linkTitle: "Deploy & Manage"
title: "Deploy, manage, and troubleshoot"
weight: 300
layout: "docs"
type: "docs"
no_list: true
open_on_desktop: true
overview: true
---

<p>
{{<imgproc src="/platform-overviews/fleet.png" resize="1200x" style="width:800px" class="aligncenter imgzoom" declaredimensions=true alt="ALT">}}
</p>

<!-- Viam fleet management allows you to deploy, manage, and monitor any number of machines alone or in collaboration with others.
You can manage and control your fleet of {{< glossary_tooltip term_id="machine" text="smart machines" >}} from the [Viam app](https://app.viam.com), using the [CLI](/cli/), or using the [fleet management API](/appendix/apis/fleet/). -->

<!-- Maybe add images of this:
For example, you might have 30 robots in one warehouse and 500 in another.
You can monitor and teleoperate all of the robots from one online dashboard, and grant permission to other users to do the same.
You can grant users different levels of access to individual machines or to groups of machines. -->

{{< how-to-expand "Deploy a fleet of machines" "3" "INTERMEDIATE" "light" >}}
{{< cards >}}
{{% card link="/manage/fleet/reuse-configuration/" noimage="true" %}}
{{% card link="/manage/fleet/provision/setup/" noimage="true" %}}
{{% card link="/manage/fleet/provision/end-user-setup/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Manage software on many machines" "2" "INTERMEDIATE" "light" >}}
{{< cards >}}
{{% card link="/manage/software/deploy-packages/" noimage="true" %}}
{{% card link="/manage/software/update-packages/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Manage access for organizations" "1" "INTERMEDIATE" "middle" >}}
{{< cards >}}
{{% card link="/manage/manage/access/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}

{{< how-to-expand "Remotely monitor and troubleshoot" "5" "INTERMEDIATE" "dark" >}}
{{< cards >}}
{{% card link="/manage/troubleshoot/monitor/" noimage="true" %}}
{{% card link="/manage/troubleshoot/alert/" noimage="true" %}}
{{% card link="/manage/troubleshoot/teleoperate/custom-interface" customTitle="Teleoperate with custom interface" noimage="true" %}}
{{% card link="/manage/troubleshoot/teleoperate/default-interface" customTitle="Teleoperate with default interface" noimage="true" %}}
{{% card link="/manage/troubleshoot/troubleshoot/" noimage="true" %}}
{{< /cards >}}
{{< /how-to-expand >}}
