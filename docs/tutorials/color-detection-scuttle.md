---
title: "How to Detect and Follow a Colored Object with the SCUTTLE Robot on Viam"
linkTitle: "Colored Object Follower"
weight: 30
type: "docs"
description: "Instructions for detecting and following a colored object with a SCUTTLE Robot on Viam software."
tags: ["vision", "detector", "base", "scuttle", "services"]
---
## Introduction

{{% alert title="Note" color="note" %}}

In the Python code, you must add your robot's address and secret, which are found on the **CODE SAMPLE** tab of the Viam app at [https://app.viam.com](https://app.viam.com) in your web browser.
Viam app pre-populates the **CODE SAMPLE** tab with the robot name, address, and secret:<br>
<img src="../img/color-rdk-remote-cfg.png" />
{{% /alert %}}

{{% alert title="Caution" color="caution" %}}  
Do not share your robot secret or robot address publicly. Sharing this information compromises your system security by allowing unauthorized access to your computer.
{{% /alert %}}

### Demonstration Video
{{<video src="../videos/scuttledemos_colordetection.mp4" type="video/mp4">}}

### Python.py Code
<a href="https://gist.github.com/mestcihazal/e78e3b29c58aa301c9a197ada272e6a0" target="_blank">**Python.py GIST**</a>[^hgist]

[^hgist]:Python.py code Gist: <a href="https://gist.github.com/mestcihazal/e78e3b29c58aa301c9a197ada272e6a0" target="_blank">ht<span></span>tps://gist.github.com/mestcihazal/e78e3b29c58aa301c9a197ada272e6a0</a>

## Prerequisites
The prerequisite of this tutorial is to have a SCUTTLE rover which you can drive via a webUI.
Please refer to [Setting Up Tutorial For SCUTTLE with a Pi](../scuttlebot/). if you have not already configured your SCUTTLE.

Now you should try to drive the SCUTTLE around following the color red.
Perhaps you can start with a red sports ball to demo with.

Download the <file>scuttle.py</file> code to a directory on your computer that you can remember.
Feel free to choose your own location, but as an example, we’ve chosen the Desktop.
We highly suggest using a virtual python environment like <a href="https://python-poetry.org" target="_blank">Poetry</a>[^poetry] or <a href="https://docs.conda.io/en/latest/miniconda.html" target="_blank">Miniconda</a>[^minicon].

[^poetry]:Poetry: <a href="https://python-poetry.org" target="_blank">ht<span></span>tps://python-poetry.org</a>
[^minicon]:Miniconda: <a href="https://docs.conda.io/en/latest/miniconda.html" target ="_blank">ht<span></span>tps://docs.conda.io/en/latest/miniconda.html</a>

Then create an environment for Python by running the following on the terminal:
```bash
poetry new pysdk  # new poetry project
conda create -n pysdk python=3.9  # new (mini)conda environment
```

You can also name your environment as you wish, but please remember to keep it consistent.
We named our environment pysdk, referring to the [Viam Python SDK](https://python.viam.dev/).

NOTE: If using (mini)conda, activate the environment by running the command:
```bash
conda activate pysdk
```
Poetry environments are implicitly activated.

Before you can run the code, you need to install the "viam" module.
Follow the <a href="https://github.com/viamrobotics/viam-python-sdk#installation" target="_blank">Python SDK installation</a>[^pos] guide to properly install the package.

[^pos]:Python SDK installation: <a href="https://github.com/viamrobotics/viam-python-sdk#installation" target="_blank">ht<span></span>tps://github.com/viamrobotics/viam-python-sdk#installation</a>

NOTE: If using a python environment, ensure that the package is installed in the proper environment.
```bash
pip freeze | grep viam  # generic
poetry show | grep viam  # for poetry environments
conda list | grep viam  # for (mini)conda environments
```

You should see `viam-sdk` listed near the end.

Now you are ready to run the code!

## Running the code

Navigate to the folder you saved the Python script into. From that folder, run in the terminal:
```bash
python scuttle.py
```
Be sure to replace “~/Desktop/” with the “/path/toYour/directory/” where the Python code was saved.
```bash
python ~/Desktop/scuttle.py
```

## Notes on Color Detection Operation

Within `getVisService(robot)`, a detector is configured with particular properties and subsequently added to the vision service.
This particular detector is a "color" detector, which means the relevant parameters are “detect_color (hex string)”, “hue_tolerance_pct (float from 0 to 1)”, and “segment_size_px (integer).”
Feel free to add new detectors with different parameters!
To learn about all the different detectors and parameters, check out the [Vision Service](../../services/vision/) topic.

The `leftOrRight()` code splits the screen vertically into thirds (left, center, and right) and makes a determination about which third the object (red ball) is in.
Within `main()`, this decides how the robot moves (as configured by the 4 given variables).
Run the code as is before making changes to see how it affects the output!
