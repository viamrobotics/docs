---
title: "Changelog"
linkTitle: "Changelog"
weight: 20
draft: false
type: "docs"
description: "A log of added features, improvements, and changes over time."
aliases:
  - "/appendix/release-notes/"
  - "/components/camera/single-stream/"
  - "/components/camera/dual-stream/"
  - "/components/camera/align-color-depth-extrinsics/"
  - "/components/camera/align-color-depth-homography/"
  - "/components/board/customlinux/"
  - "/components/board/jetson/"
  - "/components/board/pca9685/"
  - "/components/board/ti/"
  - "/components/gripper/softrobotics/"
  - "/components/motor/encoded-motor/"
  - "/components/motor/gpiostepper/"
  - "/components/motor/roboclaw/"
  - "/components/movement-sensor/adxl345/"
  - "/components/movement-sensor/dual-gps-rtk/"
  - "/components/movement-sensor/gps-nmea-rtk-pmtk/"
  - "/components/movement-sensor/gps-nmea-rtk-serial/"
  - "/components/movement-sensor/gps-nmea/"
  - "/components/movement-sensor/wheeled-odometry/"
  - "/components/power-sensor/ina219/"
  - "/components/power-sensor/ina226/"
  - "/components/sensor/bme280/"
  - "/components/sensor/ds18b20/"
  - "/components/sensor/sensirion-sht3xd/"
  - /appendix/changelog/
layout: "changelog"
outputs:
  - rss
  - html
date: "2024-09-18"
# updated: ""  # When the content was last entirely checked
---

<!-- If there is no concrete date for a change that makes sense, use the end of the month it was released in. -->

{{% changelog date="2024-11-12" color="added" title="Builtin models moved to modules" %}}

The following resource models have moved to modules.

