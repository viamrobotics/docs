---
title: "Template Component"
linkTitle: "Template"
weight: 10
type: "docs"
description: "A NAME is a ..."
tags: ["camera", "components"]
icon: "../img/components.png"
draft: true
no_list: true
# SMEs:
---

<img src="../../img/components.png"  style="float:right" alt="Component picture" width="400" />

Brief description of the component and what you can do with it.

Use cases:

- A brief description of one sample use case.
- ...

Most robots with a COMPONENT need at least the following hardware:

- Board
- ...

## Configuration

Configuring this component on your robot enables you to ....
You can easily configure your component, as pictured below, on the [Viam app](https://app.viam.com/).
{{< tabs name="TabPanelExample" >}}
{{% tab name="UI"%}}

Description of how to configure the component in the UI

{{% /tab %}}
{{% tab name="JSON" %}}

```json
{
    "name": "COMPONENT_name",
    "type": "component",
    "model" : "model1|model2|model3",
    "attributes": {
        "attribute1": string, # explanation
        "attribute2": int # (optional) explanation
    }
}
```

Configure the following attributes:

- `attribute1` (`string`): Description.
- `attribute1` (`string`): *Optional.* Description.

The following is an example configuration for an Example component:

```json
{
    "name": "COMPONENT_name",
    "type": "component",
    "model" : "model1|model2|model3",
    "attributes": {
        "attribute1": string, # explanation
        "attribute2": int # (optional) explanation
    }
}
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

Troubleshooting information for configuration errors.

## Next Steps

<div class="container text-center">
  <div class="row">
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="control-a-component">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Control a COMPONENTNAME</h4>
            <p style="text-align: left;">Control your COMPONENTNAME.</p>
        <a>
    </div>
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="install">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Relevant tutorial name</h4>
            <p style="text-align: left;">Description.</p>
        </a>
    </div>
  </div>
</div>
