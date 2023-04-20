---
title: "Integrate Viam with ChatGPT to create a companion robot"
linkTitle: "Create an AI companion robot"
weight: 60
type: "docs"
tags: ["base", "AI", "OpenAI", "ChatGPT", "ElevenLabs", "servo", "vision", "computer vision", "camera", "viam rover", "python"]
description: "Harness AI to add life to your Viam rover."
image: "/tutorials/img/ai-integration/rosey_robot.jpg"
aliases:
  /tutorials/integrating-viam-with-openai/
imageAlt: "Viam Rover Rosey."
# SME: Matt Vella
---

When we think of robots, most of us tend to group them into categories:

* useful robots
* bad or scary robots
* good robots

<div class="td-max-width-on-larger-screens">
  <img src="../../img/ai-integration/rosey.jpeg" class="alignright" alt="Rosey the robot, from the Jetsons." title="Rosey the robot, from the Jetsons." style="max-width: 350px" />
</div>

One type of “good” robot is a companion robot - a robot created for the purposes of providing real or apparent companionship for human beings.
While some [examples](https://www.google.com/search?q=companion+robot) have recently been brought to market, primarily marketed towards children and the elderly, we are all familiar with robots from popular movies that ultimately have proven to be endearing companions and became embedded in our culture.
Think [C-3P0](https://en.wikipedia.org/wiki/C-3PO), [Baymax](https://en.wikipedia.org/wiki/Baymax!), and [Rosey](https://thejetsons.fandom.com/wiki/Rosey) from the Jetsons.

AI language models like OpenAI's [ChatGPT](https://openai.com/blog/chatgpt/) are making companion robots with realistic, human-like speech a potential reality.
By combining ChatGPT with the Viam platform’s built-in [computer Vision Service](/services/vision), ML model support, and [locomotion](/components/base/), you can within a few hours create a basic companion robot that:

* Listens with a microphone, converts speech-to-text, gets a response from ChatGPT.
* Converts GPT response text to speech and "speaks" the response through a speaker.
* Follows commands like "move forward" and "spin".
* Makes observations about its environment when asked questions like "What do you see?".

This tutorial will show you how to use the Viam platform to create an AI-integrated robot with less than 200 lines of code.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/vR2oE4iKY6A">}}

## Hardware list

* [Raspberry Pi with microSD card](https://a.co/d/bxEdcAT), with [`viam-server` installed](/installation/prepare/rpi-setup/).
* [Viam rover](https://www.viam.com/resources/rover) (note: this tutorial can also be adapted to work with any other configured rover that has a webcam and a microphone)
* [270 degree servo](https://www.amazon.com/ANNIMOS-Digital-Waterproof-DS3218MG-Control/dp/B076CNKQX4/)
* [USB powered speaker](https://www.amazon.com/Bluetooth-Portable-Wireless-Speakers-Playtime/dp/B07PLFCP3W/) (with included 3.5mm audio cable and USB power cable)
* A servo mounting bracket - [3D printed](https://www.thingiverse.com/thing:3995995) or [purchased](https://www.amazon.com/Bolsen-Servos-Bracket-Sensor-Compatible/dp/B07HQB95VY/)
* A servo disc - [3D printed](https://github.com/viam-labs/tutorial-openai-integration/blob/main/servo_disc_large.stl) (preferred, as it is an ideal size) or [purchased](https://www.amazon.com/outstanding-Silvery-Aluminum-Steering-Screws/dp/B0BDDZW1FG/)

## Rover setup

This tutorial assumes that you have already set up your Viam Rover.
If not, first follow the Viam Rover [setup instructions](/try-viam/rover-resources/rover-tutorial/).

If you are not using a Viam Rover, [install viam-server](/installation/) and configure your robot with the [appropriate components](/components/).
If you are using a different rover, the [Viam Rover setup instructions](https://docs.viam.com/try-viam/rover-resources/rover-tutorial-fragments/) may still help you configure your robot.

### 1. Connect the servo

We'll use a [servo](/components/servo) in this project to indicate emotion, by rotating the servo to a position that shows a happy, sad, or angry emoji.

{{% alert title="Caution" color="caution" %}}
Always disconnect devices from power before plugging, unplugging, moving wires, or otherwise modifying electrical circuits.
{{% /alert %}}

Power off your rover.
Wire your servo to the Pi by attaching the black wire to ground, red wire to [an available 5V pin](https://pinout.xyz/pinout/5v_power), and yellow wire to [pin 8](https://pinout.xyz/pinout/pin8_gpio14).

### 2. Mount the servo to your rover

Using the bracket you printed or purchased, attach the servo mount to the Viam rover so that the servo output spline is facing outward in the front of the rover (screws required, mounting holes should line up).
Attach the servo to the bracket.

<img src="../../img/ai-integration/servo_mounted.jpg"   alt="Servo mounted on Viam rover." title="Servo mounted on Viam rover." width="300" />

### 3. Servo disc

<div class="td-max-width-on-larger-screens">
  <img src="../../img/ai-integration/3emotion.png" class="alignright" alt="Emotion wheel." title="Emotion wheel." style="max-width: 220px" />
</div>

If you are 3D printing the servo disc, [download the STL file](https://github.com/viam-labs/tutorial-openai-integration/blob/main/servo_disc_large.stl) and print it.
Attach the servo disc to the servo by fitting it to the servo's output spline.

Now, download and print the [emoji wheel](https://github.com/viam-labs/tutorial-openai-integration/blob/main/3emotion.png) with a color, or black and white printer.
Cut the wheel out with scissors.
Do not attach it to the servo wheel yet.

### 4. Speaker

You need a speaker attached to your rover so that you can hear the responses generated from ChatGPT, and converted from text to speech.

Connect your speaker to your Pi:

* Connect the USB power cable to the speaker and any available USB port on the Pi.
* Connect the 3.5mm audio cable to the speaker and the audio jack on the Pi.

Both cables come with the speaker in the [hardware list](#hardware-list), and can otherwise be easily acquired.
You can also attach your speaker to the top of your rover with [double-sided foam tape](https://www.amazon.com/3M-Natural-Polyurethane-Double-Coated/dp/B007Y7CA3C/), but this is optional.

### 5. Set up tutorial software

The [git repository](https://github.com/viam-labs/tutorial-openai-integration) for this tutorial contains code that integrates with:

* [viam-server](/viam/#get-started)
* [Google text/speech tools](https://gtts.readthedocs.io/en/latest/)
* [OpenAI](https://openai.com/api/)

It also contains an open source machine learning [classifier model](https://tfhub.dev/google/lite-model/imagenet/mobilenet_v3_large_100_224/classification/5/metadata/1).

Power on  and choose a location on your Raspberry Pi, and clone the tutorial code repository.
If you have git installed on your Pi, run the following command in the preferred directory from your terminal:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
git clone https://github.com/viam-labs/tutorial-openai-integration
```

If you don't have git installed on your Pi, you will need to first run:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo apt install git
```

Now that you have cloned the repository, you will need to install dependencies.
If you do not have python3 and pip3 installed, do this first:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo apt update && sudo apt upgrade -y
sudo apt-get install python3
sudo apt install python3-pip
```

You will also need to install pyaudio, alsa, and flac:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo apt install python3-pyaudio
sudo apt-get install alsa-tools alsa-utils
sudo apt-get install flac
```

Now, install the python library dependencies by running the following command from inside the directory where you cloned the code:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
pip install -r requirements.txt
```

Finally, you will need both Viam robot credentials and OpenAI API credentials in order to run the software.
Viam credentials can be copied from the **code sample** tab on your [Viam robot page](https://app.viam.com).
To acquire OpenAI credentials, [sign up for OpenAI](https://openai.com/api/) and [set up API keys](https://platform.openai.com/account/api-keys).

Once you have both of the credentials, create a file called `run.sh`, add the following, and update the credentials within:

``` bash
#!/usr/bin/sh
export OPENAPI_KEY=abc
export OPENAPI_ORG=xyz
export VIAM_SECRET=123
export VIAM_ADDRESS=789
python rosey.py
```

Then, make `run.sh` executable:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
chmod +x run.sh
```

## Configuration

Now that we've set up the rover by attaching the servo and making the tutorial software available on the Pi, we can configure the rover to:

* Recognize and operate the servo
* Make the ML classifier model available for use by the Viam Vision Service

### 1. Configure the servo

To configure your [servo](/components/servo), go to your rover's **config** page, scroll to the bottom and create a new instance of the `servo` component.
Name it `servo1` (or something else if you prefer, but then you will need to update references to it in the tutorial code).

Since you've attached your servo to a Raspberry Pi, choose the model `pi`.
Click **Create Component**.

<img src="../../img/ai-integration/servo_component_add.png" style="border:1px solid #000" alt="Adding the servo component." title="Adding the servo component." width="900" />

Now, in the panel for *servo1*, add the following configuration in attributes to tell viam-server that the servo is attached to GPIO pin 8, then press the **Save Config** button.

``` json
{
  "pin": "8",
  "board": "local"
}
```

`viam-server` will now make the servo available for use.
Click on the **control** tab.
You should see a panel for `servo1`.
From there, you can change the angle of your servo by increments of 1 or 10 degrees.

Move the servo to 0 degrees, and attach the emotion wheel to the servo with the happy emoji facing upwards and centered.
We found that if set up this way, the following positions accurately show the corresponding emojis, but you can verify and update the tutorial code if needed:

* happy: 0 degrees
* angry: 75 degrees
* sad: 157 degrees

### 2. Configure the Vision Service and classifier

Click the **config** tab and then the **Services** subtab.
From there, scroll to the bottom and create a new service of **type** `vision` named 'vision'.

<img src="../../img/ai-integration/vision_service_add.png" style="border:1px solid #000" alt="Adding the Vision Service." title="Adding the Vision Service." width="500" />

Now, add the following configuration to the attributes for the Vision Service.
You are registering a model of **type** `tflite_classifier` **named** `stuff_classifier`.
Your companion robot will use this to - well, classify stuff (using an ML model trained using the [ImageNet image database](https://www.image-net.org/))!

Update the `label_path` and `model_path` to match where you [copied the tutorial software](#5-set-up-tutorial-software).
Click **Save config** to finish adding the classifier.

``` json
{
  "register_models": [
    {
      "name": "stuff_classifier",
      "parameters": {
        "label_path": "/home/<username>/tutorial-openai-integration/labels.txt",
        "num_threads": 1,
        "model_path": "/home/<username>/tutorial-openai-integration/lite-model_imagenet_mobilenet_v3_large_075_224_classification_5_metadata_1.tflite"
      },
      "type": "tflite_classifier"
    }
  ]
}
```

## Bring "Rosey" to life

With the rover and tutorial code set up and it is time to bring your companion robot to life!
Let's call her "Rosey", and bring her to life by running:

``` bash
./run.sh
```

Now, you can start talking to Rosey.
<img src="../../img/ai-integration/rosey_robot.jpg" class="alignright" alt="Viam Rover Rosey." title="Viam Rover Rosey." style="max-width: 350px" />
Any time she hears the keyword "Rosey", she will pay attention to anything you say immediately afterwards.
For example, if you say *"Hello Rosey, what do you think will happen today?"*, the phrase *"what do you think will happen today"* will be sent to OpenAI's chat completion API, and you'll get a response back similar to *"It is impossible to predict what will happen today.
Every day is different and unpredictable!"*

If you [explore the tutorial code](https://github.com/viam-labs/tutorial-openai-integration/blob/45ce0e3f2b7bad33f568cd4273e6721aa2ceffe5/rosey.py#L144), you will notice that some words or phrases are keywords when heard after "Rosey", and will trigger specific behavior.
For example, there are a number of commands that will cause the rover to move - like *"move forward"*, *"turn left"*, *"spin"*.

<div class="td-max-width-on-larger-screens">
<img src="../../img/ai-integration/yoda.jpeg" class="alignleft" alt="Viam Rover Rosey." title="Viam Rover Rosey." style="max-width: 300px" />

If you ask *"what do you see"*, it will use the rover's camera and a machine learning model to view the world, classify what it sees, and then read a ChatGPT-generated response about what it sees.
Also, a "mood" will be selected at random, and the response will be generated with that mood.

The GPT-3 model is quite good at responding in the style of known personas, so you can also say *"Hey Rosey, act like Yoda"*, and from that point on, responses will be generated in the style of Yoda! The tutorial code has a number of characters you can try, and to pick one randomly, you can say *"Rosey, act random"*.
You can even guess who Rosey is acting like by saying *"Rosey, I think you are Scooby Doo!"*

Much of Rosey's behavior can be modified by changing the values of parameters in the tutorial code's [params.py](https://github.com/viam-labs/tutorial-openai-integration/blob/main/params.py) file.
You can change Rosey's name to something else, add characters, adjust the classifier confidence threshold, and more.
</div>

## Use realistic custom AI voices

By default, Rosey will use Google TTS for audio voice generation.
However, [ElevenLabs](https://elevenlabs.io/) can be used for enhanced AI voice generation.
To use ElevenLabs, add your ElevenLabs API key to `run.sh` as follows:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
export ELEVENLABS_KEY=mykey
```

You can then assign voices to Rosey or any characters by adding the ElevenLabs voice name (including names of voices you have created with the [ElevenLabs VoiceLab](https://beta.elevenlabs.io/voice-lab)) in <file>params.py</file>.
For example:

``` json
{ "linda belcher": { "voice": "domi" } }
```

This opens up some really interesting possibilities, like having your robot talk to you in a voice that sounds like your favorite celebrity, or having your robot tell your cat to "Get off of the table!" in an AI version of your own voice.

## Next steps

What you've seen in this tutorial is a very basic integration between a Viam-powered robot and OpenAI.
There's a lot that could be done to make this a more production-ready companion robot.

Some ideas:

* Make the voice recognition software listen in the background, so the robot can move and interact with the world while listening and responding.
* Integrate another ML model that is used to follow a human (when told to do so).
* Add Lidar and integrate Viam's [SLAM Service](/services/slam) to map the world around it.
* Use Viam's [Data Management](/manage/data/) to collect environmental data and use this data to train new ML models that allow the robot to improve its functionality.

We'd love to see where you decide to take this. If you build your own companion robot, let us and others know on the [Community Discord](https://discord.gg/viam).