<!-- prettier-ignore -->
| Resource | Model |
| -------- | ----- |
| board | [`customlinux`](https://github.com/viam-modules/customlinux/) |
| board | [`jetson`](https://github.com/viam-modules/nvidia) |
| board | [`pca9685`](https://github.com/viam-modules/pca/tree/main) |
| board | [`odroid`](https://github.com/viam-modules/hardkernel) |
| board | [`ti`](https://github.com/viam-modules/texas-instruments) |
| board | [`pi`](https://github.com/viam-modules/raspberry-pi) |
| board | [`orange-pi`](https://github.com/viam-modules/orange-pi) |
| board | [`upboard`](https://github.com/viam-modules/up) |
| motor | [`tmc5072`](https://github.com/viam-modules/analog-devices) |
| motor | [`28byj-48`](https://github.com/viam-modules/uln2003) |
| encoder | [`ams-as5048`](https://github.com/viam-modules/ams/) |
| movement sensor | [`adxl345`](https://github.com/viam-modules/analog-devices) |
| movement sensor | [`dual-gps-rtk`](https://github.com/viam-modules/gps/) |
| movement sensor | [`gps-nmea-rtk-pmtk`](https://github.com/viam-modules/gps/) |
| movement sensor | [`gps-nmea-rtk-serial`](https://github.com/viam-modules/gps/) |
| movement sensor | [`gps-nmea`](https://github.com/viam-modules/gps/) |
| movement sensor | [`imu-wit`](https://github.com/viam-modules/wit-motion) |
| movement sensor | [`imu-wit-hwt905`](https://github.com/viam-modules/wit-motion) |
| movement sensor | [`mpu6050`](https://github.com/viam-modules/tdk-invensense) |
| power sensor | [`ina219`](https://github.com/viam-modules/texas-instruments) |
| power sensor | [`ina226`](https://github.com/viam-modules/texas-instruments) |
| sensor | [`bme280`](https://github.com/viam-modules/bosch) |
| sensor | [`sensirion-sht3xd`](https://github.com/viam-modules/sensirion) |
| sensor | [`pi`](https://github.com/viam-modules/raspberry-pi) |
| ML model | [`TFLite CPU`](https://app.viam.com/module/viam/tflite_cpu) |

The following models were removed:

<!-- prettier-ignore -->
| Resource | Model |
| -------- | ----- |
| gripper | `softrobotics` |
| motor | `encoded-motor` |
| motor | `gpiostepper` |
| motor | `roboclaw` |
| sensor | `ds18b20` |

{{% /changelog %}}

{{% changelog date="2024-11-05" color="added" title="MoveThroughJointPositions to arm interface" %}}
The [arm interface](/dev/reference/apis/components/arm/) now includes a [MoveThroughJointPositions](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm) method that moves an arm through an ordered array of joint positions.
{{% /changelog %}}

{{% changelog date="2024-10-16" color="added" title="Set data retention policies" %}}

You can now set how long data collected by a component should remain stored in the Viam Cloud in the component's data capture configuration.
For more information, see [Data management service](/data-ai/capture-data/capture-sync/).

{{% /changelog %}}

{{% changelog date="2024-09-20" color="added" title="Pi models moved to module" %}}

The Raspberry Pi 4, 3, and Zero 2 W boards are now supported by [`viam:raspberry-pi:rpi`](https://github.com/viam-modules/raspberry-pi).

{{% /changelog %}}

{{% changelog date="2024-08-26" color="added" title="ESP32 cameras" %}}

`viam-micro-server` now supports cameras on ESP32s.
For more information, see [Configure an esp32-camera](/operate/reference/components/camera/esp32-camera/).

{{% /changelog %}}

{{% changelog date="2024-08-26" color="changed" title="Micro-RDK now called viam-micro-server" %}}

The lightweight version of `viam-server` that is built from the micro-RDK is now referred to as `viam-micro-server`.
For more information, see [viam-micro-server](/operate/reference/viam-micro-server/).

{{% /changelog %}}

{{% changelog date="2024-08-26" color="added" title="Provisioning" %}}

You can now configure provisioning for machines with the Viam Agent.
For more information, see [Configure provisioning with viam-agent](/manage/fleet/provision/setup/).

{{% /changelog %}}

{{% changelog date="2024-08-16" color="added" title="Data capture for vision" %}}

Data capture is now possible for the vision service.
For more information, see [Supported components and services](/data-ai/capture-data/capture-sync/#supported-resources).

{{% /changelog %}}

{{% changelog date="2024-08-01" color="added" title="Create custom training scripts" %}}

You can now upload custom training scripts to the Viam Registry and use them to train machine learning models.
For more information, see [Create custom training scripts](/data-ai/ai/train/).

{{% /changelog %}}

{{% changelog date="2024-07-19" color="changed" title="Operators can now view data" %}}

The operator role now has view permissions for the data in the respective resource a user has access to.
For more information, see [Data and machine learning permissions](/manage/manage/rbac/#data-and-machine-learning).

{{% /changelog %}}

{{% changelog date="2024-06-14" color="changed" title="Python get_robot_part_logs parameters" %}}

The `errors_only` parameter has been removed from [`get_robot_part_logs()`](/dev/reference/apis/fleet/#getrobotpartlogs) and replaced with `log_levels`.

{{% /changelog %}}

{{% changelog date="2024-05-28" color="changed" title="Return type of analog Read" %}}

The board analog API [`Read()`](/dev/reference/apis/components/board/#readanalogreader) method now returns an `AnalogValue` struct instead of a single int.
The struct contains an int representing the value of the reading, min and max range of values, and the precision of the reading.

{{% /changelog %}}

{{% changelog date="2024-05-28" color="added" title="CaptureAllFromCamera and GetProperties to vision API" %}}

The vision service now supports two new methods: [`CaptureAllFromCamera`](/dev/reference/apis/services/vision/#captureallfromcamera) and [`GetProperties`](/dev/reference/apis/services/vision/#getproperties).

{{% /changelog %}}

{{% changelog date="2024-05-14" color="changed" title="Renamed GeoObstacle to GeoGeometry" %}}

The motion service API parameter `GeoObstacle` has been renamed to `GeoGeometry`.
This affects users of the [`MoveOnGlobe()`](/dev/reference/apis/services/motion/#moveonglobe) method.

{{% /changelog %}}

{{< changelog date="2024-05-09" color="changed" title="Return type of GetImage" >}}

The Python SDK introduced a new image container class called [`ViamImage`](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.ViamImage).
The camera component's [`GetImage()`](/dev/reference/apis/components/camera/#getimage) method now returns a `ViamImage` type, and the vision service's [`GetDetections()`](/dev/reference/apis/services/vision/#getdetections) and [`GetClassifications()`](/dev/reference/apis/services/vision/#getclassifications) methods take in `ViamImage` as a parameter.

You can use the helper functions `viam_to_pil_image` and `pil_to_viam_image` provided by the Python SDK to convert the `ViamImage` into a [`PIL Image`](https://omz-software.com/pythonista/docs/ios/Image.html) and vice versa.

{{< expand "Click for an example of using the ViamImage -> PIL Image helper functions." >}}

```python {class="line-numbers linkable-line-numbers"}
from viam.media.utils.pil import pil_to_viam_image, viam_to_pil_image

# Get the ViamImage from your camera.
frame = await my_camera.get_image()

# Convert "frame" to a PIL Image representation.
pil_frame = viam_to_pil_image(frame)

# Use methods from the PIL Image class to get size.
x, y = pil_frame.size[0], pil_frame.size[1]
# Crop image to get only the left two fifths of the original image.
cropped_pil_frame = pil_frame.crop((0, 0, x / 2.5, y))

# Convert back to ViamImage.
cropped_frame = pil_to_viam_image(cropped_pil_frame)

# Get detections from your vision service.
detections = await detector.get_detections(cropped_frame)
```

{{< /expand >}}
{{< /changelog >}}

{{% changelog date="2024-05-08" color="removed" title="WriteAnalog from Go SDK" %}}

The `WriteAnalog()` method has been removed from the Go SDK.
Use [`AnalogByName()`](/dev/reference/apis/components/board/#analogbyname) followed by [`Write()`](/dev/reference/apis/components/board/#writeanalog) instead.

{{% /changelog %}}

{{% changelog date="2024-04-30" color="changed" title="Python SDK data retrieval behavior" %}}

[`tabular_data_by_filter()`](/dev/reference/apis/data-client/#tabulardatabyfilter) and [`binary_data_by_filter()`](/dev/reference/apis/data-client/#binarydatabyfilter) now return paginated data.

{{% /changelog %}}

{{% changelog date="2024-04-30" color="changed" title="Renamed AnalogReader to Analog" %}}

`AnalogReader` has been renamed to `Analog`.
The functionality remains the same, but code that uses analogs must be updated.
`AnalogReaderByName()` and `AnalogReaderNames()` have become [`AnalogByName()`](/dev/reference/apis/components/board/#analogbyname) and `AnalogNames()` (since deprecated), respectively.

{{% /changelog %}}

{{% changelog date="2024-04-30" color="added" title="Part online and part offline triggers" %}}

You can now configure [triggers](/manage/troubleshoot/alert/) to execute actions when a {{< glossary_tooltip term_id="part" text="machine part" >}} comes online or goes offline.

{{% /changelog %}}

{{% changelog date="2024-04-30" color="removed" title="Status from Board API" %}}

Viam has removed support for the following board API methods: `Status()`, `AnalogStatus()`, `DigitalInterruptStatus()`, `Close()`, `Tick()`, `AddCallback()`, and `RemoveCallback()`.

{{% /changelog %}}

{{% changelog date="2024-04-19" color="removed" title="Removed and replaced camera models" %}}

Viam has removed support for following builtin camera models: `single_stream`, `dual_stream`, `align_color_depth_extrinsics`, and `align_color_depth_homography`.

{{% /changelog %}}

{{% changelog date="2024-04-17" color="changed" title="Updated GetCloudMetadata response" %}}

In addition to the existing returned metadata, the [`GetCloudMetadata`](/dev/reference/apis/robot/#getcloudmetadata) method now returns `machine_id` and `machine_part_id` as well.

{{% /changelog %}}

{{% changelog date="2024-04-16" color="improved" title="Viam app interface" %}}

the [Viam app](https://app.viam.com) machine page UI has been updated significantly.
In addition to other improvements, your component, service, and other resource config cards are all displayed on one page instead of in separate tabs.

{{% /changelog %}}

{{% changelog date="2024-03-01" color="added" title="Additional ML models" %}}

Viam has added support for the TensorFlow, PyTorch, and ONNX ML model frameworks, expanding upon the existing support for TensorFlow Lite models.
You can now upload your own ML model(/data-ai/ai/deploy/#deploy-your-ml-model) using any of these frameworks for use with the Vision service.

{{% /changelog %}}

{{% changelog date="2024-03-01" color="added" title="Ultrasonic sensor for `viam-micro-server`" %}}

You can now use the [ultrasonic sensor component](/operate/reference/components/sensor/ultrasonic-micro-rdk/) with [`viam-micro-server`](/operate/reference/viam-micro-server/) to integrate an [HC-S204](https://www.sparkfun.com/products/15569) ultrasonic distance sensor into a machine running `viam-micro-server`.

{{% /changelog %}}

{{% changelog date="2024-03-01" color="added" title="Edit a machine configuration that uses a fragment" %}}

You can now edit the configuration of an existing machine that has been configured with a fragment by using [the `fragment_mods` object](/manage/fleet/reuse-configuration/#modify-fragment-settings-on-a-machine) in your configuration.
You can use the `fragment_mods` objects to be able to deploy a fragment to a fleet of machines, but still be able to make additional per-machine edits as needed.

{{% /changelog %}}

{{% changelog date="2024-03-01" color="added" title="Dual GPS movement sensor" %}}

You can now use the [dual GPS movement sensor component](https://github.com/viam-modules/gps) to integrate a movement sensor that employs two GPS sensors into your machine.
The dual GPS movement sensor calculates a compass heading from both GPS sensors, and returns the midpoint position between the two sensors as its position.

{{% /changelog %}}

{{% changelog date="2024-03-01" color="added" title="Viam Agent" %}}

You can now use the [Viam Agent](/manage/reference/viam-agent/) to provision your machine or fleet of machines during deployment.
The Viam Agent is a software provisioning manager that you can install on your machine which manages your `viam-server` installation, including installation and ongoing updates, as well as providing flexible deployment configuration options, such as pre-configured WiFi network credentials.

{{% /changelog %}}

{{% changelog date="2024-02-12" color="added" title="Generic service" %}}

You can now use the [generic service](/operate/reference/components/generic/) to define new, unique types of services that do not already have an [appropriate API](/dev/reference/apis/#service-apis) defined for them.

{{% /changelog %}}

{{% changelog date="2024-02-12" color="added" title="ML models in the registry" %}}

You can now upload [machine learning (ML) models](/data-ai/ai/deploy/#deploy-your-ml-model) to the Viam Registry, in addition to modules.
You may upload models you have trained yourself using the Viam app, or models you have trained outside of the App.
When uploading, you have the option to make your model available to the general public for reuse.

{{% /changelog %}}

{{% changelog date="2024-01-31" color="added" title="Sensor-controlled base" %}}

Viam has added a [sensor-controlled base](/operate/reference/components/base/sensor-controlled/) component model, which supports a robotic base that receives feedback control from a movement sensor.

{{% /changelog %}}

{{% changelog date="2024-01-31" color="added" title="Visualize captured data" %}}

You can now [visualize your data](/data-ai/data/visualize/) using many popular third-party visualization tools, including Grafana, Tableau, Google’s Looker Studio, and more.
You can visualize any data, such as sensor readings, that you have [synced](/data-ai/capture-data/capture-sync/) to the Viam app from your machine.

See [Visualize data with Grafana](/tutorials/services/visualize-data-grafana/) for a full walkthrough focused on Grafana specifically.

{{% /changelog %}}

{{% changelog date="2024-01-31" color="added" title="Use triggers to trigger actions" %}}

You can now configure [triggers](/data-ai/data/advanced/alert-data/) (previously called webhooks) to execute actions when certain types of data are sent from your machine to the cloud.

{{% /changelog %}}

{{% changelog date="2023-12-31" color="added" title="Filtered camera module" %}}

Viam has added a [`filtered-camera` module](https://app.viam.com/module/erh/filtered-camera) that selectively captures and syncs only the images that match the detections of an ML model.
For example, you could train an ML model that is focused on sports cars, and only capture images from the camera feed when a sports car is detected in the frame.

Check out [this guide](/data-ai/capture-data/filter-before-sync/) for more information.

{{% /changelog %}}

{{% changelog date="2023-12-31" color="added" title="Raspberry Pi 5 Support" %}}

You can now run `viam-server` on a [Raspberry Pi 5](/operate/reference/components/board/pi5/) with the new board model [`pi5`](/operate/reference/components/board/pi5/).

{{% /changelog %}}

{{% changelog date="2023-12-31" color="added" title="Role-based access control" %}}

Users can now have [access to different fleet management capabilities](/manage/manage/rbac/) depending on whether they are an owner or an operator of a given organization, location, or machine.

{{% /changelog %}}

{{% changelog date="2023-11-30" color="added" title="Authenticate with location API key" %}}

You can now use [API keys for authentication](/dev/tools/cli/#authenticate).
API keys allow you to assign the minimum required permissions for usage.
Location secrets, the previous method of authentication, is deprecated and will be removed in a future release.

{{% /changelog %}}

{{% changelog date="2023-11-30" color="added" title="Queryable sensor data" %}}

Once you have added the data management service and synced data, such as sensor readings, to the Viam app, you can now run queries against both captured data as well as its metadata using either SQL or MQL.

For more information, see [Query Data with SQL or MQL](/data-ai/data/query/).

{{% /changelog %}}

{{% changelog date="2023-11-30" color="changed" title="Model training from datasets" %}}

To make it easier to iterate while training machine learning models from image data, you now train models from [datasets](/data-ai/ai/create-dataset/).

{{% /changelog %}}

{{% changelog date="2023-11-30" color="improved" title="Manage users access" %}}

You can now manage users access to machines, locations, and organizations.
For more information, see [Access Control](/manage/manage/rbac/)

{{% /changelog %}}

{{% changelog date="2023-10-31" color="added" title="Test an ML model in browser" %}}

After you upload and train a machine learning model, you can test its results in the **Data** tab.

This allows you to refine models by iteratively tagging more images for training based on observed performance.

For more information, see [Test classification models with existing images in the cloud](/services/vision/mlmodel/#existing-images-in-the-cloud).

To use this update, the classifier must have been trained or uploaded after September 19, 2023.
The current version of this feature exclusively supports classification models.

{{% /changelog %}}

{{% changelog date="2023-10-31" color="added" title="PLC support" %}}

The Viam platform now supports the [Revolution Pi line of PLCs](https://revolutionpi.com/) from KUNBUS in the form of a [module](https://app.viam.com/module/viam-labs/viam-revolution-pi).
This collaboration allows you to leverage the Raspberry Pi-based Revolution Pi, which runs on Linux and has a [specially designed I/O modules](https://www.raspberrypi.com/products/compute-module-4/?variant=raspberry-pi-cm4001000) for streamlined interaction with industrial controls, eliminating the need for additional components.

Read the [Viam PLC Support](https://www.viam.com/post/viam-plc-support-democratizing-access-to-smart-ot-and-ics) blog post for a step-by-step guide on using a PLC with Viam.

{{% /changelog %}}

{{% changelog date="2023-10-31" color="improved" title="SLAM map creation" %}}

The [Cartographer-module](/operate/reference/services/slam/cartographer/) now runs in Viam's cloud for creating or updating maps.
This enhancement allows you to:

- Generate larger maps without encountering session timeouts
- Provide IMU input to improve map quality
- Save maps to the **SLAM library**
- Create or update maps using previously captured LiDAR and IMU data
- Deploy maps to machines

{{% /changelog %}}

{{% changelog date="2023-09-30" color="added" title="Modular registry" %}}

The [Modular Registry](https://app.viam.com/registry/) enables you to use, create, and share custom modules, extending the capabilities of Viam beyond the components and services that are natively supported.

You can:

- Publish modules on the registry
- Add modules to any machine's configuration with a few clicks
- Select the desired module version for deployment, make changes at your convenience, and deploy the updates to a single machine or an entire fleet.

{{% /changelog %}}

{{% changelog date="2023-09-30" color="added" title="Mobile app" %}}

You can use a [mobile application](/manage/troubleshoot/teleoperate/default-interface/#viam-mobile-app), available for download now in the [Apple](https://apps.apple.com/us/app/viam-robotics/id6451424162) and [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US) app stores, to connect to and control your Viam-powered machines directly from your mobile device.

{{% /changelog %}}

{{% changelog date="2023-09-30" color="added" title="Power sensor component" %}}

You now have the capability to use a [power sensor component](/operate/reference/components/power-sensor/) to monitor the voltage, current, and power consumption within your machine's system.

{{% /changelog %}}

{{% changelog date="2023-09-30" color="added" title="Filter component’s data before the cloud" %}}
Viam has written a module that allows you to filter data based on specific criteria before syncing it to [Viam's cloud](/data-ai/capture-data/capture-sync/).
It equips machines to:

- Remove data that is not of interest
- Facilitate high-interval captures while saving data based on your defined metrics
- Prevent the upload of unnecessary data

To learn more, see [this tutorial](/tutorials/configure/pet-photographer/) on creating and configuring a data filtration module.

{{% /changelog %}}

{{% changelog date="2023-08-31" color="added" title="Configure a custom Linux board" %}}

You can now use boards like the [Mediatek Genio 500 Pumpkin](https://ologicinc.com/portfolio/mediateki500/) that run Linux operating systems with the [`customlinux` board model](https://github.com/viam-modules/customlinux/).

{{% /changelog %}}

{{% changelog date="2023-08-31" color="improved" title="Image inspection for ML training" %}}

This update enables you to get a closer examination of your image and streamline your image annotation experience by making it easier to add bounding boxes and labels in the **Data** tab.

With the latest improvements, you can now:

- Navigate between images using the arrow keys in the main image view
- Expand images for a more detailed inspection by clicking the expand button on the right image panel
- Move between full-screen images effortlessly with the <> arrow buttons or arrow keys
- Return to the standard view by using the escape key or collapse button

{{% /changelog %}}

{{% changelog date="2023-08-31" color="added" title="Duplicate component button" %}}

You now have the ability to duplicate any config component, service, module, remote, or process.

To use this feature:

- Click on the duplicate component icon at the top right of any resource
- Optionally, you can modify the component name to distinguish it
- Adjust any attributes, such as motor pin numbers

{{% /changelog %}}

{{% changelog date="2023-07-31" color="added" title="Apple SSO authentication" %}}

Viam now supports sign-up/log-in through Apple Single Sign-On.

Note that currently, accounts from different SSO providers are treated separately, with no account merging functionality.

{{% /changelog %}}

{{% changelog date="2023-07-31" color="improved" title="Arm component API" %}}

Arm models now support the [`GetKinematics` method](/dev/reference/apis/components/arm/#getkinematics) in the arm API, allowing you to request and receive kinematic information.

{{% /changelog %}}

{{% changelog date="2023-06-30" color="added" title="View sensor data within Viam" %}}

You can now [view your sensor data](https://app.viam.com/data/view?view=sensors) directly in the Viam app to verify data creation and accuracy.
If you depend on sensor data to plan and control machine operations, this feature increases access to data and supports a more efficient workflow.

{{% /changelog %}}

{{% changelog date="2023-06-30" color="added" title="Session management in the Python SDK" %}}

The Python SDK now includes sessions, a safety feature that automatically cancels operations if the client loses connection to your machine.

[Session management](/dev/reference/apis/sessions/) helps you to ensure safer operation of your machine when dealing with actuating controls.
Sessions are enabled by default, with the option to [disable sessions](/dev/reference/apis/sessions/#disable-default-session-management).

{{% /changelog %}}

{{% changelog date="2023-06-30" color="added" title="Connect an ODrive motor controller as a Viam module" %}}

You can integrate and control ODrive motor controllers with Viam using the [`odrive` module from the Viam Registry](https://github.com/viamrobotics/odrive).

See the [Odrive module readme](https://github.com/viamrobotics/odrive) to learn how to connect and use an ODrive motor controller with Viam, and view the sample configurations.

{{% /changelog %}}

{{% changelog date="2023-06-30" color="added" title="Implement custom robotic arms as Viam modules" %}}

When prototyping a robotic arm, you can now facilitate movement without creating your own motion planning.
This update enables you to implement custom models of an arm component as a modular resource by coding three endpoints of the [Arm API](/dev/reference/apis/components/arm/#api):

- `getJointPositions`
- `movetoJointPositions`
- `GetKinematics`

Then, use the [motion planning service](/operate/reference/services/motion/) to specify poses, and Viam handles the rest.

{{% /changelog %}}

{{% changelog date="2023-06-30" color="improved" title="Gantry component" %}}

To better control gantries with Viam, you can now:

- Specify speed values when calling the `MovetoPosition` method on [Gantry components](/operate/reference/components/gantry/).
  This allows you to define the speed at which each axis moves to the desired position, providing enhanced precision and control over the gantry's movement.
- Set a home position for Gantry components to facilitate position resetting or maintain consistent starting points.

{{% /changelog %}}

{{% changelog date="2023-06-30" color="improved" title="Optimized Viam-trained object detection models" %}}

This update for TFlite object detection models [trained with the machine learning service](/data-ai/ai/train-tflite/) brings significant improvements, including:

- 76% faster model inference for camera streams
- 64% quicker model training for object detection
- 46% reduction in compressed model size

{{% /changelog %}}

{{% changelog date="2023-05-31" color="added" title="TypeScript SDK beta release" %}}

The beta release of the [TypeScript SDK](https://github.com/viamrobotics/viam-typescript-sdk/) allows you to create a web interface to work with your machine, as well as create custom components and services.

{{% /changelog %}}

{{% changelog date="2023-05-31" color="added" title="Train object detection ML models" %}}

You now have the capability to directly [train a TFlite object detection models](/data-ai/ai/train-tflite/) in addition to image classification models from within the Viam app.

This update allows you to:

- Add labels by drawing bounding boxes around specific objects in your images or a single image.
- Create a curated subset of data for training by filtering images based on labels or tags.

{{% /changelog %}}

{{% changelog date="2023-05-31" color="added" title="Permissions for organizations in Viam" %}}

Now when you invite collaborators to join your organization, you can assign permissions to members by setting one of these roles:

- **Owner**: These members can see and edit every tab on the machine page, as well as manage users in the app.
  This role is best for those on your team who are actively engineering and building machines.

- **Operator**: These members can only see and use the [remote control tab](/manage/troubleshoot/teleoperate/default-interface/).
  This role is best for those on your team who are teleoperating or remotely controlling machines.

For more information about assigning permissions and collaborating with others on Viam, see [Manage access](/manage/manage/access/).

{{% /changelog %}}

{{% changelog date="2023-05-31" color="improved" title="Control RoboClaw motor controllers with the driver" %}}

When using a RoboClaw motor controller without encoders connected to your motors, you now have more direct control over the RoboClaw’s functionality within Viam or through the motor API.

For example, in the Viam app, you can now set **Go For** values for these motors, utilizing a time-based estimation for the number of revolutions.

{{% /changelog %}}

{{% changelog date="2023-05-31" color="improved" title="Camera webcam names and setting framerates" %}}

The updates to the camera component have improved the process of connecting to and using cameras with your machines.

The latest updates enable you to:

- View readable webcam names in the **video path** of your camera component.
- Specify your preferred framerate by selecting the desired value in the newly added **framerate field** on the **CONFIGURE** tab.

{{% /changelog %}}

{{% changelog date="2023-05-31" color="improved" title="Additions to code samples in the Viam app" %}}

The updated code samples now includes:

- Options for C++ and TypeScript
- The ability to hide or display your machines' [secrets](/dev/reference/apis/)

Access these samples in the **Code sample** tab on your machine's page to connect to your machine in various languages.

{{% /changelog %}}

{{% changelog date="2023-05-31" color="improved" title="Delete data in bulk in the Viam app" %}}

You can manage the data synced to Viam's cloud with the new capability for bulk data deletion on the **Data** tab.

{{% /changelog %}}

{{% changelog date="2023-04-25" color="changed" title="Vision service" %}}

{{% alert title="Important: Breaking Change" color="note" %}}

The [vision service](/operate/reference/services/vision/) became more modular in RDK [v0.2.36](https://github.com/viamrobotics/rdk/releases/tag/v0.2.36), API [v0.1.118](https://github.com/viamrobotics/api/releases/tag/v0.1.118), and Python SDK [v0.2.18](https://github.com/viamrobotics/viam-python-sdk/releases/tag/v0.2.18).

Find more information on each of the changes below.

{{% /alert %}}

<!-- markdownlint-disable MD001 -->

#### Use individual vision service instances

You need to create **an individual vision service instance** for each detector, classifier, and segmenter model.
You can no longer be able to create one vision service and register all of your detectors, classifiers, and segmenters within it.

{{%expand "Click for details on how to migrate your code." %}}

#### API calls

Change your existing API calls to get the new vision service instance for your detector, classifier, or segmenter model directly from the `VisionClient`:

{{< tabs >}}
{{% tab name="New Way" %}}

Change your existing API calls to get the new vision service instance for your detector, classifier, or segmenter model directly from the `VisionClient`:

```python {class="line-numbers linkable-line-numbers"}
my_object_detector = VisionClient.from_robot(robot, "find_objects")
img = await cam.get_image()
detections = await my_object_detector.get_detections(img)
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```python {class="line-numbers linkable-line-numbers"}
vision = VisionServiceClient.from_robot(robot)
img = await cam.get_image()
detections = await vision.get_detections(img, "find_objects")
```

{{% /tab %}}
{{< /tabs >}}

#### Color detector configurations

You can replace existing color detectors by [configuring new ones in the UI](/operate/reference/services/vision/color_detector/) or you can update the JSON configuration of your machines:

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "blue_square",
        "type": "vision",
        "model": "color_detector",
        "attributes": {
            "segment_size_px": 100,
            "detect_color": "#1C4599",
            "hue_tolerance_pct": 0.07,
            "value_cutoff_pct": 0.15
        }
    },
    {
        "name": "green_triangle",
        "type": "vision",
        "model": "color_detector",
        "attributes": {
            "segment_size_px": 200,
            "detect_color": "#62963F",
            "hue_tolerance_pct": 0.05,
            "value_cutoff_pct": 0.20
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "segment_size_px": 100,
                    "detect_color": "#1C4599",
                    "hue_tolerance_pct": 0.07,
                    "value_cutoff_pct": 0.15
                },
                "name": "blue_square",
                "type": "color_detector"
            },
            {
                "parameters": {
                    "segment_size_px": 200,
                    "detect_color": "#62963F",
                    "hue_tolerance_pct": 0.05,
                    "value_cutoff_pct": 0.20
                },
                "name": "green_triangle",
                "type": "color_detector"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### TFLite detector configurations

You can replace existing TFLite detectors by [configuring new ones in the UI](/operate/reference/services/vision/mlmodel/) or you can update the JSON configuration of your machines:

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "person_detector",
        "type": "mlmodel",
        "model": "tflite_cpu",
        "attributes": {
            "model_path": "/path/to/file.tflite",
            "label_path": "/path/to/labels.tflite",
            "num_threads": 1
        }
    },
    {
        "name": "person_detector",
        "type": "vision",
        "model": "mlmodel",
        "attributes": {
            "mlmodel_name": "person_detector"
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "model_path": "/path/to/file.tflite",
                    "label_path": "/path/to/labels.tflite",
                    "num_threads": 1
                },
                "name": "person_detector",
                "type": "tflite_detector"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### TFLite Classifier configurations

You can replace existing TFLite classifiers by [configuring new ones in the UI](/operate/reference/services/vision/mlmodel/) or you can update the JSON configuration of your machines:

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "fruit_classifier",
        "type": "mlmodel",
        "model": "tflite_cpu",
        "attributes": {
            "model_path": "/path/to/classifier_file.tflite",
            "label_path": "/path/to/classifier_labels.txt",
            "num_threads": 1
        }
    },
    {
        "name": "fruit_classifier",
        "type": "vision",
        "model": "mlmodel",
        "attributes": {
            "mlmodel_name": "fruit_classifier"
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "model_path": "/path/to/classifier_file.tflite",
                    "label_path": "/path/to/classifier_labels.txt",
                    "num_threads": 1
                },
                "name": "fruit_classifier",
                "type": "tflite_classifier"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### Radius Clustering 3D segmenter configurations

You can replace existing Radius Clustering 3D segmenters by [configuring new ones in the UI](/operate/reference/services/vision/obstacles_pointcloud/) or you can update the JSON configuration of your machines:

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "rc_segmenter",
        "type": "vision",
        "model": "obstacles_pointcloud"
        "attributes": {
            "min_points_in_plane": 1000,
            "min_points_in_segment": 50,
            "clustering_radius_mm": 3.2,
            "mean_k_filtering": 10
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "min_points_in_plane": 1000,
                    "min_points_in_segment": 50,
                    "clustering_radius_mm": 3.2,
                    "mean_k_filtering": 10
                },
                "name": "rc_segmenter",
                "type": "radius_clustering_segmenter"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}

#### Detector to 3D segmenter configurations

You can replace existing Radius Clustering 3D segmenters by [configuring new ones in the UI](/operate/reference/services/vision/detector_3d_segmenter/) or you can update the JSON configuration of your machines:

{{< tabs >}}
{{% tab name="New Way" %}}

```json
"services": [
    {
        "name": "my_segmenter",
        "type": "vision",
        "model": "detector_3d_segmenter"
        "attributes": {
            "detector_name": "my_detector",
            "confidence_threshold_pct": 0.5,
            "mean_k": 50,
            "sigma": 2.0
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{% tab name="Old Way" %}}

```json
"services": [
    {
        "name": "vision",
        "type": "vision",
        "attributes": {
            "register_models": [
            {
                "parameters": {
                    "detector_name": "my_detector",
                    "confidence_threshold_pct": 0.5,
                    "mean_k": 50,
                    "sigma": 2.0
                },
                "name": "my_segmenter",
                "type": "detector_segmenter"
            }
            ]
        }
    },
    ... // other services
]
```

{{% /tab %}}
{{< /tabs >}}
{{% /expand%}}

#### Add and remove models using the machine config

You must add and remove models using the [machine config](/operate/get-started/supported-hardware/#configure-hardware-on-your-machine).
You will no longer be able to add or remove models using the SDKs.

#### Add machine learning vision models to a vision service

The way to add machine learning vision models is changing.
You will need to first register the machine learning model file with the [ML model service](/data-ai/ai/deploy/) and then add that registered model to a vision service.

{{% /changelog %}}

{{% changelog date="2023-03-31" color="added" title="Machine learning for image classification models" %}}

You can now [train](/data-ai/ai/train-tflite/) and [deploy](/data-ai/ai/deploy/) image classification models with the [data management service](/data-ai/capture-data/capture-sync/) and use your machine's image data directly within Viam.
Additionally, you can upload and use existing [machine learning models](/data-ai/ai/deploy/#deploy-your-ml-model) with your machines.
For more information on using data synced to the cloud to train machine learning models, read [train a TFlite](/data-ai/ai/train-tflite/) or [another model](data-ai/ai/train/).

{{% /changelog %}}

{{% changelog date="2023-03-31" color="added" title="Motion planning with new `constraint` parameter" %}}

A new parameter, [`constraint`](/operate/reference/services/motion/constraints/), has been added to the [Motion service API](/dev/reference/apis/services/motion/#api), allowing you to define restrictions on the machine's movement.
The constraint system also provides flexibility to specify that obstacles should only impact specific frames of a machine.

{{% /changelog %}}

{{% changelog date="2023-03-31" color="added" title="Fragments in machine configuration" %}}

You can now access {{< glossary_tooltip term_id="fragment" text="fragments" >}} in your machine configuration.
The configurations you added will now show up automatically in the **Builder** view on your machine's **CONFIGURE** tab.
This makes it easier to monitor what fragments you've added to your machine and how they're configured.

For more information, see [Fragments](/configure/#fragments).

{{% /changelog %}}

{{% changelog date="2023-03-31" color="improved" title="Sticky GPS keys" %}}

GPS keys you enter are now saved in your local storage.
This ensures that when you reload the page, your GPS keys remain accessible.

{{% /changelog %}}

{{% changelog date="2023-03-31" color="improved" title="More reliable camera streams" %}}

The camera component's streams are smoother and more reliable with recent improvements.

Additionally, camera streams automatically restart if you momentarily lose internet connection.

{{% /changelog %}}

{{% changelog date="2023-03-31" color="improved" title="UI updates to Logs and History" %}}

The latest UI updates enable you to:

- Load a previous configuration for reverting changes made in the past
- Search logs by filtering keywords or log levels such as _info_ or _error_ messages
- Change your timestamp format to **ISO** or **Local** depending on your preference.

{{% /changelog %}}

{{% changelog date="2023-02-28" color="added" title="Rover reuse in Try Viam" %}}

You now have the option to reuse a machine config from a previous Try Viam session.

{{% /changelog %}}

{{% changelog date="2023-02-28" color="added" title="Dynamic code samples" %}}

The Viam app **Code sample** tab now dynamically updates as you add resources to your machine's config.
The code samples instantiate each resource and include examples of how to call a `Get` method on it.

{{% /changelog %}}

{{% changelog date="2023-02-28" color="added" title="TypeScript SDK" %}}

Find more information in the [TypeScript SDK docs](https://ts.viam.dev/).

{{% /changelog %}}

{{% changelog date="2023-02-28" color="added" title="Frame system visualizer" %}}

When adding [frames](/operate/mobility/define-geometry/) to your machine's config in the Viam app, you can now use the **Frame System** subtab of the **CONFIGURE** tab to more easily visualize the relative positions of frames.

{{% /changelog %}}

{{% changelog date="2023-02-28" color="added" title="Support for microcontrollers" %}}

`viam-micro-server` is a lightweight version of `viam-server` that can run on an ESP32.
Find more information in the [`viam-micro-server` docs](/operate/reference/viam-micro-server/).

{{% /changelog %}}

{{% changelog date="2023-01-31" color="added" title="Remote control power input" %}}

On your machine's **CONTROL** tab on the [Viam app](https://app.viam.com/), you can now set the power of a [base](/operate/reference/components/base/).
The base control UI previously always sent 100% power to the base's motors.

{{% /changelog %}}

{{% changelog date="2023-01-31" color="added" title="New encoder model: AMS AS5048" %}}

The [AMS AS5048](https://github.com/viam-modules/ams) is now supported.

{{% /changelog %}}

{{% changelog date="2023-01-31" color="added" title="GetLinearAcceleration method" %}}

The movement sensor API now includes a [GetLinearAcceleration](/dev/reference/apis/components/movement-sensor/#getlinearacceleration) method.

{{% /changelog %}}

{{% changelog date="2023-01-31" color="added" title="Support for capsule geometry" %}}

The [motion service](/operate/reference/services/motion/) now supports capsule geometries.

The UR5 arm model has been improved using this new geometry type.

{{% /changelog %}}

{{% changelog date="2022-12-28" color="added" title="Modular resources" %}}

You can now implement your own custom {{< glossary_tooltip term_id="resource" text="resources" >}} as [_modular resources_ in the registry](https://app.viam.com/registry/).

{{% alert title="Important: Breaking Change" color="note" %}}

All users need to update to the latest version of the RDK (V3.0.0) to access machines using the Viam app.

{{% /alert %}}

{{% /changelog %}}

{{% changelog date="2022-12-28" color="added" title="URDF kinematic file support" %}}

You can now supply kinematic information using URDF files when implementing your own arm models.

{{% /changelog %}}

{{% changelog date="2022-12-28" color="added" title="New movement sensor models" %}}

There are two new movement sensor {{< glossary_tooltip term_id="model" text="models" >}}:

- [ADXL345](https://github.com/viam-modules/analog-devices): A 3-axis accelerometer
- [MPU-6050](https://github.com/viam-modules/tdk-invensense): A 6-axis accelerometer and gyroscope

{{% /changelog %}}

{{% changelog date="2022-12-28" color="improved" title="Camera performance and reliability" %}}

- Improved server-side logic to choose a mime type based on the camera image type, unless a specified mime type is supplied in the request.
  **The default mime type for color cameras is now JPEG**, which improves the streaming rate across every SDK.
- Added discoverability when a camera reconnects without changing video paths.
  This now triggers the camera discovery process, where previously users would need to manually restart the RDK to reconnect to the camera.

{{% /changelog %}}

{{% changelog date="2022-12-28" color="improved" title="Motion planning with remote components" %}}

The [motion service](/operate/reference/services/motion/) is now agnostic to the networking topology of a machine.

- Kinematic information is now transferred over the robot API.
  This means that the motion service is able to get kinematic information for every component on the machine, regardless of whether it is on a main or remote viam-server.
- Arms are now an input to the motion service.
  This means that the motion service can plan for a machine that has an arm component regardless of whether the arm is connected to a main or {{< glossary_tooltip term_id="remote-part" text="remote-part" >}} instance of `viam-server`.

{{% /changelog %}}

{{% changelog date="2022-12-28" color="improved" title="Motion planning path smoothing" %}}

- RRT\* paths now undergo rudimentary smoothing, resulting in improvements to path quality with negligible change to planning performance.
- Plan manager now performs direct interpolation for any solution within some factor of the best score, instead of only in the case where the best inverse kinematics solution could be interpolated.

{{% /changelog %}}

{{% changelog date="2022-12-28" color="improved" title="Data synchronization reliability" %}}

Previously, data synchronization used bidirectional streaming.
Now is uses a simpler unary approach that is more performant on batched unary calls, is easier to load balance, and maintains ordered captures.

{{% /changelog %}}

{{% changelog date="2022-11-28" color="changed" title="Camera configuration" %}}

**Changed** the configuration schemes for the following camera models:

- Webcam
- FFmpeg
- Transform
- Join pointclouds

For information on configuring any camera model, see [Camera Component](/operate/reference/components/camera/).

{{% /changelog %}}

{{% changelog date="2022-11-15" color="added" title="New servo model" %}}

A new [servo model called `gpio`](/operate/reference/components/servo/gpio/) supports servos connected to non-Raspberry Pi boards.

{{% /changelog %}}

{{% changelog date="2022-11-15" color="added" title="RTT indicator in the app" %}}

A badge in the Viam app now displays RTT (round trip time) of a request from your client to the machine.
Find this indicator of the time to complete one request/response cycle on your machine's **CONTROL** tab, in the **Operations & Sessions** card.

{{% /changelog %}}

{{% changelog date="2022-11-15" color="added" title="Python 3.8 support" %}}

The Python SDK now supports Python 3.8, in addition to 3.9 and 3.10.

{{% /changelog %}}

{{% changelog date="2022-11-15" color="added" title="New parameter: `extra`" %}}

A new API method parameter, `extra`, allows you to extend {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} functionality by implementing the new field according to whatever logic you choose.
`extra` has been added to the following APIs: arm, data management, gripper, input controller, motion, movement sensor, navigation, pose tracker, sensor, SLAM, vision.

{{% alert title="IMPORTANT: Breaking change" color="note" %}}

Users of the Go SDK _must_ update code to specify `extra` in the arguments that pass into each request.

`extra` is an optional parameter in the Python SDK.

{{% /alert %}}

{{% /changelog %}}

{{% changelog date="2022-11-15" color="added" title="Service dependencies" %}}

`viam-server` now initializes and configures resources in the correct order.
For example, if the SLAM service depends on a LiDAR, it will always initialize the LiDAR before the SLAM service.

{{% alert title="IMPORTANT: Breaking change" color="note" %}}

If you are using the SLAM service, you now need to specify sensors used by the SLAM service in the `depends_on` field of the SLAM configuration.
Other service configurations are not affected.

{{% /alert %}}

{{% /changelog %}}

{{% changelog date="2022-11-15" color="removed" title="Width and height fields from camera API" %}}

Removed `width` and `height` from the response of the [`GetImage`](/dev/reference/apis/components/camera/#getimage) method in the camera API.
This does not impact any existing camera models.
If you write a custom camera model, you no longer need to implement the `width` and `height` fields.

{{% /changelog %}}
