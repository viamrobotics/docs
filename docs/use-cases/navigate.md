---
title: "Teleoperate and navigate rovers"
linkTitle: "Teleoperate and navigate with rovers"
weight: 60
type: "docs"
tags: ["navigation", "motion", "services", "base", "base remote control"]
no_list: true
description: "Use Viam to teleoperate and navigate rover bases."
images: ["/platform/mobility.svg", "/use-cases/base-control.png"]
---

If you have a rover base, you can use Viam to teleoperate it and to navigate autonomously.
Once you have configured your machine, you can remotely control your machine on the app's **CONTROL** tab, and set up autonomous navigation with the [navigation service](/mobility/navigation/).

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/use-cases/base-control.png" class="fill alignright" resize="200x" style="max-width: 200px" declaredimensions=true alt="Base control card">}}
**1. Teleoperate**

You can remotely control your rover from anywhere through the [Viam app](https://app.viam.com).
Create an account and add a machine, [install `viam-server`](/get-started/installation/), and [configure your rover base](/components/base/).
Then, go to the **CONTROL** tab and access a remote control card for your base, with an interface for controlling speed, direction, and power.
You can also view live feeds from any cameras you configure.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/base-rc.svg" class="fill alignleft" resize="200x" style="max-width: 200px" declaredimensions=true alt="Base remote control service icon.">}}
**2. Program to move**

Remotely control your rover base programmatically with a [Viam SDK](/sdks/) by making calls to the [base API](/components/base/#api).
Or, [configure the base remote control service](/mobility/base-rc/) to teleoperate your base with an [input controller.](/components/input-controller/)

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/navigation.svg" class="fill alignright" resize="200x" style="max-width: 200px" declaredimensions=true alt="Navigation icon.">}}
**3. Prepare your base to navigate**

[Configure a movement sensor](/components/movement-sensor/) as part of your machine to use navigation.
Additionally, [configure and calibrate](/mobility/navigation/#configure-and-calibrate-the-frame-system-service-for-gps-navigation) the frame system for GPS navigation.
Then, [configure the navigation service](/mobility/navigation/) on your machine.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/use-cases/navigation-card.png" class="fill alignleft" resize="200x" style="max-width: 300px" declaredimensions=true alt="Navigation map card">}}
**4. Navigate autonomously**

Define a path for your rover to navigate with waypoints and obstacles. Then, start and stop your machine's motion along the path and view your machine's current location. You can use the map interface on the **CONTROL** tab or the [navigation API](/mobility/navigation/#api).

{{< /tablestep >}}
{{< /table >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{% card link="/mobility/motion/" %}}
{{% card link="/mobility/navigation/" %}}
{{% card link="/mobility/base-rc/" %}}
{{< /cards >}}
