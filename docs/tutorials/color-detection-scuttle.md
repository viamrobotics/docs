---
title: "Color Detection with the Scuttle Robot on Viam"
linkTitle: "Colored Object Follower"
weight: 55
type: "docs"
description: "Instructions for detecting and following a colored object with a Scuttle Robot on Viam software."
---
## Introduction

{{% note %}}
In the Python code, you must add your robot's address and secret, which are found on the **Connect** tab of the Viam App at [https://app.viam.com](https://app.viam.com) in your web browser. 
Viam App pre-populates the **Connect** tab with the robot name, address, and secret:<br>
<img src="../img/color-rdk-remote-cfg.png" />
{{% /note %}}

### Demonstration Video
{{<video src="../videos/scuttledemos_colordetection.mp4" type="video/mp4">}}

### Python.py Code 
<a href="https://gist.github.com/mestcihazal/e78e3b29c58aa301c9a197ada272e6a0" target="_blank">**Python.py GIST**</a>[^hgist]

[^hgist]:Python.py code Gist: <a href="https://gist.github.com/mestcihazal/e78e3b29c58aa301c9a197ada272e6a0" target="_blank">ht<span></span>tps://gist.github.com/mestcihazal/e78e3b29c58aa301c9a197ada272e6a0</a>

## Prerequisites
The prerequisite of this tutorial is to have a Scuttle rover which you can drive via a webUI. 
Please refer to [Setting Up Tutorial For Scuttle with a Pi](../scuttlebot). if you have not already configured your Scuttle.

Now you should try to drive the Scuttle around following the color red. 
Perhaps you can start with a red sports ball to demo with.

Download the <file>scuttle.py</file> code to a directory on your computer that you can remember. 
Feel free to choose your own location, but as an example, we’ve chosen the Desktop. 
You must already have or install <a href="https://www.anaconda.com" target="_blank">Anaconda</a>[^ana] (or <a href="https://docs.conda.io/en/latest/miniconda.html" target="_blank">Miniconda</a>[^minicon]).
 
[^ana]:Anaconda: <a href="https://www.anaconda.com" target="_blank">ht<span></span>tps://www.anaconda.com</a>
[^minicon]:Miniconda: <a href="https://docs.conda.io/en/latest/miniconda.html" target ="_blank">ht<span></span>tps://docs.conda.io/en/latest/miniconda.html</a>

Then create an environment for Python by running the following on the terminal:
```bash
conda create -n pysdk python=3.9. 
```

You can also name your environment as you wish, but please remember to keep it consistent. 
We named our environment pysdk, referring to the [Viam Python SDK](https://python.viam.dev/). 
Next, activate and navigate to this environment by running the command: 
```bash
conda activate pysdk
```

Before you can run the code, you need to install the "viam" module. 
Follow the directions at the bottom of the [Python SDK installation](https://github.com/viamrobotics/python-sdk#installation---pre-open-sourcing) guide to properly install the package. 

It will look like this on the terminal:

<img src="../img/color-det-terminal.png" />

Ensure that the package is installed in the proper environment by running the following command while in that environment:
```bash
conda list
```

You should see Viam listed near the end.

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
To learn about all the different detectors and parameters, check out the [Vision Service](../../services/vision) topic. 

The `leftOrRight()` code splits the screen vertically into thirds (left, center, and right) and makes a determination about which third the object (red ball) is in. 
Within `main()`, this decides how the robot moves (as configured by the 4 given variables). 
Run the code as is before making changes to see how it affects the output!