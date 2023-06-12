---
title: "Configure a yahboom-dofbot Arm"
linkTitle: "yahboom-dofbot"
weight: 34
type: "docs"
description: "Configure a yahboom-dofbot arm."
images: ["/components/img/components/arm.svg"]
tags: ["arm", "components"]
---

Configure a `yahboom-dofbot` arm to add a [Yahboom DOFBOT](https://category.yahboom.net/collections/r-robotics-arm) to your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your arm, select the type `arm`, and select the `yahboom-dofbot` model.

Click **Create component**.

![Web UI configuration panel for an arm of model yahboom-dofbot in the Viam app, with Attributes & Depends On drop-downs and the option to add a frame.](../img/yahboom-dofbot-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [{
      "model": "yahboom-dofbot",
      "name": "<your-arm-name>",
      "type": "arm",
      "attributes": {
        "board": "<your-board-name>",
        "i2c": "<your-i2c-name>"
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
        "i2cs": [
          {
            "name": "bus1",
            "bus": "1"
          }
        ]
      }
    },
    {
      "name": "myarm",
      "type": "arm",
      "model": "yahboom-dofbot",
      "attributes": {
        "board": "local",
        "i2c": "bus1"
      },
      "depends_on": [
        "local"
      ]
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `yahboom-dofbot` arms:

| Attribute | Type | Inclusion | Description |
| --------- | ---- | ----------| ----------- |
| `i2c`  | string | **Required** | The `name` of the Inter-Integrated Circuit (I<sup>2</sup>C) bus on your GPIO [board](/components/board/) where the connection to the `yahboom-dofbot` is made. See [configuration info](/components/board/#i2cs). |
