---
title: "Use ML and a webcam to entertain with bedtime songs"
linkTitle: "Bedtime Songs Bot"
weight: 60
type: "docs"
tags: ["mac", "app", "board", "webcam", "camera", "ml", "machine learning", "babysitter"]
description: "Create a robot babysitter with a webcam and machine learning."
image: "/tutorials/img/robot-babysitter/robot_babysitter.jpg"
imageAlt: "Tess holds up brightly colored puzzle pieces in front of the camera of a Macbook laptop."
images: ["/tutorials/img/robot-babysitter/robot_babysitter.jpg"]
authors: [ "Tess Avitabile" ]
languages: [ "python" ]
viamresources: [ "camera", "sensor", "mlmodel", "vision" ]
level: "Beginner"
date: "21 April 2023"
# cost: 0 (laptop)
---

{{<gif webm_src="/tutorials/img/robot-babysitter/robot_babysitter.webm" mp4_src="/tutorials/img/robot-babysitter/robot_babysitter.mp4" max-width="500px" alt="A demonstration of the bedtime songs bot is taking place in an office. The author, Tess, holds up brightly colored puzzle pieces in front of the camera of a Macbook laptop. As the webcam on the laptop recognizes the puzzle pieces, different songs start to play on the speakers of the computer.">}}

<br>

A Note From the Author:

<pre>

When I started at Viam, Eliot told me the best way to test the product is to try to automate something I do in my life with a robot.

As a parent of a 3-year-old and a 1-year-old, I am often presented with a toy and asked to sing a song about it.
When we were testing out Viam's ML Model service, I came up with the idea of using machine learning to make my computer do this simple task for my kids when I'm not around.

As I created this babysitting program myself, I was able to customize it to recognize the different toys my kid likes to play with and sing the songs I wanted it to in my voice.
In the future, I'd build a babysitting robot that does more to respond to the sight of different toys, like spin around gadgets or tell a story with integrated ChatGPT.

</pre>

This tutorial teaches how to make your own singing robot babysitter.
The instructions here are just a start.
Expand upon this tutorial to customize your "babysitting bot" with [machine learning](/services/ml/), the [Vision Service](/services/), and more [components](/components/) and [services](/services/).

To make your own babysitting bedtime-songs bot, you need only the following hardware:

- A computer with a webcam and speakers

Tess used a Macbook.
You can use any PC or [single-board computer](/components/board/) with a Viam-compatible operating system that meets these requirements, but you will need to modify the code to program the robot to play songs if not using MacOs.

To start,  you will configure the camera on your laptop to capture data with the Data Management service, and use it to capture images.
You will learn how to filter this image data with tags of your choice and use it to train a [machine learning model](/services/ml/) on [the Viam app](https://app.viam.com).

Then, you'll configure that same camera to act as a shape classifier with Viam's [ML Model](/services/ml/) and [Vision](/services/vision/) Services.

## Part 1: Train your ML Model with pictures of toys

Make sure you have created a robot before starting this tutorial.
If you haven't already, follow [this guide](/installation/#install-viam-server) to install `viam-server` on your computer and connect to the corresponding robot by following the steps in the **Setup** tab of [the Viam app](https://app.viam.com).

### Configure your webcam to capture data

Navigate to your robot's page on the app and click on the **Config** tab.

First, add the camera on your computer as a [camera](/components/camera/) component by creating a new component with **type** `camera` and **model** `webcam`:

{{< tabs >}}
{{% tab name="Config Builder" %}}

![Creation of a `webcam` camera in the Viam app config builder. The user is selecting the video_path configuration attribute from the drop-down menu](../../img/robot-babysitter/video-path-ui.png)

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

Now that you've added your camera, follow these instructions [to add a data management service](/services/data/configure-data-capture/#add-the-data-management-service) to your robot and [configure data capture](/services/data/configure-data-capture/#configure-data-capture-for-individual-components) on the camera.

{{< alert title="Important" color="tip" >}}

Make sure that you add a `service_config` to the JSON configuration of your webcam with type `data_manager`, as well as a new service with type `data_manager`.

{{< /alert >}}

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
               "capture_frequency_hz": 5,
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

### Take pictures

Navigate to the **Control** tab of your robot's page on [the Viam app](https://app.viam.com).

Click on the drop-down menu labeled **camera** and toggle the feed on to view your webcam's image stream.

![The image stream of a Macbook webcam in the Viam app control tab. A small wooden toy is shown on screen.](../../img/robot-babysitter/export-screenshot.png)

Now, click on **Export Screenshot** to take pictures of the toys you want the robot to be able to recognize and differentiate between.

You are going to use these pictures to train your machine learning model so that when your webcam "sees" (captures image data containing) that toy, the robot knows to play a particular song through its computer's speakers.

My kids like playing with brightly colored puzzle pieces, which come in different shape and color combinations.
Tess decided to tag by shape, but you can filter your objects as you choose.
Capture pictures of the different shapes.
Use a consistent background.
Try to get at least 50 images of each object, like each puzzle piece.

### Tag data

Add tags for each of the puzzle pieces.
Tess used “octagon”, “circle”, “triangle”, “oval”, “rectangle”, “pentagon”, “diamond”, and “square”.
They recommend tagging at least 50 images for each shape.

<!-- TODO: more info here. config ui. -->

### Train a model

Follow [the tutorial](/manage/ml/train-model/) to train your ML model.

## PART 2: Use your ML Model to sing songs to your kids

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

### Program your robot with Viam's SDKs

Put mp3 files with the same names as the classifier tags in the folder with the code (i.e. square.mp3, etc).
Here are my songs.

<!-- TODO: insert mp3s from google drive -->

Write code to connect to the robot and play a song when the camera is pointed at a puzzle piece.
I used the sample code tab in the config UI to get the code to connect to the robot.
Here is a video of me demoing this.

<!-- (TODO: SEE TICKET. trim down video) -->

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

The audio files I used are available on [GitHub](https://github.com/viam-labs/singing-babysitter/tree/main/songs) here.

## Next Steps

<!-- TODO: can do a lot more with this tutorial -->
