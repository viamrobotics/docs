---
title: "Configure a ur5e Arm"
linkTitle: "ur5e"
weight: 40
type: "docs"
description: "Configure a ur5e arm."
images: ["/components/img/components/arm.svg"]
tags: ["arm", "components"]
---

Configure a `ur5e` arm to add a [Universal Robots UR5e](https://www.universal-robots.com/products/ur5-robot) to your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your arm, select the type `arm`, and select the `ur5e` model.

Click **Create component**.

![Web UI configuration panel for an arm of model ur5e in the Viam app, with Attributes & Depends On drop-downs and the option to add a frame.](../img/ur5e-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [{
      "model": "ur5e",
      "name": "<your-arm-name>",
      "type": "arm",
      "attributes": {
        "speed_degs_per_sec": <float>,
        "host": "<your-host-address>",
      },
      "depends_on": []
    }]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "depends_on": [],
      "model": "pi",
      "name": "local",
      "type": "board",
      "attributes": {
      }
    },
    {
      "name": "my-arm",
      "type": "arm",
      "model": "ur5e",
      "attributes": {
        "speed_degs_per_sec": 1,
        "host": "10.1.10.82"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `ur5e` arms:

| Attribute | Type | Inclusion | Description |
| --------- | ---- | ----------| ----------- |
| `speed_degs_per_sec`  | float | **Required** | Desired maximum speed of joint movement in degrees/sec. <br> Range: `[.1, 1]` |
| `host`  | string | **Required** | The IP address of the arm's system on your network. Find this when setting up your ur5e. |
