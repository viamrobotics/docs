---
title: "Template Component"
linkTitle: "Template"
weight: 10
type: "docs"
description: "A NAME is a ..."
tags: ["camera", "components"]
# icon: "img/components/name.png"
draft: true
# SMEs:
---

Brief description of the component and what you can do with it.

Use cases:

- A brief description of one sample use case.
- ...

Requirements:

- Board
- ...

## Configuration

```json-viam
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

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `attribute1`         | string | Description. |
| `attribute2`         | int | *Optional.* Description. |

The following is an example configuration for an Example component:

```json-viam
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

## Troubleshooting

Troubleshooting information for configuration errors.

### Next Steps

<div class="container text-center">
  <div class="row">
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="prepare">
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
