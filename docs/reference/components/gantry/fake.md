---
title: "fake"
linkTitle: "fake"
weight: 10
type: "docs"
description: "Reference for the fake gantry model. Fake gantry."
tags: ["gantry", "components"]
icon: true
images: ["/icons/components/gantry.svg"]
aliases:
  - "/operate/reference/components/gantry/fake/"
  - "/components/gantry/fake/"
  - "/reference/components/gantry/fake/"
component_description: "A model used for testing, with no physical hardware."
# SME: Rand
---

Configure a `fake` gantry to test implementing a gantry component on your machine without any physical hardware.
The fake gantry is single-axis: it tracks position in memory along one prismatic joint, validates moves against the axis length, always returns `false` from `IsMoving`, and returns `true` immediately from `Home`.

{{< tabs name="Configure a Fake Gantry" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-fake-gantry-name>",
  "model": "fake",
  "api": "rdk:component:gantry",
  "attributes": {
    "length_mm": <float>,
    "model_path": "<path_to_gantry_model>"
  }
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my-fake-gantry",
  "model": "fake",
  "api": "rdk:component:gantry",
  "attributes": {
    "length_mm": 1000
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `fake` gantries:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `length_mm` | float | Optional | Travel length of the single axis in millimeters. Defaults to `100` when omitted. Cannot be set together with `model_path`. |
| `model_path` | string | Optional | Path to a [kinematic configuration file](/motion-planning/frame-system/) for a single-DoF prismatic gantry. This path should point to the exact location where the file is located on your computer running `viam-server`. Cannot be set together with `length_mm`. |

See [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/gantry/fake/gantry.go) for API call return specifications.

{{< readfile "/static/include/components/test-control/gantry-control.md" >}}
