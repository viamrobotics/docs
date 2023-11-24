---
title: "Integrate Viam with ChatGPT to create a companion robot"
linkTitle: "AI Companion Robot"
weight: 5
type: "docs"
tags:
  [
    "base",
    "AI",
    "OpenAI",
    "ChatGPT",
    "ElevenLabs",
    "servo",
    "vision",
    "computer vision",
    "camera",
    "viam rover",
    "python",
  ]
description: "Harness AI and use ChatGPT to add life to your Viam rover and turn it into a companion robot."
image: "/tutorials/ai-integration/rosey_robot.jpg"
images: ["/tutorials/ai-integration/rosey_robot.jpg"]
aliases: /tutorials/integrating-viam-with-openai/
imageAlt: "An AI powered companion robot called Rosey."
authors: ["Matt Vella"]
languages: ["python"]
viamresources: ["custom", "servo", "board", "ml model", "vision", "speech"]
level: "Intermediate"
date: "2023-02-15"
# updated: ""
cost: 200
no_list: true
---

When we think of robots, most of us tend to group them into categories:

- useful robots
- bad or scary robots
- good robots

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/ai-integration/rosey.jpeg" resize="400x" declaredimensions=true alt="Rosey the robot, from the Jetsons." class="alignright" style="max-width: 350px">}}
</div>

