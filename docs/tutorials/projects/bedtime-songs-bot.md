---
title: "Use ML and a webcam to entertain kids with bedtime songs"
linkTitle: "Bedtime Songs Bot"
weight: 60
type: "docs"
tags: ["mac", "app", "board", "webcam", "camera", "ml", "machine learning", "babysitter"]
description: "Create a robot babysitter with a webcam and machine learning."
image: "/tutorials/img/bedtime-songs-bot/bedtime-songs-bot.png"
imageAlt: "Tess holds up brightly colored puzzle pieces in front of the camera of a Macbook laptop."
images: ["/tutorials/img/bedtime-songs-bot/bedtime-songs-bot.png"]
authors: [ "Tess Avitabile" ]
languages: [ "python" ]
viamresources: [ "camera", "sensor", "mlmodel", "vision" ]
level: "Beginner"
date: "21 April 2023"
# cost: 0 (laptop)
---

<br>
A note from the author:
</br>

<pre>

When I started at Viam, Eliot told me the best way to test the product is to try to automate something I do in my life with a robot.

As a parent of a 3-year-old and a 1-year-old, I am often presented with a toy and asked to sing a song about it.
When we were testing out Viam's ML Model service, I came up with the idea of using machine learning to make my computer do this simple task for my kids when I'm not around.

</pre>

Follow this tutorial to train a machine learning model to make your own "bedtime songs bot" out of a personal computer.

## Requirements

To make your own singing robot, you need only the following hardware:

