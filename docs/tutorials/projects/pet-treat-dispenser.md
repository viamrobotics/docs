---
title: "Build a machine-learning enabled pet treat dispenser"
linkTitle: "Build a Pet Treat Dispenser"
weight: 60
type: "docs"
tags: []
description: ""
image: ""
images: []
draft: true
imageAlt: ""
---

How To Build a Smart Pet Feeder With Machine Learning

Written by  | Designs by 



**Description**  \


Use the Viam app to train and deploy a custom machine learning model on your pets to have your robot give your pet treats whenever they walk by.. programmatically on a schedule! This tutorial will teach you how to design your own custom pet feeder that utilizes the Data Manager, ML Service, the Vision Service, and a stepper motor to dispense treats at the sight of your pet! 

**Introduction**

Your dog is insatiable. You wake up every morning to the sound of gentle whining at the door and the pitter patter of begging paws on the floor, and you know your fur-baby is only living for his next meal. _It’s two hours before my alarm_, you think to yourself, but you remember dogs have no sense of the manmade concept of time. The sun has barely risen on the horizon as you glance out your east facing window, and you can see a moist nose peering under your door frame. Your dog commands you: it’s time to eat. 

So what if you could build a robot to feed your pet in the morning so you can catch some extra zzz’s before work? What if you want to give your dog some treats for being a Good Boy™ while you’re spending a day in the office? 

In this tutorial you will learn how to design your own custom smart pet feeder or treat dispenser. You will learn how to train a custom machine learning model on your pet's face, programmatically or autonomously control your feeder using Viam, and how to assemble the necessary hardware and circuitry to make this happen. 

**Prerequisites **

You will need a computer and a robot set up in the Viam app. You will also need to have 

