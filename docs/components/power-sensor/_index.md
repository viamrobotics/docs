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
aliases:
  - "/components/power-sensor/"
hide_children: true
# SME: #team-bucket
---

If you have a physical power sensor, an API endpoint, or anything else that provides measurements of voltage, current, and power consumption, use a _power sensor_ component.

The sensor component is often used alongside the [data management service](/services/data/), which allows you to capture and sync the sensor's data.

## Available models

To use a power sensor and get its measurements, you have to add it as well as any dependencies, such as a board and a configured analog-to-digital converter (ADC), to your machine's configuration.

Go to your machine's **CONFIGURE** page, and add a model that supports your sensor.

The following list shows you the available sensor models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:power_sensor" type="power_sensor" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component in `viam-micro-server`.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

To get started using your power sensor, see the [power sensor API](/appendix/apis/components/power-sensor/), which supports the following methods:

{{< readfile "/static/include/components/apis/generated/power_sensor-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next steps

For general configuration and development info, see:

{{< cards >}}
  {{% card link="/how-tos/configure/" noimage="true" %}}
  {{% card link="/how-tos/develop-app/" noimage="true" %}}
  {{% card link="/how-tos/collect-sensor-data/" noimage="true" %}}
{{< /cards >}}