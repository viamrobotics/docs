---
title: "Pet Photographer: Filter Data Captures"
linkTitle: "Pet Photographer"
type: "docs"
description: "Use the filter modular component in the Viam app to photograph your pet in their collar."
tags: ["vision", "filter", "camera", "detector", "services"]
aliases:
    - /tutorials/pet-photographer
    - /tutorials/filter-modular-component
authors: [ "Sky Leilani" ]
languages: []
viamresources: [ "vision", "camera" ]
level: "Beginner"
date: "2023-09-17"
# updated: ""
cost: "0"
no_list: true
weight: 3
---

This tutorial will show you how to create a filter modular component to configure your camera to selectively capture and sync photos to the cloud when your pet enters the frame with a collar of a specified color.

Smart machines are an integral part of our daily lives.
From phones to traffic lights, the technology around us relies on the ability to process data and respond accordingly.
The filter modular component allows you to increase the precision of your model's data capture and determine which readings to store.

## Requirements 

- Update `viam-server`](/installation/manage/#update-viam-server).
If you don't already have `viam-server` installed, follow [these directions](/installation/#install-viam-server) to install the most recent, stable version.

- Clone the [Viam modular filter](https://github.com/viam-labs/modular-filter-examples) examples onto your robot's computer:

```{class="command-line" data-prompt="$"}
git clone https://github.com/viam-labs/modular-filter-examples.git
```

### Hardware

This tutorial makes use of the following hardware, but you can substitute or extend as needed.

- A collar or ribbon (use blue/green for increased precision)
- A computer
- A webcam or external camera

## Add vision service to detect color

This tutorial uses the color of my dogs collar, #43A1D0 or rgb(67, 161, 208) (blue).

## Add data management service to collect images

### Vision service

### Data management service

## Configure your camera

After you [create and connect to your robot](/manage/fleet/robots/), configure your camera to detect color following these steps:

## Program your X

## Photograph your pet

Code and directions.

## Test your X

Verify that your...

## Next steps

Write your own filter module following [this guide](/extend/modular-resources/create/).

{{< cards >}}
  {{% card link="/tutorials/get-started/blink-an-led" %}}
{{< /cards >}}
