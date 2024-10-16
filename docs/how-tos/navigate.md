---
title: "Teleoperate and navigate rovers"
linkTitle: "Teleoperate and navigate with rovers"
weight: 60
type: "docs"
tags: ["navigation", "motion", "services", "base", "base remote control"]
no_list: true
description: "Use Viam to teleoperate and navigate rover bases."
images: ["/platform/mobility.svg", "/how-tos/base-control.png"]
aliases:
  - /use-cases/navigate/
languages: []
viamresources:
  ["base", "movement_sensor", "motion", "frame_system", "navigation"]
platformarea: ["mobility"]
level: "Intermediate"
date: "2024-01-04"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

If you have a rover base, you can use Viam to teleoperate it and to navigate autonomously.
Once you have configured your machine, you can remotely control your machine on the app's **CONTROL** tab, and set up autonomous navigation with the [navigation service](/services/navigation/).

{{< table >}}
{{% tablestep link="/components/base/wheeled/#test-the-base" %}}
{{<imgproc src="/how-tos/base-control.png" class="fill alignleft" resize="200x" style="width: 200px" declaredimensions=true alt="Base control card">}}
**1. Teleoperate**

You can remotely control your rover from anywhere through the [Viam app](https://app.viam.com).
After physically setting up the hardware on your base and powering the base on, create an account and add a machine, [install `viam-server`](/installation/viam-server-setup/), and [configure your rover base](/components/base/).
Then, go to the **CONTROL** tab and access a remote control card for your base, with an interface for controlling speed, direction, and power.
You can also view live feeds from any cameras you configure.

{{% /tablestep %}}
{{% tablestep link="/sdks/"%}}
{{<imgproc src="/services/icons/base-rc.svg" class="fill alignleft" resize="200x" style="width: 200px" declaredimensions=true alt="Base remote control service icon.">}}
**2. Program to move**

Remotely control your rover base programmatically with a [Viam SDK](/sdks/) by making calls to the [base API](/appendix/apis/components/base/#api).
Or, [configure the base remote control service](/services/base-rc/) to teleoperate your base with an [input controller.](/components/input-controller/)

{{% /tablestep %}}
{{% tablestep link="/services/navigation/"%}}
{{<imgproc src="/services/icons/navigation.svg" class="fill alignleft" resize="200x" style="width: 200px" declaredimensions=true alt="Navigation icon.">}}
**3. Prepare your base to navigate**

[Configure a movement sensor](/components/movement-sensor/) as part of your machine to use navigation.
Additionally, [configure and calibrate](/services/navigation/#configure-and-calibrate-the-frame-system-service-for-gps-navigation) the frame system for GPS navigation.
Then, [configure the navigation service](/services/navigation/) on your machine.

{{% /tablestep %}}
{{% tablestep link="/services/navigation/#api" %}}
{{<imgproc src="/how-tos/navigation-card.png" class="fill alignleft" resize="200x" style="width: 300px" declaredimensions=true alt="Navigation map card">}}
**4. Navigate autonomously**

Define a path for your rover to navigate with waypoints and obstacles. Then, start and stop your machine's motion along the path and view your machine's current location. You can use the map interface on the **CONTROL** tab or the [navigation API](/appendix/apis/services/navigation/#api).

{{% /tablestep %}}
{{< /table >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{% card link="/services/motion/" %}}
{{% card link="/services/navigation/" %}}
{{% card link="/services/base-rc/" %}}
{{< /cards >}}
