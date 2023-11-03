---
title: "Build a bedtime songs bot with a custom ML model"
linkTitle: "Bedtime Songs Bot"
type: "docs"
tags:
  [
    "mac",
    "app",
    "board",
    "webcam",
    "camera",
    "ml",
    "machine learning",
    "babysitter",
  ]
description: "Create a robot babysitter with a webcam and machine learning."
images: ["/tutorials/img/bedtime-songs-bot/robot_babysitter.gif"]
webmSrc: "/tutorials/img/bedtime-songs-bot/robot_babysitter.webm"
mp4Src: "/tutorials/img/bedtime-songs-bot/robot_babysitter.mp4"
videoAlt: "A demonstration of the bedtime songs bot is taking place in an office. Tess holds up brightly colored puzzle pieces in front of the camera of a Macbook laptop. As the webcam on the laptop recognizes the puzzle pieces, different songs start to play on the speakers of the computer."
authors: ["Tess Avitabile", "Sierra Guequierre"]
languages: ["python"]
viamresources: ["camera", "sensor", "mlmodel", "vision"]
level: "Intermediate"
date: "2023-08-18"
# updated: ""
cost: "0"
---

{{< alert title="Creator's note" color="note" >}}

"When I started at Viam, Eliot Horowitz told me the best way to test the product is to try to automate something I do in my life with a robot.
As a parent of a 3-year-old and a 1-year-old, I am often presented with a toy and asked to sing a song about it.
When I was testing out Viam's ML Model service, I came up with the idea of using machine learning to make my computer do this instead."

<p style="text-align: right;">Tess, Engineering Director</p>
{{< /alert >}}

Follow this tutorial to train a machine learning model to make your own "bedtime songs bot" out of a personal computer.

## Get started

To make your own singing robot, you need the following hardware:

