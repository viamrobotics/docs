--
title: "Configure a wheeledodometry movement sensor"
linkTitle: "wheeledodometry"
type: "docs"
description: "Configure a wheeledodometry movement sensor."
images: ["/icons/components/movement-sensor.svg"]
tags: ["movement sensor", "components", "movement sensor"]
# SMEs: Martha Johnston
---

Configure a `wheeledodometry` movement sensor to implement _wheeledodometry odometry_ on your robot.

Wheeled odometry is the estimation of position, orientation, linear velocity, and angular velocity using the dimensions of a base. 
<!-- Attach a `wheeledodometry` movement sensor to the motors on each wheel of a base to measure their rotation. -->
Then, you can use your wheeledodometry base with Viam's built-in services like the [navigation service](/services/navigation/).

{{< tabs name="Configure an wheeledodometry movement sensor" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your movement sensor, select the type `movement sensor`, and select the `wheeledodometry` model.

Click **Create component**.

![Configuration of a wheeledodometry movement sensor in the Viam app config builder.](/components/movement-sensor/configure-wheeledodometry.png)

Fill in and edit the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
"name" : "your-wheeledodometry-movement-sensor",
"type" : "movement_sensor",
"model" : "wheeledodometry",
"attributes" : {
    "base" : "your--base-name",
    "left_motors" : ["your-base-left-motor-name-1", "your-base-left-motor-name-2"],
    "right_motors" : ["your-base-right-motor-name-1", "your-base-right-motor-name-2"],
    "time-interval-msec": <number>
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

The following attributes are available for `wheeledodometry` movement sensors:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `base` | string | **Required** | The `name` of the [base](/components/base/) to which this movement sensor is wired. |
| `left_motors` | object | **Required** | A struct holding the names of the bases' left motors wired to this movement sensor: <ul> <li> <code>i</code>: {{< glossary_tooltip term_id="pin-number" text="Pin number" >}} of the pin to which the movement sensor is wired. </li> </ul> |
| `right_motors` | object | **Required** | A struct holding the name of the bases' right motors wired to this movement sensor: <ul> <li> <code>i</code>: {{< glossary_tooltip term_id="pin-number" text="Pin number" >}} of the pin to which the movement sensor is wired. </li> </ul> |
| `time_interval_msec` | number | **Required** | todo |
