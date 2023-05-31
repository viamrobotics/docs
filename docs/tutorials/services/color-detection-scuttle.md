---
title: "Detect and Follow a Colored Object with the SCUTTLE Robot on Viam"
linkTitle: "Colored Object Follower"
weight: 30
type: "docs"
description: "Instructions for detecting and following a colored object with a SCUTTLE Robot on Viam software."
webmSrc: "/tutorials/videos/scuttle-colordetection-preview.webm"
mp4Src: "/tutorials/videos/scuttle-colordetection-preview.mp4"
videoAlt: "Detecting color with a Scuttle Robot"
images: ["/tutorials/videos/scuttle-colordetection-preview.gif"]
aliases:
    - "/tutorials/color-detection-scuttle"
    - "/tutorials/scuttlebot/color-detection-scuttle/"
tags: ["vision", "detector", "base", "scuttle", "services"]
---

{{< alert title="Caution" color="caution" >}}
There are [breaking changes in the Vision Service](/appendix/release-notes/#25-april-2023).
This tutorial has not yet been updated.
{{< /alert >}}

This tutorial shows how to use the Viam [Vision Service](/services/vision/) to make a [SCUTTLE rover](https://www.scuttlerobot.org/) follow a colored object.

{{<video webm_src="../../videos/scuttledemos_colordetection.webm" mp4_src="../../videos/scuttledemos_colordetection.mp4" poster="../../videos/scuttledemos_colordetection.jpg" alt="Detecting color with a Scuttle Robot">}}

### Code used in this tutorial

[`scuttle.py` GitHub Gist](https://gist.github.com/mestcihazal/e78e3b29c58aa301c9a197ada272e6a0)

## Prerequisites

The prerequisite of this tutorial is to have a [SCUTTLE rover](https://www.scuttlerobot.org/) connected to the [Viam app](https://app.viam.com).
Please refer to the [Configure a SCUTTLE Robot tutorial](../../configure/scuttlebot/) if you have not already configured your SCUTTLE.

### Set up your code environment

We highly suggest using a virtual Python environment like [Poetry](https://python-poetry.org) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

Then create an environment for Python by running the following on the terminal:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
poetry new pysdk  # new poetry project
conda create -n pysdk python=3.9  # new (mini)conda environment
```

You can also name your environment as you wish, but please remember to keep it consistent.
We named our environment pysdk, referring to the [Viam Python SDK](https://python.viam.dev/).

NOTE: If using (mini)conda, activate the environment by running the following command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
conda activate pysdk
```

Poetry environments are implicitly activated.

Before you can run the code, you need to install the "viam" module.
Follow the [Python SDK installation](https://github.com/viamrobotics/viam-python-sdk#installation) guide to properly install the package.

NOTE: If using a python environment, ensure that the package is installed in the proper environment.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip freeze | grep viam  # generic
poetry show | grep viam  # for poetry environments
conda list | grep viam  # for (mini)conda environments
```

You should see `viam-sdk` listed near the end.

## Save the code

Download the [<file>scuttle.py</file>](https://gist.github.com/mestcihazal/e78e3b29c58aa301c9a197ada272e6a0) code to a directory on your computer.
Feel free to choose your own location, but as an example, we’ve chosen the Desktop.

In the Python code, you must add your robot's address and secret (payload), which are found on the **Code Sample** tab of the [Viam app](https://app.viam.com).
Viam pre-populates the **Code Sample** tab with the robot name, address, and secret:

![Remote configuration JSON](../../img/color-rdk-remote-cfg.png)

{{< readfile "/static/include/snippet/secret-share.md" >}}

In your local copy of <file>scuttle.py</file>, paste your robot payload and address where indicated.
Save the file.

Now you are ready to run the code!

## Run the code

Now you should try to drive the SCUTTLE around following the color red.
You can use something like a red sports ball or book cover as a target to follow.

Navigate to the folder where you saved the Python script.
From that folder, run this in the terminal:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python scuttle.py
```

Be sure to replace <file>~/Desktop/</file> with the <file>/path/toYour/directory/</file> where the Python code was saved.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
python ~/Desktop/scuttle.py
```

## Notes on color detection operation

Within `getVisService(robot)`, a detector is configured with particular properties and subsequently added to the Vision Service.
This particular detector is a [color detector](/services/vision/detection), which means the relevant parameters are `detect_color` (hex string), `hue_tolerance_pct` (float from `0` to `1`), and `segment_size_px` (integer).
Feel free to configure more detectors with different parameters!
To learn about all the different detectors and parameters, check out the [Vision Service documentation](/services/vision/).

The `leftOrRight()` code splits the screen vertically into thirds (left, center, and right) and makes a determination about which third the object (red ball) is in.
Within `main()`, this decides how the robot moves (as configured by the 4 given variables).
Run the code as is before making changes to see how it affects the output!
