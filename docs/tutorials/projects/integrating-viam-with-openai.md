---
title: "Integrate Viam with ChatGPT to Create a Companion Robot"
linkTitle: "AI Companion Robot"
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
images: ["/tutorials/ai-integration/rosey_robot.jpg"]
aliases: /tutorials/integrating-viam-with-openai/
imageAlt: "An AI powered companion robot called Rosey."
authors: ["Matt Vella"]
languages: ["python"]
viamresources: ["custom", "servo", "board", "mlmodel", "vision", "speech"]
level: "Intermediate"
date: "2023-02-15"
# updated: ""
cost: 200
no_list: true
---

<!-- LEARNING GOALS
After following this tutorial, you will know about modules and understand when you need to use them, and be able to find useful resources from the Viam Registry, such as the speech module.
Notes:
- Potentially requires a full rewrite.
- Keep openai as an example but make the rest more simple.
- Consider moving the tutorial as is to the blog if the resulting content is too different.
-->

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
By combining ChatGPT with the Viam platform’s built-in [computer vision service](/services/vision/), ML model support, and [locomotion](/components/base/), you can within a few hours create a basic companion robot that:

- Listens with a microphone, converts speech-to-text, gets a response from ChatGPT.
- Converts GPT response text to speech and "speaks" the response through a speaker.
- Follows commands like "move forward" and "spin".
- Makes observations about its environment when asked questions like "What do you see?".

This tutorial will show you how to use the Viam platform to create an AI-integrated robot with less than 200 lines of code.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/vR2oE4iKY6A">}}

## Hardware list

