---
title: "Title of your tutorial in <70 characters"
linkTitle: "Menu title of the tutorial"
type: "docs"
description:
  "Short description of your tutorial (1 sentence)."
  # If GIF+video is available use those - otherwise use an image and omit webmSrc and mp4Src.
  # The GIF or image in "images" will show up in links on social media/in Slack messages etc.
  # The webmSrc and mp4Src will show up on the tutorials page and should be the the same GIF as above,
  # but in these formats which use less bandwidth than GIF when a user is loading our site.
# images: ["path to preview GIF if available and less than 1MB in size - otherwise path to preview image"]
# webmSrc: "path to preview video - ideally in 4:3 format"
# mp4Src: "path to preview video - ideally in 4:3 format"
# imageAlt: "ALT text for the image"
# videoAlt: "ALT text for the video" (omit either imageAlt or videoAlt depending on preview type)
tags: ["tutorial"]
draft: true # Change this when you're ready
authors: [] # Your Name
weight: # A positive integer that determines the position of the tutorial on the tutorials page. New content is automatically featured. Only use this to highlight content that should permanently be near the top.
languages: [] # Viam SDK programming languages used, if any
viamresources: [
    "arm",
    "base",
    "board",
    "camera",
    "encoder",
    "gantry",
    "gripper",
    "input_controller",
    "motor",
    "movement_sensor",
    "sensor",
    "servo",
    "data_manager",
    "motion",
    "frame_system",
    "mlmodel",
    "navigation",
    "base_remote_control",
    "sensors",
    "slam",
    "vision",
  ] # Specific components or services used in this tutorial
level: "" # Beginner, Intermediate, Advanced
# Beginner means: high level of explanation and guidance
# Intermediate means: commands/concepts you can assume the reader knows do not need to be explained, instead link.
# Advanced means: intricate tutorial that may require the reader to have knowledge to adapt
date: "2023-01-01" # When the tutorial was created or last entirely checked
# updated: ""  # When the tutorial was last entirely checked
cost: 0 # Aproximate cost in USD - Only specify number
---

Outline the why.
Tell the story of the machine.

## Requirements

What does the reader need to already know.
What will you be using (hardware/software).

## Build X

Build steps

## Configure your X

Configuration steps

## Program your X

Code and directions.

## Next steps

Link to other tutorials with cards or text.

{{< cards >}}
{{% card link="/tutorials/get-started/blink-an-led" %}}
{{< /cards >}}
