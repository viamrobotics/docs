---
title: "Teleoperate and navigate rovers"
linkTitle: "Teleoperate and navigate with rovers"
weight: 60
type: "docs"
tags: ["navigation", "motion", "services", "base", "base remote control"]
no_list: true
description: "Use Viam to teleoperate and navigate rover bases."
image: "/services/icons/navigation.svg"
imageAlt: "Navigation"
images: ["/services/icons/navigation.svg"]
---

If you have a rover base, you can use Viam to teleoperate it and to navigate autonomously.
Once you have configured your machine, you can remotely control your machine on the app's **Control** tab, and set up autonomous navigation with the [navigation service](/mobility/navigation/).

<table>
  <tr>
    <th>{{<imgproc src="/use-cases/base-control.png" class="fill alignright" resize="200x" style="max-width: 200px" declaredimensions=true alt="Base control card">}}
      <b>1. Teleoperate</b>
      <p>You can remotely control your rover from anywhere through the <a href="https://app.viam.com">Viam app.</a> Create an account and add a machine, <a href="/get-started/installation/">install viam-server</a>, and <a href="/components/base/">configure your rover base</a>. Then, go to the <b>Control</b> tab and access a remote control card for your base, with an interface for controlling speed, direction, and power. You can also view live feeds from any cameras you configure.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/services/icons/base-rc.svg" class="fill alignleft" resize="200x" style="max-width: 200px" declaredimensions=true alt="Base remote control service icon.">}}
      <b>2. Program to move</b>
      <p>Remotely control your rover base programmatically with a <a href="/sdks/">Viam SDK</a> by making calls to the <a href="/components/base/#api">base API</a>.
      Or, <a href="/mobility/base-rc/">configure the base remote control service</a> to teleoperate your base with an <a href="/components/input-controller/">input controller.</a></p>
    </th>
  </tr>
  <tr>
    <th> {{<imgproc src="/services/icons/navigation.svg" class="fill alignright" resize="200x" style="max-width: 200px" declaredimensions=true alt="Navigation icon.">}}
      <b>3. Prepare your base to navigate</b>
      <p><a href="/components/movement-sensor/">Configure a movement sensor</a> as part of your machine to use navigation.
      Additionally, <a href="/mobility/navigation/#configure-and-calibrate-the-frame-system-service-for-gps-navigation">configure and calibrate</a> the frame system for GPS navigation.
      Then, <a href="/mobility/navigation/">configure a navigation service</a> on your machine.</p>
    </th>
  </tr>
  <tr>
    <td>
    {{<imgproc src="/use-cases/navigation-card.png" class="fill alignleft" resize="200x" style="max-width: 300px" declaredimensions=true alt="Navigation map card">}}
      <b>4. Navigate autonomously</b>
      <p>Define a path for your rover to navigate with waypoints and obstacles. Then, start and stop your machine's motion along the path and view your machine's current location. You can use the map interface on the <b>Control</b> tab or the <a href="/mobility/navigation/#api">navigation API</a>.</p>
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
