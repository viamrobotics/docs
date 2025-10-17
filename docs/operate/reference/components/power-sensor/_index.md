---
title: "Power Sensor Component"
linkTitle: "Power Sensor"
childTitleEndOverwrite: "Power Sensor"
weight: 70
no_list: true
type: "docs"
description: "A device that provides information about a machine's power systems, including voltage, current, and power consumption."
tags: ["sensor", "components", "power sensor", "ina219", "ina226", "renogy"]
icon: true
images: ["/icons/components/power-sensor.svg"]
modulescript: true
date: "2024-10-21"
aliases:
  - "/components/power-sensor/"
hide_children: true
# SME: #team-bucket
---

The power sensor component provides an API for getting measurements of voltage, current, and power consumption.

If you have a physical power sensor, an API endpoint, or anything else that provides such measurements, use a power sensor component.

## Configuration

To use a power sensor and get its measurements, you need to add it to your machine's configuration.

Go to your machine's **CONFIGURE** page, and add a model that supports your sensor.

The following list shows the available sensor models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:power_sensor" type="power_sensor" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component compatible with the Micro-RDK.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The [power sensor API](/dev/reference/apis/components/power-sensor/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/power_sensor-table.md" >}}

## Troubleshooting

If your power sensor is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review your power sensor model's documentation to ensure you have configured all required attributes.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the power sensor there.
1. Disconnect and reconnect your power sensor.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{< /cards >}}

To capture data from the power sensor and sync it in the cloud, see the [data management service](/data-ai/capture-data/capture-sync/).
