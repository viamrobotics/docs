---
title: "Integrate Viam with OpenAI to create a companion robot"
linkTitle: "Create an AI companion robot"
weight: 60
type: "docs"
tags: ["base", "AI", "ChatGPT", "servo", "vision", "computer vision", "camera", "viam rover", "python"]
description: "Harness AI to add life to your Viam rover."
# SME: Matt Vella
---

When we think of robots, most of us tend to group them into categories:

* useful robots
* bad or scary robots
* good robots

<img src="../img/ai-integration/rosey.jpeg"  style="float:right;margin-right:150px;margin-left: 20px;" alt="Rosey the robot, from the Jetsons." title="Rosey the robot, from the Jetsons." width="350" />

One type of “good” robot is a companion robot - a robot created for the purposes of providing real or apparent companionship for human beings.
While some [examples](https://www.google.com/search?q=companion+robot) have recently been brought to market - primarily for children and elderly - we are all familiar with robots from popular movies that ultimately have proven to be endearing companions and became embedded in our culture.
Think [C3P0](https://en.wikipedia.org/wiki/C-3PO), [Baymax](https://en.wikipedia.org/wiki/Baymax!), and [Rosey](https://thejetsons.fandom.com/wiki/Rosey) from the Jetsons.

AI like OpenAI's [ChatGPT](https://openai.com/blog/chatgpt/) is making companion robots with realistic, human-like speech a potential reality.
Combined with the Viam platform’s built-in [computer vision](/services/vision), ML model support, and [locomotion](/components/base/) - we can create a simple version of such a robot that:

* Listens with a microphone, converts speech-to-text, gets a response from OpenAI.
* Converts ChatGPT text to speech and "reads" this through a speaker.
* Follows commands like "move forward" and "spin".
* Makes observations about its environment with prompts like "What do you see?".

This tutorial will provide step-by-step instructions to show you how to create an AI-integrated Viam robot, including a supply list and sample code.

## Hardware list

* <a href="https://a.co/d/bxEdcAT" target="_blank">Raspberry Pi with microSD card</a>, with [`viam-server` installed](/installation/prepare/rpi-setup/).
* [Viam rover](https://www.viam.com/resources/rover) (Note: this tutorial can also be adapted to work with any other configured rover that has a webcam and a microphone)
* [270 degree servo](https://www.amazon.com/ANNIMOS-Digital-Waterproof-DS3218MG-Control/dp/B076CNKQX4/)
* [USB powered speaker](https://www.amazon.com/Bluetooth-Portable-Wireless-Speakers-Playtime/dp/B07PLFCP3W/)
* A servo mounting bracket - [3D printed](https://www.thingiverse.com/thing:3995995) or [purchased](https://www.amazon.com/Bolsen-Servos-Bracket-Sensor-Compatible/dp/B07HQB95VY/)
* A servo disc - [3D printed](https://github.com/viam-labs/tutorial-openai-integration/blob/main/servo_disc_large.stl) (preferred) or [purchased](https://www.amazon.com/outstanding-Silvery-Aluminum-Steering-Screws/dp/B0BDDZW1FG/)

## Rover setup

This tutorial assumes that you have already set up your Viam Rover.
If not, first follow the Viam Rover [setup instructions](/try-viam/rover-resources/rover-tutorial/).

### Connect the servo

We'll use a servo in this project to indicate emotion, by rotating the servo to a position that shows a happy, sad, or angry emoji.

{{% alert title="Caution" color="caution" %}}
Always disconnect devices from power before plugging, unplugging or moving wires or otherwise modifying electrical circuits.
{{% /alert %}}

Power off your rover.
Wire your servo to the Pi by attaching the black wire to ground, red wire to an available 5V pin, and yellow wire to pin 8.

### Mount the servo to your rover

Using the bracket you printed or purchased, attach the servo mount to the Viam rover so that the servo output spline is facing outward in the front of the rover(screws required, mounting holes should line up).
Attach the servo to the bracket.

<img src="../img/ai-integration/servo_mounted.jpg"   alt="Servo mounted on Viam rover." title="Servo mounted on Viam rover." width="300" />

### Servo disc

<img src="../img/ai-integration/3emotion.png"  style="float:right;margin-right:150px;margin-left: 20px;" alt="Emotion wheel." title="Emotion wheel." width="220" />

If you are 3D printing the servo disc, [download the STL file](https://github.com/viam-labs/tutorial-openai-integration/blob/main/servo_disc_large.stl) from the tutorial repository and print it.
Attach the servo disc to the servo by fitting it to the servo's output spline.

Now, download print the [emoji wheel](https://github.com/viam-labs/tutorial-openai-integration/blob/main/3emotion.png) with a color or black and white printer.
Cut the wheel out with scissors.
Do not attach it to the servo wheel yet.

### Speaker

You'll need a speaker attached to your rover so that you can hear the responses generated from OpenAI converted from text to speech.

Connect your speaker to your Pi:

* Connect the USB power cable to the speaker and any available USB port on the Pi.
* Connect 3.5mm audio cable to the speaker and the audio jack on the Pi.

Both cables come with the speaker in the [hardware list](#hardware-list), and can otherwise be easily acquired.
You may also want to attach your speaker to the top of your rover with [double-sided foam tape](https://www.amazon.com/3M-Natural-Polyurethane-Double-Coated/dp/B007Y7CA3C/), but this is optional.

### Set up tutorial software

The git repository for this tutorial contains code that integrates with:

* [viam-server](/viam/#viam-server)
* Google text/speech tools
* OpenAI

It also contains an open source machine learning [classifier model](https://tfhub.dev/google/lite-model/imagenet/mobilenet_v3_large_100_224/classification/5/metadata/1).

{{% alert title="Note" color="note"%}}
At the time this tutorial was written, OpenAI was not yet offering the ChatGPT model with their [official API](https://platform.openai.com/overview).
Therefore, this tutorial uses the [text-davinci-003](https://platform.openai.com/docs/models/davinci) GPT-3 model.

When the ChatGPT model becomes available, it is expected that the only modification to this tutorial is to change the *model* specified in the [completion](https://platform.openai.com/docs/api-reference/completions) API call.
{{% /alert %}}

Power on your Pi, choose a location on your Raspberry Pi and clone the tutorial code repository.
If you have git installed on your Pi, this is as simple as running the following command in the selected directory:

``` sh
git clone https://github.com/viam-labs/tutorial-openai-integration
```

If you don't have git installed on your Pi, you'll need to first run:

``` sh
sudo apt install git
```

## Configuration

Now that we've set up the rover by attaching the servo and making the tutorial software available on the Pi, we can configure the rover to:

* Recognize and operate the servo
* Make the ML classifier model available for use by the Viam vision service

### Configure the servo

To configure your [servo](/components/servo), go to your rover's **CONFIG** page, scroll to the bottom and create a new instance of the `servo` component.
Name it *servo1* (or something else if you prefer, but then you will need to update references to it in the tutorial code).

Since you've attached your servo to a Raspberry Pi, choose the model `pi`.
Click **Create Component**.

<img src="../img/ai-integration/servo_component_add.png" style="border:1px solid #000" alt="Adding the servo component." title="Adding the servo component." width="900" />

Now, in the card for *servo1*, add the following configuration in attributes to tell viam-server that the servo is attached to GPIO pin 8, then press the **Save Config** button.

``` json
{
  "pin": "8"
}
```

viam-server should now reconfigure and make the servo available for use.
Click into the **CONTROL** tab.
You should see a card for *servo1*.
From there, you can change the angle of your servo by increments of 1 and 10 degrees.

Move the servo to 0 degrees, and attach the emotion wheel to the servo with the happy emoji facing upwards and centered.
We found that set up this way, the following positions accurately show the corresponding emojis, but you can verify and update the tutorial code if needed:

* happy: 0 degrees
* angry: 75 degrees
* sad: 157 degrees

### Configure the Vision service and classifier

Click back to the **CONFIG** page and then to the **SERVICES** tab.
From there, scroll to the bottom and create a new service of type *Vision* named 'vision'.

<img src="../img/ai-integration/vision_service_add.png" style="border:1px solid #000" alt="Adding the vision service." title="Adding the vision service." width="500" />

Now, add the following configuration to the attributes for the Vision service.
You are registering a model of type `tflite_classifier` named `stuff_classifier`.
Your companion robot will use this to - well, classify stuff (using an ML model trained using the [ImageNet image database](https://www.image-net.org/))!

Update the `label_path` and `model_path` to match where you [copied the tutorial software](#set-up-tutorial-software).
Press "Save config" to finish adding the classifier.

``` json
{
  "register_models": [
    {
      "name": "stuff_classifier",
      "parameters": {
        "label_path": "/home/<username>/tutorial-chatgpt-integration/labels.txt",
        "num_threads": 1,
        "model_path": "/home/<username>/tutorial-chatgpt-integration/lite-model_imagenet_mobilenet_v3_large_075_224_classification_5_metadata_1.tflite"
      },
      "type": "tflite_classifier"
    }
  ]
}
```