- A computer with a webcam, speakers, and a [Viam SDK](/program/) installed

  Tess used a Macbook.
  You can use any PC or [single-board computer](/components/board/) with a Viam-compatible operating system that meets the above requirements, but you must modify the [code to program the robot](#program-your-robot-with-viams-sdks) to play songs if not using macOs.

First, you will [configure the camera on your laptop to capture data](#configure-your-webcam-to-capture-data) with the Data Management service and use it to capture images.

After that, you will filter your image data with [tags](#tag-data) and use it to train a [machine learning model](/services/ml/) on [the Viam app](https://app.viam.com).

Then, you will [configure your webcam to act as a shape classifier](#configure-your-webcam-to-act-as-a-shape-classifier) with Viam's [ML Model](/services/ml/) and [Vision](/services/vision/) Services, [record bedtime songs](#record-bedtime-songs), and [program the robot](#program-your-bedtime-songs-bot) to play a song when it recognizes a shape.

## Train your ML Model with pictures of toys

Make sure you have created a robot before starting this tutorial.
If you haven't already, follow [this guide](/installation/#install-viam-server) to install `viam-server` on your computer and connect to the corresponding robot by following the steps in the **Setup** tab of [the Viam app](https://app.viam.com).

### Configure your webcam to capture data

Navigate to your robot's page on the app and click on the **Config** tab.

First, add the camera on your computer as a [camera](/components/camera/) component by creating a new component with **type** `camera` and **model** `webcam`:

{{< tabs >}}
{{% tab name="Config Builder" %}}

![Creation of a `webcam` camera in the Viam app config builder. The user is selecting the video_path configuration attribute from the drop-down menu](../../img/bedtime-songs-bot/video-path-ui.png)

You do not have to edit the attributes of your camera at this point.
Optionally, select a fixed filepath for the camera from the automated options in the **video path** drop-down menu.

{{% /tab %}}
{{% tab name="JSON Template" %}}

``` json {class="line-numbers linkable-line-numbers"}
"components": [
   {
     "model": "webcam",
     "attributes": {},
     "depends_on": [],
     "name": "<your-camera-name>",
     "type": "camera"
   }
 ]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

``` json {class="line-numbers linkable-line-numbers"}
"components": [
   {
     "model": "webcam",
     "attributes": {},
     "depends_on": [],
     "name": "cam",
     "type": "camera"
   }
 ]
```

{{% /tab %}}
{{< /tabs >}}

Give your camera the name "`cam`" to match the name used in the code of this tutorial.
If you use a different name, change `"cam"` in the code to match the name you used.

To view your webcam's image stream, navigate to the **Control** tab of your robot's page on [the Viam app](https://app.viam.com).
Click on the drop-down menu labeled **camera** and toggle the feed on.
Click on **Export Screenshot** to capture an image.

![The image stream of a Macbook webcam in the Viam app control tab. A small wooden toy is shown on screen.](../../img/bedtime-songs-bot/export-screenshot.png)

Now, configure a [Data Management Service](/services/data/configure-data-capture/#add-the-data-management-service) with [Data Capture](/services/data/configure-data-capture/) to use the image data coming from your camera on your robot to train your ML model:

1. Under the **Config** tab, select **Services**, and navigate to **Create service**.
Here, you will add a service so your robot can sync data to the Viam app in the cloud.
1. For **type**, select **Data Management** from the drop-down, and give your service a name.
We used `Data-Management-Service` for this tutorial.
1. Ensure that **Data Capture** is enabled and **Cloud Sync** is enabled.
Enabling data capture here will allow you to view the saved images in the Viam app and allow you to easily tag them and train your own machine learning model.
You can leave the default directory as is.
This is where your captured data is stored on-robot.
By default, it saves it to the <file>~/.viam/capture</file> directory on your robot.
<!-- 
![The data management service configured with the name pet-data.](/tutorials/pet-treat-dispenser/app-service-data-management.png) -->

Next, [configure Data Capture for an individual component](/services/data/configure-data-capture/#configure-data-capture-for-individual-components) on your webcam:

1. Go to the **Components** tab and scroll down to the camera component you previously configured.
2. Click **+ Add method** in the **Data Capture Configuration** section.
3. Set the **Type** to `ReadImage` and the **Frequency** to `0.333`.
This will capture an image from the camera roughly once every 3 seconds.
  Feel free to adjust the frequency if you want the camera to capture more or less image data.
  You want to capture data quickly so your classifier model can be very accurate.
1. Select the **Mime Type** that you want to capture.
For this tutorial, we are capturing `image/jpeg` data.

![The configuration page for a camera component.](/tutorials/img/pet-treat-dispenser/app-camera-configuration.png)

At this point, the full **Raw JSON** configuration of your robot should look like the following:

{{< tabs >}}
{{% tab name="JSON Template" %}}

``` json {class="line-numbers linkable-line-numbers"}
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
               "capture_frequency_hz": <float>,
               "method": "ReadImage"
             }
           ]
         },
         "type": "data_manager"
       }
     ],
     "name": "<your-camera-name>",
     "type": "camera"
   }
 ],
 "services": [
   {
     "attributes": {
       "sync_interval_mins": <float>,
       "capture_dir": "<>",
       "tags": []
     },
     "name": "<your-data-management-service-name>",
     "type": "data_manager"
   }
 ]
}
```

If you copy and paste this template into your robot's **Raw JSON** configuration, make sure to edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Example" %}}

``` json {class="line-numbers linkable-line-numbers"}
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
               "capture_frequency_hz": 1,
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

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Important" color="tip" >}}

Make sure that you have added a `service_config` to the JSON configuration of your webcam with type `data_manager`, as well as a new service with type `data_manager`.

{{< /alert >}}

### Capture data

<!-- Navigate to the **Control** tab of your robot's page on [the Viam app](https://app.viam.com).

Click on the drop-down menu labeled **camera** and toggle the feed on to view your webcam's image stream.

![The image stream of a Macbook webcam in the Viam app control tab. A small wooden toy is shown on screen.](../../img/bedtime-songs-bot/export-screenshot.png)

Now, click on **Export Screenshot** to take pictures of the toys you want the robot to be able to recognize and differentiate between. -->

