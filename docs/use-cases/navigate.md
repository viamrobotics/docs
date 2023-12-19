---
title: "Teleoperate and navigate with rovers"
linkTitle: "Teleoperate and navigate with rovers"
weight: 50
type: "docs"
tags: ["navigation", "motion", "services", "base", "base remote control"]
no_list: true
description: "Use Viam to teleoperate and navigate rover bases."
image: "/services/icons/navigation.svg"
imageAlt: "Navigation"
images: ["/services/icons/navigation.svg"]
---

If you have a rover base, you can teleoperate and navigate it with Viam.
Remotely control your base after configuring your machine on the app's **Control** tab, and set up autonomous navigation with the [navigation service](/mobility/navigation/).

<table>
  <tr>
    <th>{{<imgproc src="/use-cases/base-control.png" class="fill alignright" resize="200x" style="max-width: 200px" declaredimensions=true alt="Base control card">}}
      <b>1. Teleoperate</b>
      <p>Remotely control your rover base through the <a href="https://app.viam.com">Viam app.</a> Create an account and add a machine, <a href="/get-started/installation/">install viam-server</a>, and <a href="/components/base/">configure your base</a>. Then, go to the <b>Control</b> tab and access a remote control card for your base, with an interface for controlling speed, direction, and power.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/services/icons/base-rc.svg" class="fill alignleft" resize="200x" style="max-width: 200px" declaredimensions=true alt="Base remote control service icon.">}}
      <b>2. Program to move</b>
      <p>Remotely control your rover base programmatically with a <a href="/sdks/">Viam SDK.</a> Make calls to the <a href="/mobility/motion/">motion service.</a>
      Or, <a href="/mobility/base-rc/">configure a base remote control service</a> to teleoperate your base with an <a href="/components/input-controller/">input controller.</a></p>
    </th>
  </tr>
  <tr>
    <th> {{<imgproc src="/services/icons/navigation.svg" class="fill alignright" resize="200x" style="max-width: 200px" declaredimensions=true alt="Navigation icon.">}}
      <b>3. Prepare your base to navigate</b>
      <p><a href="/components/movement-sensor/">Configure a movement sensor</a> as part of your machine to use navigation.
      Then, <a href="/mobility/navigation/#configure-and-calibrate-the-frame-system-service-for-gps-navigation">configure and calibrate</a> the frame system for GPS navigation.</p>
    </th>
  </tr>
  <tr>
    <td>
    {{<imgproc src="/use-cases/navigation-card.png" class="fill alignleft" resize="200x" style="max-width: 300px" declaredimensions=true alt="Navigation map card">}}
      <b>4. Navigate</b>
      <p><a href="/mobility/navigation/">Configure a navigation service</a> on your machine. Add waypoints to define a path. Manage navigation's start and stop, see where your machine is navigating, and configure waypoints and obstacles on the <b>Control</b> tab or with a <a href="/sdks/">Viam SDK.</a></p>
    </td>
  </tr>
</table>

## Next steps

{{< cards >}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{% card link="/mobility/motion/" %}}
{{% card link="/mobility/navigation/" %}}
{{% card link="/mobility/base-rc/" %}}
{{< /cards >}}