One type of “good” robot is a companion robot - a robot created for the purposes of providing real or apparent companionship for human beings.
While some [examples](https://www.google.com/search?q=companion+robot) have recently been brought to market, primarily marketed towards children and the elderly, we are all familiar with robots from popular movies that ultimately have proven to be endearing companions and became embedded in our culture.
Think [C-3P0](https://en.wikipedia.org/wiki/C-3PO), [Baymax](https://en.wikipedia.org/wiki/Baymax!), and [Rosey](https://thejetsons.fandom.com/wiki/Rosey) from the Jetsons.

AI language models like OpenAI's [ChatGPT](https://openai.com/blog/chatgpt/) are making companion robots with realistic, human-like speech a potential reality.
By combining ChatGPT with the Viam platform’s built-in [computer vision service](/build/configure/services/vision/), ML model support, and [locomotion](/build/configure/components/base/), you can within a few hours create a basic companion robot that:

- Listens with a microphone, converts speech-to-text, gets a response from ChatGPT.
- Converts GPT response text to speech and "speaks" the response through a speaker.
- Follows commands like "move forward" and "spin".
- Makes observations about its environment when asked questions like "What do you see?".

This tutorial will show you how to use the Viam platform to create an AI-integrated robot with less than 200 lines of code.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/vR2oE4iKY6A">}}

## Hardware list

- [Raspberry Pi with microSD card](https://a.co/d/bxEdcAT), with [`viam-server` installed](/get-started/installation/prepare/rpi-setup/).
- [Viam rover](https://www.viam.com/resources/rover) (note: this tutorial can also be adapted to work with any other configured rover that has a webcam and a microphone)
- [270 degree servo](https://www.amazon.com/ANNIMOS-Digital-Waterproof-DS3218MG-Control/dp/B076CNKQX4/)
- [USB powered speaker](https://www.amazon.com/Bluetooth-Portable-Wireless-Speakers-Playtime/dp/B07PLFCP3W/) (with included 3.5mm audio cable and USB power cable)
- A servo mounting bracket - [3D printed](https://www.thingiverse.com/thing:3995995) or [purchased](https://www.amazon.com/Bolsen-Servos-Bracket-Sensor-Compatible/dp/B07HQB95VY/)
- A servo disc - [3D printed](https://github.com/viam-labs/tutorial-openai-integration/blob/main/servo_disc_large.stl) (preferred, as it is an ideal size) or [purchased](https://www.amazon.com/outstanding-Silvery-Aluminum-Steering-Screws/dp/B0BDDZW1FG/)

## Rover setup

This tutorial assumes that you have already set up your Viam Rover.
If not, first follow the Viam Rover [setup instructions](/get-started/try-viam/rover-resources/rover-tutorial/).

If you are not using a Viam Rover, [install viam-server](/get-started/installation/) and configure your robot with the [appropriate components](/build/configure/components/).
If you are using a different rover, the [Viam Rover setup instructions](/get-started/try-viam/rover-resources/rover-tutorial-fragments/) may still help you configure your robot.

### 1. Connect the servo

We'll use a [servo](/build/configure/components/servo/) in this project to indicate emotion, by rotating the servo to a position that shows a happy, sad, or angry emoji.

{{% alert title="Caution" color="caution" %}}
Always disconnect devices from power before plugging, unplugging, moving wires, or otherwise modifying electrical circuits.
{{% /alert %}}

Power off your rover.
Wire your servo to the Pi by attaching the black wire to ground, red wire to [an available 5V pin](https://pinout.xyz/pinout/5v_power), and signal wire (often yellow) to [pin 8](https://pinout.xyz/pinout/pin8_gpio14).
If your servo wires are attached to one another and the order does not match the pins on the board, you can use male-female jumper wires to connect them.

### 2. Mount the servo to your rover

Using the bracket you printed or purchased, attach the servo mount to the Viam rover so that the servo output spline is facing outward in the front of the rover (screws required, mounting holes should line up).
Attach the servo to the bracket.

{{<imgproc src="/tutorials/ai-integration/servo_mounted.jpg" resize="400x" declaredimensions=true alt="Servo mounted on Viam rover.">}}

### 3. Servo disc

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/ai-integration/3emotion.png" resize="300x" declaredimensions=true alt="Emotion wheel." class="alignright" style="max-width: 220px">}}
</div>

If you are 3D printing the servo disc, [download the STL file](https://github.com/viam-labs/tutorial-openai-integration/blob/main/servo_disc_large.stl) and print it.
Attach the servo disc to the servo by fitting it to the servo's output spline.

Now, download and print the [emoji wheel](https://github.com/viam-labs/tutorial-openai-integration/blob/main/3emotion.png) with a color, or black and white printer.
Cut the wheel out with scissors.
Do not attach it to the servo wheel yet.

### 4. Speaker

You need a speaker attached to your rover so that you can hear the responses generated from ChatGPT, and converted from text to speech.

Connect your speaker to your Pi:

- Connect the USB power cable to the speaker and any available USB port on the Pi.
- Connect the 3.5mm audio cable to the speaker and the audio jack on the Pi.

Both cables come with the speaker in the [hardware list](#hardware-list), and can otherwise be easily acquired.
You can also attach your speaker to the top of your rover with [double-sided foam tape](https://www.amazon.com/3M-Natural-Polyurethane-Double-Coated/dp/B007Y7CA3C/), but this is optional.

### 5. Set up tutorial software

The [git repository](https://github.com/viam-labs/tutorial-openai-integration) for this tutorial contains code that integrates with:

- [viam-server](/get-started/viam/#get-started)
- [Google text/speech tools](https://gtts.readthedocs.io/en/latest/)
- [OpenAI](https://openai.com/api/)

It also contains an open source machine learning [detector model](https://github.com/viam-labs/tutorial-openai-integration/tree/main/detector).

Power your Raspberry Pi on, choose a location on your Pi, and clone the tutorial code repository.

If you don't have git installed on your Pi, you will need to first run:

```sh {class="command-line" data-prompt="$"}
sudo apt install git
```

If you have git installed on your Pi, run the following command in the preferred directory from your terminal:

```sh {class="command-line" data-prompt="$"}
git clone https://github.com/viam-labs/tutorial-openai-integration
```

Now that you have cloned the repository, you will need to install dependencies.
If you do not have python3 and pip3 installed, do this first:

```sh {class="command-line" data-prompt="$"}
sudo apt update && sudo apt upgrade -y
sudo apt-get install python3
sudo apt install python3-pip
```

You will also need to install pyaudio, alsa, and flac:

```sh {class="command-line" data-prompt="$"}
sudo apt install python3-pyaudio
sudo apt-get install alsa-tools alsa-utils
sudo apt-get install flac
```

Now, install the python library dependencies by running the following command from inside the directory where you cloned the code:

```sh {class="command-line" data-prompt="$"}
pip install -r requirements.txt
```

Finally, you will need both Viam robot credentials and OpenAI API credentials in order to run the software.

{{% snippet "show-secret.md" %}}

To acquire OpenAI credentials, [sign up for OpenAI](https://openai.com/api/) and [set up API keys](https://platform.openai.com/account/api-keys).

Once you have both of the credentials, create a file called `run.sh`, add the following, and update the credentials within:

```sh {class="command-line" data-prompt="$"}
#!/usr/bin/sh
export OPENAPI_KEY=abc
export OPENAPI_ORG=xyz
export VIAM_API_KEY=123
export VIAM_API_KEY_ID=123
export VIAM_ADDRESS=789
python rosey.py
```

Then, make `run.sh` executable:

```sh {class="command-line" data-prompt="$"}
chmod +x run.sh
```

## Configuration

Now, configure your rover to:

- Recognize and operate the servo
- Make the ML detector model available for use by the Viam vision service

### 1. Configure the servo

To configure your [servo](/build/configure/components/servo/), go to your rover's **Config** tab and click the **Components** subtab.

Click **Create component** in the lower-left corner of the screen.

Select type `servo`.
Since you've attached your servo to a Raspberry Pi, choose the model `pi`.

Name it `servo1`.
Click **Create**.

{{<imgproc src="/tutorials/ai-integration/servo_component_add.png" resize="900x" declaredimensions=true alt="Adding the servo component." style="border:1px solid #000" >}}

Now, in the panel for `servo1`, add the following configuration in attributes to tell `viam-server` that the servo is attached to GPIO pin 8, then press the **Save Config** button.

```json
{
  "pin": "8",
  "board": "local"
}
```

`viam-server` will now make the servo available for use.
Click on the **Control** tab.
You should see a panel for `servo1`.
From there, you can change the angle of your servo by increments of 1 or 10 degrees.

Move the servo to 0 degrees, and attach the emotion wheel to the servo with the happy emoji facing upwards and centered.
We found that if set up this way, the following positions accurately show the corresponding emojis, but you can verify and update the tutorial code if needed:

- happy: 0 degrees
- angry: 75 degrees
- sad: 157 degrees

### 2. Configure the ML Model and vision services to use the detector

Click the **Config** tab and then the **Services** subtab.
From there, scroll to the bottom and create a new service of **type** `ML Models`, **model** `tflite_cpu` named 'stuff_detector'.
Your robot will register this as a machine learning model and make it available for use.

{{<imgproc src="/tutorials/ai-integration/mlmodels_service_add.png" resize="500x" declaredimensions=true alt="Adding the ML Models Service." style="border:1px solid #000">}}

Make sure `Path to Existing Model on Robot` is selected.

Update the **Model Path** and **Label Path** to match where you [copied the tutorial software](#5-set-up-tutorial-software).
For example, the model path would would be similar to:

```sh {class="command-line" data-prompt="$"}
/home/<username>/tutorial-openai-integration/detector/effdet0.tflite
```

and the label path similar to:

```sh {class="command-line" data-prompt="$"}
/home/<username>/tutorial-openai-integration/detector/labels.txt
```

Now, create a new service of **type** `vision`, **model** `ML Model` named 'vis-stuff-detector'.
Your companion robot will use this to interface with the machine learning model allowing you to - well, detect stuff!

{{<imgproc src="/tutorials/ai-integration/vision_service_add.png" resize="500x" declaredimensions=true alt="Adding the vision service." style="border:1px solid #000">}}

Select the model that you added in the previous step.
Click **Save config** to finish adding the detector.

## Bring "Rosey" to life

With the rover and tutorial code set up and it is time to bring your companion robot to life!
Let's call her "Rosey", and bring her to life by running:

```sh {class="command-line" data-prompt="$"}
./run.sh
```

Now, you can start talking to Rosey.
{{<imgproc src="/tutorials/ai-integration/rosey_robot.jpg" resize="400x" declaredimensions=true alt="Viam Rover Rosey." class="alignright" style="max-width: 350px">}}
Any time she hears the keyword "Rosey", she will pay attention to anything you say immediately afterwards.
For example, if you say _"Hello Rosey, what do you think will happen today?"_, the phrase _"what do you think will happen today"_ will be sent to OpenAI's chat completion API, and you'll get a response back similar to _"It is impossible to predict what will happen today.
Every day is different and unpredictable!"_

If you [explore the tutorial code](https://github.com/viam-labs/tutorial-openai-integration/blob/main/rosey.py#L192), you will notice that some words or phrases are keywords when heard after "Rosey", and will trigger specific behavior.
For example, there are a number of commands that will cause the rover to move - like _"move forward"_, _"turn left"_, _"spin"_.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/ai-integration/yoda.jpeg" resize="400x" declaredimensions=true alt="Viam Rover Rosey." class="alignleft" style="max-width: 300px">}}

If you ask _"what do you see"_, it will use the rover's camera and a machine learning model to view the world, detect what it sees, and then read a ChatGPT-generated response about what it sees.
Also, a "mood" will be selected at random, and the response will be generated with that mood.

The GPT-3 model is quite good at responding in the style of known personas, so you can also say _"Hey Rosey, act like Yoda"_, and from that point on, responses will be generated in the style of Yoda! The tutorial code has a number of characters you can try, and to pick one randomly, you can say _"Rosey, act random"_.
You can even guess who Rosey is acting like by saying _"Rosey, I think you are Scooby Doo!"_

Much of Rosey's behavior can be modified by changing the values of parameters in the tutorial code's [params.py](https://github.com/viam-labs/tutorial-openai-integration/blob/main/params.py) file.
You can change Rosey's name to something else, add characters, adjust the detector confidence threshold, and more.

</div>

## Use realistic custom AI voices

By default, Rosey will use Google TTS for audio voice generation.
However, [ElevenLabs](https://elevenlabs.io/) can be used for enhanced AI voice generation.
To use ElevenLabs, add your ElevenLabs API key to `run.sh` as follows:

```sh {class="command-line" data-prompt="$"}
export ELEVENLABS_KEY=mykey
```

You can then assign voices to Rosey or any characters by adding the ElevenLabs voice name (including names of voices you have created with the [ElevenLabs VoiceLab](https://beta.elevenlabs.io/voice-lab)) in <file>params.py</file>.
For example:

```json
{ "linda belcher": { "voice": "domi" } }
```

This opens up some really interesting possibilities, like having your robot talk to you in a voice that sounds like your favorite celebrity, or having your robot tell your cat to "Get off of the table!" in an AI version of your own voice.

## Alternative Option: Configure Viam Labs speech module

As an alternate option for adding an AI speech integration to your robot, [the Viam Registry](https://app.viam.com/registry) provides [the `speech` module](https://app.viam.com/module/viam-labs/speech), a modular [service](/build/configure/services/) providing text-to-speech (TTS) and speech-to-text (STT) capabilities for robots running on the Viam platform.
Usage is documented on [Viam Labs' GitHub](https://github.com/viam-labs/speech).

### Configuration

Navigate to the **Config** page of your rover robot in [the Viam app](https://app.viam.com).

{{< tabs name="Configure the speech module" >}}
{{% tab name="Config Builder" %}}

Click on the **Services** subtab and click the **Create service** button.
Search `speech`.
Select the `speech/speechio` option:

![Add the speech module in the Viam config builder UI for services.](/tutorials/ai-integration/add-speech-module.png)

Give your new speech module a name of your choice.
Copy and paste the following JSON into the attributes box:

```json {class="line-numbers linkable-line-numbers"}
{
  "completion_provider_org": "org-abc123",
  "completion_provider_key": "sk-mykey",
  "completion_persona": "Gollum",
  "listen": true,
  "speech_provider": "elevenlabs",
  "speech_provider_key": "keygoeshere",
  "speech_voice": "Antoni",
  "mic_device_name": "myMic"
}
```

Save the config.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Select **Raw JSON** mode.
Copy and paste the following into your `modules` array to add [`speech`](https://app.viam.com/module/viam-labs/speech) from [the Viam app's Modular Registry](https://app.viam.com/registry):

```json {class="line-numbers linkable-line-numbers"}
{
  "type": "registry",
  "name": "viam-labs_speech",
  "module_id": "viam-labs:speech",
  "version": "latest"
}
```

Then, copy and paste the following into your `services` array to add [elevenlabs.io](https://elevenlabs.io/) as your `speechio` modular service provider:

```json {class="line-numbers linkable-line-numbers"}
{
  "namespace": "viam-labs",
  "model": "viam-labs:speech:speechio",
  "attributes": {
    "completion_provider_org": "org-abc123",
    "completion_provider_key": "sk-mykey",
    "completion_persona": "Gollum",
    "listen": true,
    "speech_provider": "elevenlabs",
    "speech_provider_key": "keygoeshere",
    "speech_voice": "Antoni",
    "mic_device_name": "myMic"
  },
  "name": "speechio",
  "type": "speech"
}
```

Save the config.

{{% /tab %}}
{{< /tabs >}}

Use the above configuration to set up listening mode, use an ElevenLabs voice `"Antoni"`, make AI completions available, and use a 'Gollum' persona for AI completion from OpenAI.

Edit the attributes as applicable:

- Edit `"completion_provider_org"` and `"completion_provider_key"` to match your AI API organization and API credentials, for example your [OpenAI organization header and API key credentials](https://platform.openai.com/account/api-keys).
- Edit `"speech_provider_key"` to match [your API key from elevenlabs](https://docs.elevenlabs.io/api-reference/quick-start/authentication) or another speech provider.
- Edit `"mic_device_name"` to match the name your microphone is assigned on your robot's computer.
  Available microphone device names will logged on module startup.
  If left blank, the module will attempt to auto-detect the microphone.

## Next steps

What you've seen in this tutorial is a very basic integration between a Viam-powered robot and OpenAI.
There's a lot that could be done to make this a more production-ready companion robot.

Some ideas:

- Make the voice recognition software listen in the background, so the robot can move and interact with the world while listening and responding.
- Integrate another ML model that is used to follow a human (when told to do so).
- Add Lidar and integrate Viam's {{< glossary_tooltip term_id="slam" text="SLAM service" >}} to map the world around it.
- Use Viam's [Data Management](/data/) to collect environmental data and use this data to train new ML models that allow the robot to improve its functionality.

We'd love to see where you decide to take this. If you build your own companion robot, let us and others know on the [Community Discord](https://discord.gg/viam).
