---
linkTitle: "Move a base"
title: "Move a wheeled robot base"
weight: 40
layout: "docs"
type: "docs"
no_list: true
description: "Move a mobile robot with manual or autonomous navigation."
---

You have three options for moving a mobile robot base:

- Give direct commands such as `Spin` and `MoveStraight` using the [base API](/dev/reference/apis/components/base/)
- Send the base to a destination on a SLAM map or to a GPS coordinate using the [motion planning service API's](/dev/reference/apis/services/motion/) `MoveOnMap` or `MoveOnGlobe` commands, respectively
- Define waypoints and move your base along those waypoints while avoiding obstacles, using the [navigation service API](/dev/reference/apis/services/navigation)

{{< cards >}}
{{% card link="/dev/reference/apis/components/base/" %}}
{{% card link="/dev/reference/apis/services/motion/" %}}
{{% card link="/dev/reference/apis/services/navigation/" %}}
{{< /cards >}}

## Example usage

{{< cards >}}
{{% card link="/tutorials/control/drive-rover/" %}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}