- [Raspberry Pi with microSD card](https://a.co/d/bxEdcAT), with [`viam-server` installed](/installation/prepare/rpi-setup/).
- [Viam rover](https://www.viam.com/resources/rover) (note: this tutorial can also be adapted to work with any other configured rover that has a webcam and a microphone)
- [270 degree servo](https://www.amazon.com/ANNIMOS-Digital-Waterproof-DS3218MG-Control/dp/B076CNKQX4/)
- [USB powered speaker](https://www.amazon.com/Bluetooth-Portable-Wireless-Speakers-Playtime/dp/B07PLFCP3W/) (with included 3.5mm audio cable and USB power cable)
- A servo mounting bracket - [3D printed](https://www.thingiverse.com/thing:3995995) or [purchased](https://www.amazon.com/Bolsen-Servos-Bracket-Sensor-Compatible/dp/B07HQB95VY/)
- A servo disc - [3D printed](https://github.com/viam-labs/tutorial-openai-integration/blob/main/servo_disc_large.stl) (preferred, as it is an ideal size) or [purchased](https://www.amazon.com/outstanding-Silvery-Aluminum-Steering-Screws/dp/B0BDDZW1FG/)

## Rover setup

This tutorial assumes that you have already set up your Viam Rover.
If not, first follow the Viam Rover [setup instructions](/appendix/try-viam/rover-resources/rover-tutorial/).

If you are not using a Viam Rover, [add a new machine](/cloud/machines/#add-a-new-machine) in the [Viam app](https://app.viam.com).
Then follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} to install `viam-server` on the computer you're using for your project and connect to the Viam app.
Wait until your machine has successfully connected.
Then configure your machine with the [appropriate components](/components/).
If you are using a different rover, the [Viam Rover setup instructions](/appendix/try-viam/rover-resources/rover-tutorial-fragments/) may still help you configure your robot.

### 1. Connect the servo

We'll use a [servo](/components/servo/) in this project to indicate emotion, by rotating the servo to a position that shows a happy, sad, or angry emoji.

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

- [viam-server](/get-started/)
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

Now, install the Python library dependencies by running the following command from inside the directory where you cloned the code:

```sh {class="command-line" data-prompt="$"}
pip install -r requirements.txt
```

Finally, you will need both Viam robot credentials and OpenAI API credentials in order to run the software.

{{% snippet "show-secret.md" %}}

You can find API key and API key ID values for your robot by navigating to the **CONNECT** tab in the [Viam app](https://app.viam.com) and selecting the **API keys** page.

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

To configure your [servo](/components/servo/), go to your rover's **CONFIGURE** tab.

- Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
- Select the `servo` type, then select the `pi` model (since you've attached your servo to a Raspberry Pi).
- Enter the name `servo1` for your servo and click **Create**.

Now, in the panel for `servo1`, add the following attribute configuration:

{{< imgproc src="/tutorials/ai-integration/servo_pane.png" alt="An example configuration for a pi servo with GPIO 8 and board 'local' in the Viam app Config Builder." resize="1200x" style="width:450px" >}}

- Enter `8` for `pin`.
- Select the name of your [board](/components/board/) for the `board` attribute: in this case, `local`.

This tells `viam-server` that the servo is attached to GPIO pin 8 on the board.

Press the **Save** button in the top-right corner of the page to save your config.
`viam-server` will now make the servo available for use.

Click on the **CONTROL** tab.
As long as your machine is connected to the app, you will see a panel for `servo1`.
From there, you can change the angle of your servo by increments of 1 or 10 degrees.

Move the servo to 0 degrees, and attach the emotion wheel to the servo with the happy emoji facing upwards and centered.
We found that if set up this way, the following positions accurately show the corresponding emojis, but you can verify and update the tutorial code if needed:

- happy: 0 degrees
- angry: 75 degrees
- sad: 157 degrees

### 2. Configure the ML Model and vision services to use the detector

The [ML model service](/services/ml/) allows you to deploy a machine learning model to your robot.
This tutorial uses a pre-trained machine learning (ML) model from the Viam registry named [`EfficientDet-COCO`](https://app.viam.com/ml-model/viam-labs/EfficientDet-COCO).
This model can detect a variety of objects, which you can find in the provided <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file> file.

To configure an ML model service:

- Select the **CONFIGURE** tab.
- Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
- Select the `ML model` type, then select the `TFLite CPU` model.
- Enter the name `stuff_detector` for your service and click **Create**.

Your robot will register this as a machine learning model and make it available for use.

Select **Deploy model on machine** for the **Deployment** field.
Then select the `viam-labs:EfficientDet-COCO` model from the **Models** dropdown.

Now, create a vision service to visualize your ML model:

- Select the **CONFIGURE** tab.
- Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
- Select the `vision` type, then select the `ML model` model.
- Enter the name `mlmodel` for your service and click **Create**.

Your companion robot will use this to interface with the machine learning model allowing you to - well, detect stuff!

Select the model that you added in the previous step in the **ML Model** field of your detector:

{{<imgproc src="/services/deploy-model-menu.png" resize="700x" alt="Models dropdown menu with models from the registry.">}}

Click **Save** in the top-right corner of the page to save your config.

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

## Alternative option: configure Viam Labs speech module

As an alternate option for adding an AI speech integration to your robot, [the Viam Registry](https://app.viam.com/registry) provides [the `speech` module](https://app.viam.com/module/viam-labs/speech), a modular [service](/services/) providing text-to-speech (TTS) and speech-to-text (STT) capabilities for robots running on the Viam platform.
Usage is documented on [Viam Labs' GitHub](https://github.com/viam-labs/speech).

### Configuration

Navigate to the **CONFIGURE** page of your rover robot in [the Viam app](https://app.viam.com).

{{< tabs name="Configure the speech module" >}}
{{% tab name="Builder" %}}

- Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
- Search `speech`.
- Select the `speech/speechio` option and click **Add module**.
- Give your new speech module a name of your choice.
- In the pane that appears for the service, copy and paste the following JSON into the attributes field:

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

For example:

{{< imgproc src="/tutorials/ai-integration/add-speech-module.png" alt="Adding attributes to the speech module in the Viam config builder UI for services." resize="1000x" style="width:450px" >}}

Save your config by selecting the **Save** button in the top-right corner of the page.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Select **JSON** mode.
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

Save your config by selecting the **Save** button in the top-right corner of the page.

{{% /tab %}}
{{< /tabs >}}

Use the above configuration to set up listening mode, use an ElevenLabs voice `"Antoni"`, make AI completions available, and use a 'Gollum' persona for AI completion from OpenAI.

Edit the attributes as applicable:

- Edit `"completion_provider_org"` and `"completion_provider_key"` to match your AI API organization and API credentials, for example your [OpenAI organization header and API key credentials](https://platform.openai.com/account/api-keys).
- Edit `"speech_provider_key"` to match [your API key from elevenlabs](https://docs.elevenlabs.io/api-quick-start/authentication) or another speech provider.
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
- Use Viam's [Data Management](/services/data/) to collect environmental data and use this data to train new ML models that allow the robot to improve its functionality.

We'd love to see where you decide to take this. If you build your own companion robot, let us and others know on the [Community Discord](https://discord.gg/viam).