Your webcam should now be configured to automatically capture images when you are connected to your robot on [the Viam app](https://app.viam.com).

You set the rate of capture in your webcam's service configuration attibute `capture_frequency_hz`.
If you set this to `.33`, your webcam should export 1 image every 3 seconds.

At this point, grab the toys or any objects you want the robot to be able to differentiate between.
Tess's kids like playing with puzzle pieces, which come in different shape and color combinations.
Tess decided to filter between these puzzle pieces by tagging by shape, but you can filter your objects as you choose.

- Hold up the toys to the camera to capture photos of the different shapes.
Use a consistent background.
Try to get at least 50 images of each object, like each puzzle piece.

- Go to the [**DATA tab**](https://app.viam.com/data/view?view=images) in the Viam app to see the images captured by your webcam.

You are going to use these pictures to train your machine learning model.
When your webcam "sees" (captures image data containing) that toy, the robot should know to play a particular song through its computer's speakers.

### Tag data

Add tags for each of the puzzle pieces.
Tess used “octagon”, “circle”, “triangle”, “oval”, “rectangle”, “pentagon”, “diamond”, and “square”.
Try to have at least 50 images labelled for every tag.

<!-- TODO: more info here. config ui. -->

### Train a model

Follow [the tutorial](/manage/ml/train-model/) to train your ML model.

## Use your ML Model to sing songs to your kids

### Configure your webcam to act as a shape classifier

[Deploy the model](/services/ml/) to the robot and configure a [Vision Service](/services/vision/) of model `mlmodel` to use this model.

<!-- TODO: and configure mlmodel service.
more info on configuring deployment -->

``` json {class="line-numbers linkable-line-numbers"}
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
     "type": "camera",
     "model": "webcam",
     "attributes": {},
     "depends_on": []
   }
 ]
}
```

### Record bedtime songs

- Record or download the audio files you want to use to your computer in <file>.mp3</file> format.
- Make the names of the files match the classifier tags you used: for example, <file>square.mp3</file>.
- Place these files in the same directory on your computer as your SDK code.

The audio files I used are available to download on [GitHub](https://github.com/viam-labs/bedtime-songs-bot).

### Program your bedtime-songs bot

Now, write code to connect to the robot and play a song when the camera is pointed at a puzzle piece.
I used the sample code tab in the config UI to get the code to connect to the robot.
<!-- INSTRUCTIONS TO GO TO CODE SAMPLE HERE AND WHERE TO SAVE FILES ETC -->

``` go {class="line-numbers linkable-line-numbers"}
package main


import (
 "context"
 "os"
 "time"


 "github.com/edaniels/golog"
 "github.com/faiface/beep"
 "github.com/faiface/beep/mp3"
 "github.com/faiface/beep/speaker"
 "go.viam.com/rdk/robot/client"
 "go.viam.com/rdk/utils"
 "go.viam.com/utils/rpc"
 "go.viam.com/rdk/services/vision"
)


func initSpeaker(logger golog.Logger) {
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


func play(label string, logger golog.Logger) {
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

func main() {
 logger := golog.NewDevelopmentLogger("client")
 robot, err := client.New(
     context.Background(),
     "shape-classifier-main.c9iwca3k3f.viam.cloud",
     logger,
     client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
         Type:    utils.CredentialsTypeRobotLocationSecret,
         Payload: "fr8l4atdgsvsc1agh9gvjaa4zlg1z0dzf58q6to595h11asv",
     })),
 )
 if err != nil {
     logger.Fatal(err)
 }


 defer robot.Close(context.Background())
  
 visService, err := vision.FromRobot(robot, "shape-classifier")
 if err != nil {
   logger.Error(err)
 }


 initSpeaker(logger)


 for {
   // work around https://viam.atlassian.net/browse/RSDK-2396
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

<!-- Run this code on your robot by TODO: run code instructions -->

{{<gif webm_src="/tutorials/img/bedtime-songs-bot/robot_babysitter.webm" mp4_src="/tutorials/img/bedtime-songs-bot/robot_babysitter.mp4" max-width="500px" alt="A demonstration of the bedtime songs bot is taking place in an office. The author, Tess, holds up brightly colored puzzle pieces in front of the camera of a Macbook laptop. As the webcam on the laptop recognizes the puzzle pieces, different songs start to play on the speakers of the computer.">}}

## Next Steps

This project is just a start.

Expand upon the [configuration](/manage/configuration/) of your bedtime-songs bot to further customize a robot that can entertain with [machine learning](/services/ml/), the [Vision Service](/services/), and more [components](/components/) and [services](/services/).

