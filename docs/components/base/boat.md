---
title: "Configure a Boat Base"
linkTitle: "boat"
weight: 35
type: "docs"
draft: "true"
description: "Configure a boat base."
images: ["/components/img/components/base.svg"]
tags: ["base", "components"]
# SMEs: Eliot
---

A `boat` base is a model for a mobile robotic boat.
To configure a `boat` base as a component of your robot, first configure the [board](/components/board/) controlling the base and any [motors](/components/motor/) attached to the base.

{{< tabs name="Configure a Boat Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your base, select the type `base`, and select the `boat` model.

Click **Create component** and then fill in the attributes for your model:

<!-- ![An example configuration for a boat base in the Viam app Config Builder.](../img/boat-base-ui-config.png) -->

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "base",
      "type": "base",
      "model": "boat",
      "attributes": {
        "drive_mode": "<a_drive_mode_option>",
        "serial_path": "</dev/ttyXXXX>"
      },
      "depends_on": []
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `boat` bases:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `length_mm` | int | **Required** | Length of the base in millimeters. In other words, the distance between the approximate centers of the right and left wheels. Can be an approximation. |
| `width_mm` | int | **Required** | Width of the base in millimeters. In other words, the distance between the approximate centers of the right and left motors. Can be an approximation. |
| `IMU` | string | **Required** | Name of the [Inertial Measurement Unit](/components/movement-sensor/#imu-configuration) in the boat. |
| `Motors` | string[] | **Required** | JSON struct containing the configuration attributes for each motor attached to the boat. |

Each [motor](/components/motor/) inside of `Motors` has the following attributes available:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `Name` | string | **Required** | Name of the motor. |
| `x_offset_mm` | int | **Required** | |
| `y_offset_mm` | int | **Required** | |
| `angle_degs` | int | **Required** | |
| `Weight` | int | **Required** | |