[Python3](https://www.python.org/download/releases/3.0/), [Pip](https://pip.pypa.io/en/stable/#), [viam-server](https://github.com/viamrobotics/rdk/tree/0c550c246739b87b4d5a9e8d96d2b6fdb3948e2b) installed on your machine to get started. The [Viam Python SDK](https://python.viam.dev/) is also a great reference to get started writing your own custom methods for your robot. You will also need a 3D printer for this project if you choose to use the provided STL models for this project. You may also get creative and design your own using the components, wiring, and configuration recommendations. 

**Hardware**



1. [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) with [microSD card](https://www.amazon.com/Amazon-Basics-microSDXC-Memory-Adapter/dp/B08TJTB8XS/ref=sr_1_4?crid=18AP61IEBXODY&keywords=microsd%2Bcard&qid=1680799199&s=electronics&sprefix=microsd%2Bcard%2Celectronics%2C82&sr=1-4&th=1), with [viam-server installed](https://docs.viam.com/installation/) per our installation guide
2. [Raspberry Pi power supply ](https://www.amazon.com/Raspberry-Model-Official-SC0218-Accessory/dp/B07W8XHMJZ/ref=asc_df_B07W8XHMJZ/?tag=hyprod-20&linkCode=df0&hvadid=416672671431&hvpos=&hvnetw=g&hvrand=10350240906167803476&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9067609&hvtargid=pla-815817210384&psc=1&tag=&ref=&adgrpid=95587150204&hvpone=&hvptwo=&hvadid=416672671431&hvpos=&hvnetw=g&hvrand=10350240906167803476&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9067609&hvtargid=pla-815817210384)
3. [microSD card reader](https://www.amazon.com/Card-Reader-Beikell-Memory-Adapter/dp/B09Z6JCKL7/ref=sr_1_3?crid=26L0FKD1TG7PU&keywords=micro%2Bsd%2Bcard%2Breader&qid=1680799165&s=electronics&sprefix=micro%2Bsd%2Bcard%2Breade%2Celectronics%2C90&sr=1-3&th=1)
4. [Stepper motor and motor driver ](https://makersportal.com/shop/nema-17-stepper-motor-kit-17hs4023-drv8825-bridge)
5. [12V power supply adaptor for motor driver](https://www.amazon.com/ABLEGRID-12-Volt-Power-Supply/dp/B009ZZKUPG/ref=asc_df_B009ZZKUPG/?tag=hyprod-20&linkCode=df0&hvadid=167126093426&hvpos=&hvnetw=g&hvrand=1586101707378665255&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9004405&hvtargid=pla-306189306424&psc=1)
6. [Simple USB powered webcam](https://www.amazon.com/wansview-Microphone-Streaming-Conference-Teaching/dp/B08XQ3TWFX/ref=sr_1_18_sspa?crid=31LU3CR5DFPDZ&keywords=simple+usb+webcam&qid=1680799615&sprefix=%2Caps%2C104&sr=8-18-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExQUJONDZRMUtCWkJBJmVuY3J5cHRlZElkPUEwOTAzNDQ1MlQ0TUpDU1pGQlNIWCZlbmNyeXB0ZWRBZElkPUEwNzg3NTk5Wk5KT05EQ0JUSlMzJndpZGdldE5hbWU9c3BfYnRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==) 
7. [Assorted jumper wires ](https://www.amazon.com/jumper-wires/s?k=jumper+wires)
8. [Four 16mm or 20mm M3 screws](https://www.amazon.com/Cicidorai-M3-0-5-Button-Machine-Quantity/dp/B09TKP6C6B/ref=sr_1_9?crid=1A33C0LT6BKRH&keywords=m3%2Bx%2B16%2Bmachine%2Bscrews%2Bbutton%2Bhead&qid=1681335923&sprefix=m3%2Bx%2B16%2Bmachine%2Bscrews%2Bbutton%2Bhead%2Caps%2C144&sr=8-9&th=1) 

**Other Materials**



1. Wide mouth Mason Jar or [blender cup ](https://www.amazon.com/Ninja-Single-16-Ounce-Professional-Blender/dp/B07Q23X5WP/ref=sr_1_17?crid=3TIPZDR7YTO2Q&keywords=ninja+bullet+cups&qid=1685029658&sprefix=ninja+bullet+cups%2Caps%2C84&sr=8-17)(if you want to avoid using glass!)
2. Small pet treats or dry kibble 
3. Tools for assembly such as screwdrivers and allen keys 
4. 3D printer 
5. 3D printed STL models [(provided here)](https://github.com/viam-labs/smart-pet-feeder)

**Assembling Your Robot **

You can choose to use the open source 3D printed model available to create an encasement for your robot parts, but feel free to design your own. The STL files for the smart feeder robot are available on [GitHub](https://github.com/viam-labs/smart-pet-feeder).  \


The only components you will need are a raspberry pi, a stepper motor and motor driver, a power source for your pi, a power supply for your motor driver, and a simple webcam. 



1. Prepare your 3D prints. The front of the main body of your print is the side with the dog bone! 
![alt_text](images/image1.gif "image_tooltip")

2. Mount your raspberry pi to the side of the main body of your pet feeder with the provided mounting screw holes. 
3. Connect your power source to the pi through the side hole. 
4. Mount your webcam to the front of your pet feeder. Insert your USB into your pi. 
5. Insert the 3D printed stepper motor wheel into your pet feeder. This is what will funnel treats out of your pet feeder programmatically. 
6. Place your stepper motor into the motor holder print and gently slide the wires through the hole that leads through the body of your feeder and lets out on the raspberry pi side. 
7. Slide the motor driver holder into the body of your feeder, it should sit flush and fit nicely. 
8. Connect your stepper motor to the motor driver. The diagram provided details the wiring schematics for assembling your pet feeder.

    
![alt_text](images/image2.png "image_tooltip")



    Congratulations! Now your robot should be wired correctly and you can begin to test it in the Viam app. 


**Testing and Configuring Your Robot **

Now that your robot is assembled and your components have been wired, you can now proceed to test your robot in the Viam app. Begin by creating a new robot instance in your preferred organization. 

If you haven’t already, please set up the Raspberry Pi per [these instructions](https://docs.viam.com/installation/prepare/rpi-setup/). Download the Viam app config to your pi and install viam-server on your pi as per the instructions in the setup tab.

Once that is complete, head to the Config tab and configure your **board** component, and select the model **pi. **


![alt_text](images/image3.png "image_tooltip")


Configure your webcam next. Select the **camera** component and choose the model **webcam. **The discovery service should automatically detect a path for your camera. 


![alt_text](images/image4.png "image_tooltip")


Finally, configure your stepper motor. Choose the component **motor** and the model **gpiostepper**. Following the provided wiring diagram, you will want to set the **direction** to pin 15, GPIO 22, and the **step** logic to pin 16, GPIO 23. Enable the pin setting as low and configure it to pin 18, GPIO 24. Set the **ticks per rotation** to 400 and connect it to your board model, **pi. **


![alt_text](images/image5.png "image_tooltip")


Save all your changes, and head to the Control tab. If your wiring is correct, you should be able to test all of your components there. You can set the **RPM** in the control tab to 20 and 100 revolutions to see the speed of your treat dispensing mechanism. Feel free to tweak these values to achieve the desired speed of your dispenser. 


![alt_text](images/image6.png "image_tooltip")


You can even test your **camera** and check if you can see your pet! Your pet may be a little skeptical of your robot at first, but once you get some treats in there, your furry friend will love it in no time! 


![alt_text](images/image7.png "image_tooltip")


** \
Configuring Data Management **

Let’s make our pet feeder smart with some data capture and machine learning models! First, you'll want to configure Viam’s Data Management service so you can specify the location on the robot to store data. In this case, the data we are capturing and saving is images so we can train a machine learning model on pictures of your beloved pet. To enable the data capture on your robot, do the following:



1. Under the **Config** tab, select **Services**, and navigate to **Create service**. Here, you will add a service so your robot can sync data to the Viam app in the cloud.
2. For “**type**”, select “**Data Management**” from the drop-down, and give your service a name. We used “**pet-data**” for this tutorial.
3. Be sure that Data Capture is enabled and Cloud Sync is enabled. Enabling data capture here will allow you to view the saved images for tagging and training your model. You can leave the default directory in which your captured data is stored on-robot. By default, it saves it to the &lt;file>~/.viam/capture&lt;/file> directory on your robot.


![alt_text](images/image8.png "image_tooltip")


Next, you want to enable the Data Management service on the camera component on your robot. 



1. Go to the **Components** tab for your robot and scroll down to the camera component you have previously configured.
2.  Click** + Add method **on the section labeled “Data Capture Configuration”.
3. Set the** Type** to “**ReadImage**” and the **Frequency** to “0.333”. This will capture an image from the camera roughly once every 3 seconds. Feel free to adjust the frequency if you want the camera to capture more or less image data. You want to capture data quickly so that you have as many pictures of your pet as possible so your classifier model can be very accurate. You should also select the Mime Type that you want to capture. For this tutorial, we are capturing “image/jpeg” data because they are images! 


![alt_text](images/image9.png "image_tooltip")


** \
Capturing Images of Your Pet**

Now it’s time to start collecting images of your beloved pet. We recommend setting your feeder with the camera up near an area your pet likes to hang out: your couch, their bed, mount it temporarily over their food bowl, or even just hold it in front of them for a couple of minutes. You can check that data is being captured by heading over to the **DATA **tab of the Viam app and filtering to your pet feeder robot location. Capture as many images as you want and then you can begin to train your custom model. Disable Data Capture after you’re done capturing images of your pet. 

**Turning your pet feeder smart with machine learning **

Now that you know how to configure the Data Management Service on your robot, how to collect image based data, and how to export that data– you can now take this a step further and tag and train image classification models that you can then deploy to your robot.

Head over to the **Data** page of the Viam App and select an image captured from your robot. After selecting the image, you can type a custom tag for some of the objects you see in the image. The first thing you want to consider is what tags you are trying to create and how you want your custom model to function. 


![alt_text](images/image10.png "image_tooltip")


**Tagging Images**

In this example case here, we are tagging images with the name of the pet. Notice that in our image collection, we captured images at different angles and with different background compositions. This is to ensure that our model can continue to recognize the object no matter how your robot is viewing it through its camera. 

Begin by selecting the image you would like to tag, and you will see all of the data that is associated with that image. Simply type in your desired tag in the Tags section. 


![alt_text](images/image11.png "image_tooltip")


Be mindful of your naming as you can only use alphanumeric characters and underscores: this is because the model will be exported as a _.tflite_ file as well as a corresponding_ .txt _file for labeling. 

Congratulations! You have successfully tagged your images with the labels you would like to train your model with. Note we are just tagging the whole image as we are training an image classification model.


![alt_text](images/image12.png "image_tooltip")


Continue parsing through your collected data, in this case images, and tag away to your heart's desire. Once you create tags, it is as simple as selecting your image and then selecting the tag in the **Recently used **drop down menu. Tag as many images with as many tags until you are happy with your dataset. This is important for the next step. 

**Filtering Through Tags **

Say you want to only view images in your data set that belong to a certain tag. Upon completion of tagging your data set, you can now filter images according to those tags. It is as simple as heading over to the Filtering tab and selecting your desired tag from the available drop down list. Here we have filtered images in our data set according to one tag, in this case **toast**, (which is the name of our doggy test subject!) and now we can easily view those. 


![alt_text](images/image13.png "image_tooltip")


**Training a Model**

After filtering through your desired tags, you can then select as many as you like to begin to train a model. In this case, I am selecting all the tags I generated for the images collected from this robot.

And now the moment we’ve all been waiting for…. After selecting all desired tags you can train a model. Simply click the **Train Model **button and you can then name your model and choose your classification type. Here we called it **puppymodel **as a **Single label** model type and selected the tag ‘**toast**’ to train on images of the pup!  


![alt_text](images/image14.png "image_tooltip")


Selecting **Single Label **means your results will include a single predicted label for an image. Selecting **Multi Label **means your results will include all predicted labels for an image. Go ahead and select all the tags you would like to include in your model and hit **Train Model**. This is important because your model will only be trained based on the tags you selected here. 

**Deploying Your Model to Your Robot **



1. **Add a ML model service **

To deploy a new model onto your robot, navigate to the robot page on the Viam app, and in the Config tab, select Services. Create a new service, select **ML Model **as the **Type**, name it whatever you like. Here we are naming it **puppymodel **as the **name**, and under **Model** we are selecting **tflite_cpu**. More information on the ML Model Service can be found [here](https://docs.viam.com/services/ml/#tabset-servicesml-1-1). 
![alt_text](images/image15.png "image_tooltip")
 \
 \
To configure your service and deploy a model onto your robot, select** Deploy Model On Robot **for the **Deployment** field. Select your trained model (**puppymodel)** as your desired Model. 



2. **Add a vision service. **

Create a new **Service** and select **Vision**, and **mlmodel** as the Type. Select the model you previously created in the drop down menu. 


![alt_text](images/image16.png "image_tooltip")




3. **Add a transform camera. **

To test that your vision service is working, add a **transform** camera to see your classifier in action in the Control tab.  \
 \
Navigate to the **Components** tab and **Create Component**. Create a transform camera with the name **classifier_cam**, the type **camera** and the model **transform**.

 \
Replace the JSON attributes with the following object which specifies the camera source the transform cam will be using and defines a pipeline that adds a **classifier **you created. 

Head to your robots **Control** tab and you should be able to view your transform cam that is now detecting your pets face! 


![alt_text](images/image17.png "image_tooltip")


**Controlling Your Robot Programmatically **

Now you can add a program to your robot that controls the Pet Feeder when executed, using a Viam SDK in the language of your choice.

Go to your robot’s page on the Viam app, navigate to the code sample tab, select your preferred programming language, and copy the sample code generated.

When executed, this sample code will create a connection to your robot as a client. Then control your robot programmatically by adding API method calls as shown in the following examples.

**Setting up your Python environment**

Open your terminal and `ssh` into your Pi. Run the following command to install the Python package manager onto your Pi. 

 $  |  sudo apt install python3-pip                                                                                            

The [Viam Python SDK](https://python.viam.dev/) allows you to write programs in the Python programming language to operate robots using Viam. To install thePython SDKon your Raspberry Pi, run the following command in your existing `ssh` session to your Pi:

  $  |  pip3  install  viam-sdk         

Next, create a file on the Raspberry Pi and edit the file with `nano`.

Run the following command to create a folder in your home directory to put your files in. We named ours `petfeeder`:

  $  |  mkdir ~/petfeeder                                                                                                                   

Next, navigate  to the new project directory:

  $  |  cd ~/petfeeder                                                                                                                        

Create a file using `nano` by choosing a file name and ending it with `.py` . We’ll call ours `main.py`:

  $  |  nano main.py                                                                                        

**Connect **

Head to the Code Sample tab and copy the boilerplate code sample into **main.py** and save it. Here is a sample of what your code will look like without some of the sample return value methods provided just to keep the code looking clean. Add a **go_for** [method](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.go_for) to confirm that your code is connected to your robot. Your stepper motor should turn ten times! 

Press CTRL-X to save and exit. Enter `y` to confirm, and then hit return to accept the same filename.

Now, run the code to see your stepper motor turn to check the connection, and to see if there are any errors.


  $  |  python3  main.py             

**Adding the classifier **

**Summary **
