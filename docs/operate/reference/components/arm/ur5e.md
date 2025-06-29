---
title: "Configure a UR5e Arm"
linkTitle: "ur5e"
weight: 40
type: "docs"
description: "Configure a UR5e arm."
images: ["/icons/components/arm.svg"]
tags: ["arm", "components"]
aliases:
  - "/components/arm/ur5e/"
component_description: "Supports Universal Robots UR5e."
toc_hide: true
---

Configure a `ur5e` arm to add a [Universal Robots UR5e](https://www.universal-robots.com/products/ur5-robot) to your machine.

If you want to test your arm as you configure it, connect it to your machine's computer and turn it on.
Then, configure the arm:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `arm` type, then select the `ur5e` model.
Enter a name or use the suggested name for your arm and click **Create**.

{{<imgproc src="/components/arm/ur5e-ui-config.png" resize="x1100" declaredimensions=true alt="Web UI configuration panel for an arm of model ur5e, with Attributes & Depends On dropdowns and the option to add a frame." style="width:600px" class="imgzoom shadow" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-arm-name>",
      "model": "ur5e",
      "api": "rdk:component:arm",
      "attributes": {
        "speed_degs_per_sec": <float>,
        "host": "<your-host-address>"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "my-arm",
      "model": "ur5e",
      "api": "rdk:component:arm",
      "attributes": {
        "speed_degs_per_sec": 30,
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

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------- |
| `speed_degs_per_sec` | float | **Required** | Desired maximum speed of joint movement in degrees per second. Must be between `3` and `180`. |
| `host` | string | **Required** | The IP address of the arm's system on your network. Find this when setting up your UR5e. |

{{< readfile "/static/include/components/test-control/arm-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/arm.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/arm/" customTitle="Arm API" noimage="true" %}}
{{% card link="/operate/get-started/supported-hardware/" noimage="true" %}}
{{% card link="/operate/mobility/move-arm/" noimage="true" %}}
{{< /cards >}}