- A computer with a webcam, speakers, and the [Go Client SDK](https://pkg.go.dev/go.viam.com/rdk) installed.
  Tess used a Macbook, but you can use any PC with a Viam-compatible operating system that meets the above requirements.

While following this tutorial, you'll complete the following steps to train and utilize a machine learning model on a webcam:

- [Get started](#get-started)
- [Train your ML Model with pictures of toys](#train-your-ml-model-with-pictures-of-toys)
  - [Configure your webcam to capture data](#configure-your-webcam-to-capture-data)
  - [Capture data](#capture-data)
  - [Tag data](#tag-data)
    - [Filter based on tags](#filter-based-on-tags)
  - [Train a model](#train-a-model)
- [Use your ML Model to sing songs to your kids](#use-your-ml-model-to-sing-songs-to-your-kids)
  - [Configure your webcam to act as a shape classifier](#configure-your-webcam-to-act-as-a-shape-classifier)
  - [Record bedtime songs](#record-bedtime-songs)
  - [Program your bedtime-songs bot](#program-your-bedtime-songs-bot)
- [Next steps](#next-steps)

## Train your ML Model with pictures of toys

### Configure your webcam to capture data

In the [Viam app](https://app.viam.com), create a new robot and follow the steps on your new robot’s **Setup** tab.

Navigate to your robot's page on the app and click on the [**Config** tab](/manage/configuration/).

First, add your personal computer's webcam to your robot as a [camera](/components/camera/) by creating a new component with **type** `camera` and **model** `webcam`:

{{< tabs >}}
{{% tab name="Builder UI" %}}

Click the **Components** subtab, then click **Create component** in the lower-left corner of the page.

Select `camera` for the type, then select `webcam` for the model.
Enter `cam` for the name of your [camera component](/components/camera/), then click **Create**.

![Creation of a `webcam` camera in the Viam app config builder. The user is selecting the video_path configuration attribute from the drop-down menu](../../tutorials/bedtime-songs-bot/video-path-ui.png)

You do not have to edit the attributes of your camera at this point.
Optionally, select a fixed filepath for the camera from the automated options in the **video path** drop-down menu.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

On the [`Raw JSON` tab](/manage/configuration/#the-config-tab), replace the configuration with the following JSON configuration for your camera:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "model": "webcam",
      "attributes": {},
      "depends_on": [],
      "name": "cam",
      "type": "camera"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

If you use a different name, adapt the code in the later steps of this tutorial to use the name you give your camera.

To view your webcam's image stream, navigate to the **Control** tab of your robot's page on [the Viam app](https://app.viam.com).
Click on the drop-down menu labeled **camera** and toggle the feed on.
If you want to test your webcam's image capture, you can click on **Export Screenshot** to capture an image, as shown below:

{{<imgproc src="../../tutorials/bedtime-songs-bot/export-screenshot.png" resize="400x" declaredimensions=true alt="The image stream of a Macbook webcam in the Viam app control tab. A small wooden toy is shown on the screen." >}}

Now, configure the [Data Management Service](/services/data/configure-data-capture/#add-the-data-management-service) to [capture data](/services/data/configure-data-capture/), so you can use the image data coming from your camera on your robot to train your ML model:

{{< tabs >}}
{{% tab name="Builder UI" %}}

1. On the **Config** tab, select **Services**, and navigate to **Create service**.
2. Add a service so your robot can sync data to the Viam app in the cloud: For **type**, select **Data Management** from the drop-down, and name your service `Data-Management-Service`.
   If you use a different name, adapt the code in the later steps of this tutorial to use the name you give your service.
3. Make sure both **Data Capture** and **Cloud Sync** are enabled as shown:

   {{<imgproc src="../../tutorials/bedtime-songs-bot/enable-data-capture-cloud-sync.png" resize="400x" declaredimensions=true alt="Data capture and cloud sync enabled for a singular component" >}}

   Enabling data capture and cloud sync lets you capture images from your webcam, sync them to the cloud and, in the Viam app, easily tag them and train your own machine learning model.

   You can leave the default directory as is.
   By default, captured data is saved to the <file>~/.viam/capture</file> directory on-robot.

Next, [configure Data Capture for your webcam](/services/data/configure-data-capture/#configure-data-capture-for-individual-components):

1. Go to the **Components** tab and scroll down to the camera component you previously configured.
2. Click **+ Add method** in the **Data Capture Configuration** section.
3. Set the **Type** to `ReadImage` and the **Frequency** to `0.333`.
   This will capture an image from the camera roughly once every 3 seconds.
   Feel free to adjust the frequency if you want the camera to capture more or less image data.
   You want to capture data quickly so your classifier model can be very accurate.
4. Select the **Mime Type** as `image/jpeg`:

{{<imgproc src="../../tutorials/bedtime-songs-bot/app-camera-configuration.png" resize="400x" declaredimensions=true alt="The configuration page for a camera component." >}}

{{% /tab %}}
{{% tab name="Raw JSON" %}}

At this point, the full **Raw JSON** configuration of your robot should look like the following:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "model": "webcam",
      "attributes": {},
      "depends_on": [],
      "service_config": [
        {
          "attributes": {
            "capture_methods": [
              {
                "additional_params": {
                  "mime_type": "image/jpeg"
                },
                "capture_frequency_hz": 0.333,
                "method": "ReadImage"
              }
            ]
          },
          "type": "data_manager"
        }
      ],
      "name": "cam",
      "type": "camera"
    }
  ],
  "services": [
    {
      "attributes": {
        "sync_interval_mins": 0.1,
        "capture_dir": "",
        "tags": []
      },
      "name": "Data-Management-Service",
      "type": "data_manager"
    }
  ]
}
```

Make sure that you have added a `service_config` to the JSON configuration of your webcam with type `data_manager`, as well as a new service with type `data_manager`, as shown above.

{{% /tab %}}
{{< /tabs >}}

### Capture data

Your webcam is now configured to automatically capture images when you are connected to your robot live on [the Viam app](https://app.viam.com).
At this point, grab the toys or any objects you want the robot to be able to differentiate between.

Tess's kids like playing with puzzle pieces, which come in different shapes and color combinations.
They decided to filter between these puzzle pieces by tagging by shape, but you can filter your objects as you choose.

Hold up the toys to the camera while photos are being taken.
Try to capture images from different angles and backgrounds.
Try to get at least 50 images that fit your criteria for each tag.

You set the rate of capture in your webcam's service configuration attribute `capture_frequency_hz`.
If you set this to `.333`, the data management service will capture 1 image roughly every 3 seconds as you hold up your toys to the camera.

Go to the [**DATA tab**](https://app.viam.com/data/view?view=images) in the Viam app to see the images captured by your webcam.

When you've captured enough images to tag, navigate back to the **Config** tab.
Scroll to the card with the name of your webcam and click the power switch next to the **Data Capture Configuration** to **off** to [disable data capture](/services/data/configure-data-capture/#configure-data-capture-for-individual-components).

Now, use these pictures to train your machine learning model.

### Tag data

Head over to the [**DATA** page](https://app.viam.com/data/view) and select an image captured from your robot.
After selecting the image, you will see all of the data that is associated with that image.

[Add tags](/manage/data/label/#image-tags) for each of the puzzle pieces.
Type in your desired tag in the **Tags** section and save the tag.
Since Tess wanted to classify their toys by shape, they used `“octagon”`, `“circle”`, `“triangle”`, `“oval"`, `“rectangle”`, `“pentagon”`, `“diamond”`, and `“square”`.

Scroll between your images.
Add tags for each image that shows an object of the corresponding shape.
You can select tags from the **Recently used** drop down menu.
Try to have at least 50 images labeled for each tag.
This is important for the next step.

#### Filter based on tags

Now that you've tagged the image data, you have the option to [filter your images](/manage/data/view/) according to those tags.
Head over to the **Filtering** menu and select a tag from the drop down list to view all labeled images.

### Train a model

After tagging and filtering your images, begin training your model.

Click the **Train Model** button.
Name your model `"shape-classifier-model"`.
If you use a different name, adapt the code in the later steps of this tutorial to use the name you give your model.
Select **Multi label** as the model type, which accounts for multiple tags.

Then select the tags that you used to label your toys and click **Train Model**.

Read through our guide to [training a new model](/manage/ml/train-model/) for more information.

## Use your ML Model to sing songs to your kids

### Configure your webcam to act as a shape classifier

[Deploy the model](/services/ml/) to the robot and [configure a vision service classifier of model `mlmodel`](/services/vision/classification/#configure-an-mlmodel-classifier) to use the model you've trained to classify objects in your robot's field of vision.

Name your `mlmodel` vision service `"shape-classifier"`.
If you use a different name, adapt the code in the later steps of this tutorial to use the name you give your service.

{{< tabs >}}
{{% tab name="Raw JSON" %}}

At this point, the full **Raw JSON** configuration of your robot should look like the following:

```json {class="line-numbers linkable-line-numbers"}
{
  "packages": [
    {
      "name": "shapes",
      "version": "latest",
      "package": "20055b44-c8a7-4bc5-ad93-86900ee9735a/shapes"
    }
  ],
  "services": [
    {
      "name": "shape-classifier-model",
      "type": "mlmodel",
      "model": "tflite_cpu",
      "attributes": {
        "model_path": "${packages.shapes}/shapes.tflite",
        "label_path": "${packages.shapes}/labels.txt",
        "num_threads": 1
      }
    },
    {
      "name": "shape-classifier",
      "type": "vision",
      "model": "mlmodel",
      "attributes": {
        "mlmodel_name": "shape-classifier-model"
      }
    }
  ],
  "components": [
    {
      "name": "cam",
      "model": "webcam",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

### Record bedtime songs

Now, capture the audio of the songs you want your bot to play.

- Record or download the audio files you want to use to your computer in <file>.mp3</file> format.
- Make the names of the files match the classifier tags you used: for example, <file>square.mp3</file>.
- Navigate to a directory where you want to store your SDK code.
  Save your audio files inside of this directory.

The audio files Tess used are available to download on [GitHub](https://github.com/viam-labs/bedtime-songs-bot).

### Program your bedtime-songs bot

Now, use Viam's Go SDK to program your robot so that if your webcam "sees" (captures image data containing) a toy, the robot knows to play a particular song through its computer's speakers.

Follow these instructions to start working on your Go control code:

1. Navigate to your robot's page in [the Viam app](https://app.viam.com), and click on the **Code sample** tab.
2. Select **Go** as the language.
3. Click **Copy** to copy the generated code sample, which establishes a connection with your robot when run.

   {{% snippet "show-secret.md" %}}

4. Open your terminal.
   Navigate to the directory where you want to store your code.
   Paste this code sample into a new file named <file>play-songs.go</file>, and save it.

For example, run the following commands on your Macbook to create and open the file:

```sh {class="command-line" data-prompt="$"}
cd <insert-path-to>/<my-bedtime-songs-bot-directory>
touch play-songs.go
vim play-songs.go
```

Now, you can add code into <file>play-songs.go</file> to write the logic that defines your bedtime songs bot.

To start, add in the code that initializes your speaker and plays the songs.
Tess used the platform-flexible [Go `os` package](https://pkg.go.dev/os) and an audio processing package from [GitHub](https://github.com/faiface/beep/) to do this.

```go {class="line-numbers linkable-line-numbers"}
func initSpeaker(logger logger.Logger) {
   f, err := os.Open("square.mp3")
   if err != nil {
       logger.Fatal(err)
   }
   defer f.Close()


   streamer, format, err := mp3.Decode(f)
   if err != nil {
       logger.Fatal(err)
   }
   defer streamer.Close()


   speaker.Init(format.SampleRate, format.SampleRate.N(time.Second/10))
}


func play(label string, logger logger.Logger) {
   f, err := os.Open(label + ".mp3")
   if err != nil {
       logger.Fatal(err)
   }
   defer f.Close()


   streamer, _, err := mp3.Decode(f)
   if err != nil {
       logger.Fatal(err)
   }
   defer streamer.Close()


   done := make(chan bool)
   speaker.Play(beep.Seq(streamer, beep.Callback(func() {
       done <- true
   })))


   <-done
}
```

Modify the above code as you desire.

Make sure you import the necessary packages by adding the following to the `import` statement of your program:

```go
"github.com/faiface/beep"
"github.com/faiface/beep/mp3"
"github.com/faiface/beep/speaker"
```

Also, make sure that you add `initSpeaker(logger)`, a line that initializes the speaker, to the `main` function of your program.

Now, create the logic for the classifiers.
Use the vision service's [classification](/services/vision/classification/) API method `ClassificationsFromCamera` to do this.

You can get your components from the robot like this:

```go
visService, err := vision.FromRobot(robot, "shape-classifier")
```

And you can get the classification the `"shape-classifier-model"` behind `"shape-classifier"` computes for your robot like this:

```go
classifications, err := visService.ClassificationsFromCamera(context.Background(), "cam", 1, nil)
```

Change the `name` in [FromRobot()](/program/apis/#fromrobot) if you used a different name for the resource in your code.

This is what Tess used for the logic for the classifiers:

```go
// Classifications logic
for {
  for i := 0; i < 3; i++ {
      visService.ClassificationsFromCamera(context.Background(), "cam",  1, nil)
  }


  classifications, err := visService.ClassificationsFromCamera(context.Background(), "cam", 1, nil)
  if err != nil {
      logger.Fatalf("Could not get classifications: %v", err)
  }
  if len(classifications) > 0 && classifications[0].Score() > 0.7 {
      logger.Info(classifications[0])
      play(classifications[0].Label(), logger)
  }


}
```

After completing these instructions, your program <file>play-songs.go</file> should look like the following:

```go {class="line-numbers linkable-line-numbers"}
package main


import (
 "context"
 "os"
 "time"


 "github.com/faiface/beep"
 "github.com/faiface/beep/mp3"
 "github.com/faiface/beep/speaker"
 "go.viam.com/rdk/logging"
 "go.viam.com/rdk/robot/client"
 "go.viam.com/rdk/utils"
 "go.viam.com/utils/rpc"
 "go.viam.com/rdk/services/vision"
)

// Initialize the speaker
func initSpeaker(logger logger.Logger) {
   f, err := os.Open("square.mp3")
   if err != nil {
       logger.Fatal(err)
   }
   defer f.Close()


   streamer, format, err := mp3.Decode(f)
   if err != nil {
       logger.Fatal(err)
   }
   defer streamer.Close()


   speaker.Init(format.SampleRate, format.SampleRate.N(time.Second/10))
}

// Play a song
func play(label string, logger logger.Logger) {
   f, err := os.Open(label + ".mp3")
   if err != nil {
       logger.Fatal(err)
   }
   defer f.Close()


   streamer, _, err := mp3.Decode(f)
   if err != nil {
       logger.Fatal(err)
   }
   defer streamer.Close()


   done := make(chan bool)
   speaker.Play(beep.Seq(streamer, beep.Callback(func() {
       done <- true
   })))


   <-done
}

// Code Sample Connect() Code
func main() {
 logger := logger.NewDevelopmentLogger("client")
 robot, err := client.New(
     context.Background(),
     ".viam.cloud", // Insert your remote address here. Go to the Code Sample tab in the Viam app to find.
     logger,
     client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
         Type:    utils.CredentialsTypeRobotLocationSecret,
         Payload: "", // Insert your robot location secret here. Go to the Code Sample tab in the Viam app to find.
     })),
 )
 if err != nil {
     logger.Fatal(err)
 }


 defer robot.Close(context.Background())

// Get the shape classifier from the robot
 visService, err := vision.FromRobot(robot, "shape-classifier")
 if err != nil {
   logger.Error(err)
 }

 // Initialize the speaker
 initSpeaker(logger)


 // Classifications logic
 for {
   for i := 0; i < 3; i++ {
       visService.ClassificationsFromCamera(context.Background(), "cam",  1, nil)
   }


   classifications, err := visService.ClassificationsFromCamera(context.Background(), "cam", 1, nil)
   if err != nil {
       logger.Fatalf("Could not get classifications: %v", err)
   }
   if len(classifications) > 0 && classifications[0].Score() > 0.7 {
       logger.Info(classifications[0])
       play(classifications[0].Label(), logger)
   }


 }
}
```

Save your <file>play-songs.go</file> program with this logic added in.
Run the code on your personal computer as follows:

```sh {class="command-line" data-prompt="$"}
go run ~/<my-bedtime-songs-bot-directory>/play-songs.go
```

The full example source code for <file>play-songs.go</file> is available on [GitHub](https://github.com/viam-labs/bedtime-songs-bot/blob/main/play_songs.go).

Now, as shown below, your smart bedtime songs bot knows to play a song whenever it sees a shape on the camera:

{{<video webm_src="/tutorials/img/bedtime-songs-bot/robot_babysitter.webm" mp4_src="/tutorials/img/bedtime-songs-bot/robot_babysitter.mp4" max-width="500px" alt="A demonstration of the bedtime songs bot is taking place in an office. Tess holds up brightly colored puzzle pieces in front of the camera of a Macbook laptop. As the webcam on the laptop recognizes the puzzle pieces, different songs start to play on the speakers of the computer." poster="/tutorials/bedtime-songs-bot/robot-babysitter-preview.png">}}

## Next steps

This project is just a start.

Expand upon the [configuration](/manage/configuration/) of your bedtime-songs bot to further customize a robot that can entertain with [machine learning](/services/ml/), the [vision service](/services/), and more [components](/components/) and [services](/services/).
