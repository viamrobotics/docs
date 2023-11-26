---
title: "Pet Photographer: Create a Data Filtering Module"
linkTitle: "Pet Photographer"
type: "docs"
description: "Use the filter modular component in the Viam app to photograph your pet in their collar."
tags: ["vision", "filter", "camera", "detector", "services"]
image: "/tutorials/pet-photographer/data-capture.png"
imageAlt: "Filtered data from the custom colorfiltercam in the Data tab showing only photos of a dog wearing a blue collar"
images: ["/tutorials/pet-photographer/data-capture.png"]
authors: ["Sky Leilani"]
languages: ["go", "python"]
viamresources: ["vision", "camera"]
images: ["/tutorials/pet-photographer/data-capture.png"]
image: "/tutorials/pet-photographer/data-capture.png"
imageAlt: "Filtered data tab contents from colorfiltercam showing only photos of dog with blue collar"
level: "Intermediate"
date: "2023-09-17"
# updated: ""
cost: "0"
no_list: true
weight: 3
---

If your smart machine [captures](/services/data/#data-capture) a lot of data, you might want to filter captured data to selectively store only the data you are interested in.
For example, you might want to use your smart machine's camera to capture images based on specific criteria, such as the presence of a certain color, and omit captured images that don't meet that criteria.

In this tutorial, you will use a custom {{< glossary_tooltip term_id="module" text="module" >}} to function as a color filter, and use it with a [camera](/components/camera/) to only capture images where your pet is in the frame in the following way:

1. Attach a colored object, such as a blue collar, to your pet.
1. Set up a camera in an area where your pet is likely to appear in the frame, and configure the data management service to capture and sync images from that camera.
1. Configure the `colorfilter` custom module to filter captured images from your camera, saving them only when your pet, along with their easily-identifiable colored object, is present in the frame.

   {{<imgproc src="/tutorials/pet-photographer/data-example.png" resize="550x" declaredimensions=true alt="Dog in blue collar in the camera's live feed">}}

The source code for this module is available on the [`modular-filter-examples` GitHub repository](https://github.com/viam-labs/modular-filter-examples) .
In addition to the `colorfilter` module used in this tutorial, the example repository also includes a [sensor reading filter](https://github.com/viam-labs/modular-filter-examples/tree/main/sensorfilter) which you could use to control and filter the data recorded by a [sensor component](/components/sensor/).

## Hardware requirements

To create your own filtering pet photographer robot, you'll need the following hardware:

- A computer
- A [webcam](/components/camera/webcam/) or other type of [camera](/components/camera/)
- A colored object, such as a blue collar for enhanced accuracy _(optional)_

{{< alert title="Tip" color="tip" >}}
In this tutorial, the camera is configured to identify and filter images with the color blue, as it is less common in many environments.
If your pet already has a distinct color that is different from their environment, you can also configure your camera to use that color to identify pictures of your pet.
{{< /alert >}}

## Set up

Follow the steps below to set up your smart machine:

1. Install [Go](https://go.dev/dl/) or [Python](https://www.python.org/downloads/) on both your local development computer and on your robot's board if they are not the same device.
1. [Create a robot](https://docs.viam.com/manage/fleet/robots/#add-a-new-robot).
1. [Install](/installation/#install-viam-server) or [update](/installation/manage/#update-viam-server) `viam-server`.
   Your `viam-server` must be [version 0.8.0](https://github.com/viamrobotics/rdk/releases/tag/v0.8.0-rc0) or newer, as filtering capabilities were introduced in the RDK starting from that version.

## Add the custom module

In this tutorial, you can choose to add custom data filtering to your robot in one of two ways:

1. [Download the `colorfilter` module](#download-the-colorfilter-module) from Viam and get started quickly.
1. [Code your own color filtering module](#code-your-own-module), exploring the process of building a module from scratch.

### Download the colorfilter module

Follow the instructions below to download the `colorfilter` module in your preferred programming language:

{{< tabs >}}
{{% tab name="Python"%}}

1. Clone the [`colorfilter` module](https://github.com/viam-labs/modular-filter-examples) from GitHub onto your computer:

   ```{class="command-line" data-prompt="$"}
   git clone https://github.com/viam-labs/modular-filter-examples.git
   ```

1. Navigate to the Python color filter directory, `pycolorfilter`.
1. Note the path to your module's executable, <file>run.sh</file>, for later use.
1. [Add the `colorfilter` module to your smart machine as a local module](#add-as-a-local-module) and continue the tutorial from there.

{{% /tab %}}
{{% tab name="Go"%}}

1. Clone the [`colorfilter` module](https://github.com/viam-labs/modular-filter-examples) from GitHub onto your robot's computer:

   ```{class="command-line" data-prompt="$"}
   git clone https://github.com/viam-labs/modular-filter-examples.git
   ```

1. Navigate to the Go color filter directory, `colorfilter`.
1. Inside of the `module` directory, [compile the executable](/registry/create/#prepare-the-module-for-execution) that runs your module.
1. Save the path to your module's executable for later use.
1. [Add the `colorfilter` module to your smart machine as a local module](#add-as-a-local-module) and continue the tutorial from there.

{{% /tab %}}
{{< /tabs >}}

### Code your own module

To code your own color filtering module, first create the necessary files and directories on your smart machine:

{{< tabs >}}
{{% tab name="Python"%}}

1. Create a folder for your module with the name of your model `colorfilter`.
   - Your model name must use all lowercase letters.
1. Inside that folder, create a file called <file>color_filter.py</file>.

{{% /tab %}}
{{% tab name="Go"%}}

1. Create a folder for your module with the name of your model `colorfilter`.
   - Your model name must use all lowercase letters.
1. Inside that folder, create:
   - A file called <file>color_filter.go</file>.
   - A directory named `module`.

{{% /tab %}}
{{< /tabs >}}

#### Code a filter resource model

Next, include all the methods that the corresponding Viam SDK requires in the API definition of its built-in {{< glossary_tooltip term_id="subtype" text="subtype" >}}.

{{< tabs >}}
{{% tab name="Python"%}}
You can write your own code or copy the code from the `colorfilter` module's <file>[color_filter.py](https://github.com/viam-labs/modular-filter-examples/blob/main/pycolorfilter/color_filter.py)</file> file.

To write your own code, implement a client interface defined by the required methods outlined in the <file>client.py</file> file for the specific resource you are implementing.
For example, the camera's <file>client.py</file> file is located at <file>[/components/camera/client.py](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/camera/client.py)</file>.

1. Open the <file>color_filter.py</file> file you just created and implement the required methods from <file>client.py</file>.
   - Exclude the `get_images` method, which you will customize to add filtering functionality in the upcoming section.
   - Include the other methods within the class corresponding to your resource type (in this case, the `CameraClient` class).

For more information, refer to [Create a custom module](/registry/create/#create-a-custom-module).

{{% /tab %}}
{{% tab name="Go"%}}

To write your own code, implement a client interface defined by the required methods outlined in the <file>client.go</file> file for the specific resource you are implementing.
For example, the camera's <file>client.go</file> file is located at <file>[/components/camera/client.go](https://github.com/viamrobotics/rdk/blob/main/components/camera/client.go)</file>.

1. Open the <file>color_filter.go</file> file you just created and implement the required methods in it.
   Exclude the `Read` method, which you will replace with a method, `Next`, to add filtering functionality in the upcoming section.
   - You can create your own code or copy the code from the [viam-labs `colorfilter` repository's <file>color_filter.go</file>](https://github.com/viam-labs/modular-filter-examples/blob/main/colorfilter/color_filter.go) file.

For more information, refer to [Create a custom module](/registry/create/#create-a-custom-module).

{{% /tab %}}
{{< /tabs >}}

The filter function in your custom filter module must contain two critical elements:

1. A utility function that will check if the caller of the filter function is the [data management](/services/data/) service.
1. A safeguard that ensures if the data management service is not the caller, an error and the unfiltered data is returned.

{{< alert title="Important" color="note" >}}
You must include both the safeguard and utility functions in order to access data filtering functionality within your module.

For programming languages other than Python and Go, the API of the component you're receiving data from will provide comparable utility functions and safeguards.
These tools help you to check the caller of your filter function and ensure your smart machine responds accordingly.

For detailed information, please refer to the documentation for your chosen SDK.
{{< /alert >}}

Follow the steps below to include the utility function and check whether the data management service is the caller of the function responsible for data capture.
If a service other than the data management service calls the function, it will return the original, unfiltered data.

To check the caller of the collector function using the utility function:

{{< tabs >}}
{{% tab name="Python"%}}
First, import `from_dm_from_extra`:

```python {class="line-numbers linkable-line-numbers"}
from viam.utils import from_dm_from_extra
```

Then, include it in the conditional statement in your filter function:

```python {class="line-numbers linkable-line-numbers"}
if from_dm_from_extra(extra):
    detections = await self.vision_service.get_detections(img)
```

With this configuration:

- Your camera checks if the data management service is the caller of the filter function by using `from_dm_from_extra`.

{{% /tab %}}
{{% tab name="Go"%}}

Write a conditional statement that checks `FromDMContextKey`:

{{< alert title="Important" color="note" >}}
Use `FromDMContextKey` to check the caller of the data capture function when working with a modular _camera_ using the Go SDK.
For all other components, you should use `FromDMString` instead.
See the [sensor filter example](https://github.com/viam-labs/modular-filter-examples/blob/main/sensorfilter/sensor_filter.go) for example code to support working with a sensor.
{{< /alert >}}

```go {class="line-numbers linkable-line-numbers"}
if ctx.Value(data.FromDMContextKey{}) != true {
   // If not data management collector, return underlying stream contents without filtering.
   return fs.cameraStream.Next(ctx)
}

// Only return captured image if it contains a certain color set by the vision service.
img, release, err := fs.cameraStream.Next(ctx)

detections, err := fs.visionService.Detections(ctx, img, map[string]interface{}{})
```

With this configuration:

- Your camera checks if the data management service is the caller of the filter function by using `FromDMContextKey`.
- If `FromDMContextKey` is `true` and the data management service is the caller, the camera captures an image by declaring the `img` variable and filling it with the content from the camera stream.
- Then, after capturing the image, the code requests the next detection.

{{% /tab %}}
{{< /tabs >}}

After implementing a check to identify the initiator of the filter function, you must include the safeguard that will return an error if the data management service is not the caller.

To do this, include the following in your filter module's resource model:

{{< tabs name="Example tabs">}}
{{% tab name="Python"%}}

Edit <file>color_filter.py</file> and import the safeguard error `NoCaptureToStoreError` from Viam:

```python {class="line-numbers linkable-line-numbers"}
from viam.errors import NoCaptureToStoreError
```

Then, edit the `if from_dm_from_extra(extra)` conditional statement from earlier to add a second conditional statement within it that returns the error when the data management service is not the caller:

```python {class="line-numbers linkable-line-numbers"}
if from_dm_from_extra(extra):
    detections = await self.vision_service.get_detections(img)
    if len(detections) == 0:
        raise NoCaptureToStoreError()
```

This code:

- Checks the length (`len`) of the `detections` variable.
- Raises a `NoCaptureToStoreError()` if `len` is equal to `0` to signify that the data management service is not the caller.

{{% /tab %}}
{{% tab name="Go"%}}

Open <file>color_filter.go</file> and write a conditional statement inside of your filter function that includes the error message `data.ErrNoCaptureToStore`:

```go {class="line-numbers linkable-line-numbers"}
if len(detections) == 0 {
   return nil, nil, data.ErrNoCaptureToStore
}
```

This code:

- Checks the length (`len`) of the `detections` variable.
- Raises a `data.ErrNoCaptureToStore` error if `len` is equal to `0` to signify that the data management service is not the caller.

{{% /tab %}}
{{< /tabs >}}

Now that you've included the required utility function and safeguard, your complete color filter function should look like the following:

{{< tabs >}}
{{% tab name="Python"%}}

```python {class="line-numbers linkable-line-numbers"}
async def get_image(
  self,
  mime_type: str = "",
  *,
  extra: Optional[Dict[str, Any]] = None,
  timeout: Optional[float] = None,
  **kwargs
  ) -> Image.Image:
    """Filters the output of the underlying camera"""
    img = await self.actual_cam.get_image()
    if from_dm_from_extra(extra):
        detections = await self.vision_service.get_detections(img)
        if len(detections) == 0:
            raise NoCaptureToStoreError()

    return img
```

If the data management service is the caller, the filter function requests detections from the vision service and returns the image if the specified color is detected.
Otherwise, it raises a `NoCaptureToStoreError()` error.

{{% /tab %}}
{{% tab name="Go"%}}

This code includes the utility function and safeguard you implemented earlier, and also includes error handling for getting the next source image and obtaining detections.

```go {class="line-numbers linkable-line-numbers"}
// Next contains the filtering logic and returns select data from the underlying camera.
func (fs filterStream) Next(ctx context.Context) (image.Image, func(), error) {
    if ctx.Value(data.FromDMContextKey{}) != true {
    // If not data management collector, return underlying stream contents without filtering.
      return fs.cameraStream.Next(ctx)
     }

    // Only return captured image if it contains a certain color set by the vision service.
    img, release, err := fs.cameraStream.Next(ctx)
    if err != nil {
      return nil, nil, errors.New("could not get next source image")
    }
    detections, err := fs.visionService.Detections(ctx, img, map[string]interface{}{})
    if err != nil {
      return nil, nil, errors.New("could not get detections")
    }

    if len(detections) == 0 {
      return nil, nil, data.ErrNoCaptureToStore
    }

    return img, release, err
}
```

If the data management service is the caller, the filter function requests detections from the vision service and returns the image if the specified color is detected.
Otherwise, it raises a `data.ErrNoCaptureToStore` error.

{{% /tab %}}
{{< /tabs >}}

After you have implemented your resource subtype's required methods and written your filter function, your final code should look like this:

{{< tabs >}}
{{% tab name="Python"%}}

<file>color_filter.py</file> implements "colorfilter", a custom model of the [camera component API](/components/camera/#api).

<details>
  <summary>Click to view sample code from <file>color_filter.py</file></summary>

```python {class="line-numbers linkable-line-numbers"}
from typing import (
    ClassVar, Mapping, Sequence, Optional, cast, Tuple, List, Any, Dict
)
from typing_extensions import Self
from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, ResponseMetadata, Geometry
from viam.components.camera import Camera
from viam.resource.types import Model, ModelFamily
from viam.resource.base import ResourceBase
from viam.media.video import NamedImage
from PIL import Image
from viam.errors import NoCaptureToStoreError
from viam.services.vision import Vision
from viam.utils import from_dm_from_extra


class ColorFilterCam(
        Camera,
        Reconfigurable
  ):

    """A ColorFilterCam wraps the underlying camera
    `actual_cam` and only keeps the data captured on the
    actual camera if `vision_service` detects a certain
    color in the captured image.
    """
    MODEL: ClassVar[Model] = Model(
        ModelFamily("example", "camera"),
        "colorfilter")

    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    def new_cam(
        cls,
        config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        cam = cls(config.name)
        cam.reconfigure(config, dependencies)
        return cam

    @classmethod
    def validate_config(
        cls,
        config: ComponentConfig
    ) -> Sequence[str]:
        """Validates JSON configuration"""
        actual_cam = config.attributes.fields["actual_cam"].string_value
        if actual_cam == "":
            raise Exception(
              "actual_cam attribute is required for a ColorFilterCam component"
              )
        vision_service = config.attributes.fields[
          "vision_service"
        ].string_value
        if vision_service == "":
            raise Exception(
              """
              vision_service attribute
              is required for a
              ColorFilterCam component
              """
            )
        return [actual_cam, vision_service]

    def reconfigure(
        self,
        config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """Handles attribute reconfiguration"""
        actual_cam_name = config.attributes.fields[
          "actual_cam"
        ].string_value
        actual_cam = dependencies[
          Camera.get_resource_name(actual_cam_name)
        ]
        self.actual_cam = cast(Camera, actual_cam)

        vision_service_name = config.attributes.fields[
          "vision_service"
          ].string_value
        vision_service = dependencies[
          Vision.get_resource_name(
            vision_service_name
          )
        ]
        self.vision_service = cast(
           Vision,
           vision_service
        )

    async def get_properties(
              self,
              *,
              timeout: Optional[float] = None,
              **kwargs
    ) -> Camera.Properties:
        """Returns details about the camera"""
        return await self.actual_cam.get_properties()

    async def get_image(
              self,
              mime_type: str = "",
              *,
              extra: Optional[Dict[str, Any]] = None,
              timeout: Optional[float] = None,
              **kwargs
    ) -> Image.Image:
        """Filters the output of the underlying camera"""
        img = await self.actual_cam.get_image()
        if from_dm_from_extra(extra):
            detections = await self.vision_service.get_detections(img)
            if len(detections) == 0:
                raise NoCaptureToStoreError()

        return img

    async def get_images(
              self,
              *,
              timeout: Optional[float] = None,
              **kwargs
    ) -> Tuple[
         List[NamedImage],
         ResponseMetadata
         ]:
        raise NotImplementedError

    async def get_point_cloud(
              self,
              *,
              extra: Optional[Dict[str, Any]] = None,
              timeout: Optional[float] = None,
              **kwargs
    ) -> Tuple[
         bytes,
         str
         ]:
        raise NotImplementedError

    async def get_geometries(self) -> List[Geometry]:
        raise NotImplementedError
```

In this code:

- The Python SDK simplifies the verification process by exposing the utility function `from_dm_from_extra`, to see if the caller is the data management service for you.

- If the boolean is `true`, the function will call the vision service to get detections and return the image if the color is detected.
  Otherwise, it raises `NoCaptureToStoreError()`.

{{% /tab %}}
{{% tab name="Go"%}}

<file>color_filter.go</file> implements "colorfilter", a custom model of the [camera component API](/components/camera/#api).

<details>
  <summary>Click to view sample code from <file>color_filter.go</file></summary>

```go {class="line-numbers linkable-line-numbers"}
// Package colorfilter implements a modular camera that filters the output of an underlying camera and only keeps
// captured data if the vision service detects a certain color in the captured image.
package colorfilter

import (
"context"
"fmt"
"image"

    "go.viam.com/rdk/logging"
    "github.com/pkg/errors"
    "github.com/viamrobotics/gostream"

    "go.viam.com/rdk/components/camera"
    "go.viam.com/rdk/data"
    "go.viam.com/rdk/pointcloud"
    "go.viam.com/rdk/resource"
    "go.viam.com/rdk/rimage/transform"
    "go.viam.com/rdk/services/vision"

)

var (
    // Model is the full model definition.
    Model = resource.NewModel("example", "camera", "colorfilter")
    errUnimplemented = errors.New("unimplemented")
)

func init() {
    resource.RegisterComponent(camera.API, Model, resource.Registration[camera.Camera, *Config]{
    Constructor: newCamera,
    })
}

func newCamera(ctx context.Context, deps resource.Dependencies, conf resource.Config, logger logging.Logger) (camera.Camera, error) {
    c := &colorFilterCam{
        Named: conf.ResourceName().AsNamed(),
        logger: logger,
    }
    if err := c.Reconfigure(ctx, deps, conf); err != nil {
        return nil, err
    }
    return c, nil
}

// Config contains the name to the underlying camera and the name of the vision service to be used.
type Config struct {
    ActualCam string `json:"actual_cam"`
    VisionService string `json:"vision_service"`
}

// Validate validates the config and returns implicit dependencies.
func (cfg \*Config) Validate(path string) ([]string, error) {
    if cfg.ActualCam == "" {
        return nil, fmt.Errorf(`expected "actual_cam" attribute in %q`, path)
    }
    if cfg.VisionService == "" {
        return nil, fmt.Errorf(`expected "vision_service" attribute in %q`, path)
    }

    return []string{cfg.ActualCam, cfg.VisionService}, nil

}

// A colorFilterCam wraps the underlying camera `actualCam` and only keeps the data captured on the actual camera if `visionService`
// detects a certain color in the captured image.
type colorFilterCam struct {
    resource.Named
    actualCam camera.Camera
    visionService vision.Service
    logger loggingg.Logger
}

// Reconfigure reconfigures the modular component with new settings.
func (c *colorFilterCam) Reconfigure(ctx context.Context, deps resource.Dependencies, conf resource.Config) error {
    camConfig, err := resource.NativeConfig[*Config](conf)
    if err != nil {
        return err
    }

    c.actualCam, err = camera.FromDependencies(deps, camConfig.ActualCam)
    if err != nil {
        return errors.Wrapf(err, "unable to get camera %v for colorfilter", camConfig.ActualCam)
    }

    c.visionService, err = vision.FromDependencies(deps, camConfig.VisionService)
    if err != nil {
        return errors.Wrapf(err, "unable to get vision service %v for colorfilter", camConfig.VisionService)
    }

    return nil

}

// DoCommand simply echoes whatever was sent.
func (c \*colorFilterCam) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
    return cmd, nil
}

// Close closes the underlying camera.
func (c \*colorFilterCam) Close(ctx context.Context) error {
    return c.actualCam.Close(ctx)
}

// Images does nothing.
func (c \*colorFilterCam) Images(ctx context.Context) ([]camera.NamedImage, resource.ResponseMetadata, error) {
    return nil, resource.ResponseMetadata{}, errUnimplemented
}

// Stream returns a stream that filters the output of the underlying camera stream in the stream.Next method.
func (c \*colorFilterCam) Stream(ctx context.Context, errHandlers ...gostream.ErrorHandler) (gostream.VideoStream, error) {
camStream, err := c.actualCam.Stream(ctx, errHandlers...)
    if err != nil {
        return nil, err
    }

    return filterStream{camStream, c.visionService}, nil

}

// NextPointCloud does nothing.
func (c \*colorFilterCam)NextPointCloud(ctx context.Context)(pointcloud.PointCloud, error)
{
    return nil, errUnimplemented
}

// Properties returns details about the camera.
func (c \*colorFilterCam) Properties(ctx context.Context)(camera.Properties, error)
{
    return c.actualCam.Properties(ctx)
}

// Projector does nothing.
func (c \*colorFilterCam) Projector(ctx context.Context) (transform.Projector, error) {
    return nil, errUnimplemented
}

type filterStream struct {
    cameraStream gostream.VideoStream
    visionService vision.Service
}

// Next contains the filtering logic and returns select data from the underlying camera.
func (fs filterStream) Next(ctx context.Context) (image.Image, func(), error) {
    if ctx.Value(data.FromDMContextKey{}) != true {
        // If not data management collector, return underlying stream contents without filtering.
        return fs.cameraStream.Next(ctx)
    }

    // Only return captured image if it contains a certain color set by the vision service.
    img, release, err := fs.cameraStream.Next(ctx)
    if err != nil {
        return nil, nil, errors.New("could not get next source image")
    }
    detections, err := fs.visionService.Detections(ctx, img, map[string]interface{}{})
    if err != nil {
        return nil, nil, errors.New("could not get detections")
    }

    if len(detections) == 0 {
        return nil, nil, data.ErrNoCaptureToStore
    }

    return img, release, err
}

// Close closes the stream.
func (fs filterStream) Close(ctx context.Context) error {
    return fs.cameraStream.Close(ctx)
}
```

In this code:

- A modular camera coded in Go looks for a flag called `fromDM` in the context (`ctx`) using `ctx.Value(data.FromDMContextKey{})` to figure out if the data management service is the caller.

- If the boolean is `true`, the function will call the vision service to get detections and return the image if the color is .
  Otherwise, it will raise the [`ErrNoCaptureToStore`](https://github.com/viamrobotics/rdk/blob/214879e147970a454f78035e938ea853fcd79f17/data/collector.go#L44) error.

{{% /tab %}}
{{< /tabs >}}

For more information, see [Code a new resource model](/registry/create/#code-a-new-resource-model).

#### Code an entry point file

Next, code your module entry point file which `viam-server` will use to initialize and start the filter module.

To code an entry point file yourself, locate the subtype API as defined in the relevant `<resource-name>/<resource-name>.go` file in the [RDK source code](https://github.com/viamrobotics/rdk).

- In this example, the camera's API is defined in the <file>[camera.go](https://github.com/viamrobotics/rdk/blob/main/components/camera/camera.go)</file> file in the RDK source code.
  When developing your <file>main.go</file> or <file>main.py</file> file, reference this file.

{{< tabs >}}
{{% tab name="Python"%}}

Follow these steps to code your entry point file:

1. Inside of your filter module's directory, create a new file named <file>main.py</file>.
   This will be the entry point file for the module.
1. Add the code below which initializes and starts the filter module.

```python {class="line-numbers linkable-line-numbers"}
import asyncio
from viam.components.camera import Camera
from viam.module.module import Module
from viam.resource.registry import Registry, ResourceCreatorRegistration
import color_filter


async def main():

    """
    This function creates and starts a new module,
    after adding all desired resource models.
    Resource creators must be
    registered to the resource
    registry before the module adds the resource model.
    """
    Registry.register_resource_creator(
        Camera.SUBTYPE,
        color_filter.ColorFilterCam.MODEL,
        ResourceCreatorRegistration(
            color_filter.ColorFilterCam.new_cam,
            color_filter.ColorFilterCam.validate_config
        )
    )
    module = Module.from_args()
    module.add_model_from_registry(
        Camera.SUBTYPE,
        color_filter.ColorFilterCam.MODEL
    )
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go"%}}

Follow these steps to code your entry point file:

1. Open the folder named `module` inside of your filter module's directory and create a new file named <file>main.go</file>.
   This will be the entry point file for the module.
1. Add the code below which initializes and starts the filter module.

```go {class="line-numbers linkable-line-numbers"}
// Package main is a module which serves the colorfilter custom module.
package main

import (
  "context"

  "go.viam.com/rdk/logging"
  "go.viam.com/utils"

  "github.com/viam-labs/modular-filter-examples/colorfilter"
  "go.viam.com/rdk/components/camera"
  "go.viam.com/rdk/module"
)

func main() {
  utils.ContextualMain(mainWithArgs, module.NewLoggerFromArgs("colorfilter_module"))
}

func mainWithArgs(ctx context.Context, args []string, logger logging.Logger) (err error) {
  myMod, err := module.NewModuleFromArgs(ctx, logger)
  if err != nil {
    return err
  }

  err = myMod.AddModelFromRegistry(ctx, camera.API, colorfilter.Model)
  if err != nil {
    return err
  }

  err = myMod.Start(ctx)
  defer myMod.Close(ctx)
  if err != nil {
    return err
  }
  <-ctx.Done()
  return nil
}
```

{{% /tab %}}
{{< /tabs >}}

For more information on creating your own module, refer to [Code your own modules to create modular resources](/registry/create/).

Once you've written your filter module, [compile the executable](/registry/create/#prepare-the-module-for-execution) that runs your module when executed.

Note the absolute path to your module’s executable for use in the next section.

### Add as a local module

Whether you've downloaded the `colorfilter` module, or written your own color filtering module, the next step is to add the module to your smart machine as a local module:

1. Navigate to the **Config** tab of your robot's page in the [Viam app](https://app.viam.com/robots).
1. Select the **Modules** subtab and scroll to the **Add local module** section.
1. Enter a name for your local module, enter the [module's executable path](/registry/create/#prepare-the-module-for-execution), then click **Add module**.
   - The name must use only lowercase characters.
1. Then, click **Save config**.

![A color filter module that has been added.](/tutorials/pet-photographer/add-colorfilter-module.png)

## Add services

Next, add the following services to your smart machine to support the color filter module:

- The [data management service](/services/data/) enables your smart machine to capture data and sync it to the cloud.
- The [vision service](/services/vision/detection/) enables your smart machine to perform color detection on objects in a camera stream.

If you are filtering data from other components, such as [sensors](/components/sensor/), you may need to add different services, such as the [sensors service](/services/sensors/) which provides a central interface to all of your robot’s sensors.

### Add the data management service

To enable data capture on your robot, add and configure the [data management service](/services/data/) to capture and store data on your robot's computer:

{{< tabs >}}
{{% tab name="Config Builder" %}}

1. On the **Config** page, click the **Services** subtab and click **Create service** in the lower-left corner.
1. Choose `Data Management` as the type and name your instance of the data manager `dm`.
1. Select **Create**.
1. On the panel that appears, you can manage the capturing and syncing functions individually.
   By default, the data management service captures data every 0.1 minutes to the <file>~/.viam/capture</file> directory.

   Leave the default settings as they are.
   Click **Save config** at the bottom of the window.

   ![An instance of the data management service named "dm". The cloud sync and capturing options are toggled on and the directory is empty. The interval is set to 0.1](/tutorials/pet-photographer/data-management-services.png)

   For more detailed information, see [Add the data management service](/services/data/configure-data-capture/#add-the-data-management-service).
   {{% /tab %}}
   {{% tab name="JSON Template" %}}
   Add the data management service to the services array in your rover’s raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "dm",
  "type": "data_manager",
  "namespace": "rdk",
  "attributes": {
    "sync_interval_mins": 0.1,
    "capture_dir": "",
    "tags": [],
    "additional_sync_paths": []
  }
}
```

Click **Save Config** when done.

{{% /tab %}}
{{< /tabs >}}

### Add the vision service

To enable your smart machine to detect a specific color in its camera stream, add a [vision service color detector](/services/vision/detection/).
For this tutorial, we will configure the vision service to recognize a blue dog collar using `#43A1D0` or `rgb(67, 161, 208)`.
If you have a different item you want to use, or want to match to a color that matches your pet closely, you can use a different color.

{{< tabs >}}
{{% tab name="Config Builder" %}}

1. On the **Config** page, click the **Services** subtab and click **Create service** in the lower-left corner.
1. Select the `Vision` type, then select the `Color Detector` model.
1. Enter `my_color_detector` as the name for your detector and click **Create**.
1. In the vision service panel, click the color selection box to set the color to be detected.
   For this tutorial, set the color to `#43A1D0` or `rgb(67, 161, 208)`.
   Alternatively, you can provide the color of your pet, or use a different brightly-colored collar or ribbon.
1. Set **Hue Tolerance** to `0.06` and **Segment Size px** to `100`.
1. Then, click **Save config**.

Your configuration should look like the following:

![The vision service configuration panel showing the color set to blue, the hue tolerance set to 0.06, and the segment size set to 100.](/tutorials/pet-photographer/vision-service.png)

For more detailed information, refer to [Configure a color detector](/services/vision/detection/#configure-a-color_detector).

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your rover’s raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my_color_detector",
  "type": "vision",
  "model": "color_detector",
  "attributes": {
    "segment_size_px": 100,
    "detect_color": "#43a1d0",
    "hue_tolerance_pct": 0.06
  }
}
```

Click **Save Config** when done.

{{% /tab %}}
{{< /tabs >}}

## Enable filtering by color

With the vision and data management services configured, you can now configure your camera to filter by color and sync photos to Viam's cloud.

### Configure your camera

If you haven't already, add a [camera](/components/camera/) component to your smart machine:

1. Navigate to your robot's page on the [Viam app](https://app.viam.com/robots) and select the **Config** tab.
1. Click the **Components** subtab and click **Create component** in the lower-left corner.
1. Select the `camera` and then select `webcam`.
   1.Enter 'cam' as the name for your camera, then click **Create**.

Your robot's configuration page now includes a panel for your camera.

- To choose the camera the robot will use, click the **video path** field.
  - If your robot is connected to the Viam app, you'll see a list of available cameras.
  - Select the `camera` you want to use, then click **Save config**.

![An instance of the webcam component named 'cam'](/tutorials/pet-photographer/webcam-component.png)

### Add the color filter component

1. Click the **Components** subtab and then click **Create component**.
1. Next, select the `local modular resource` type from the list.
   {{<imgproc src="/tutorials/pet-photographer/add-local-module-select.png" resize="300x" declaredimensions=true alt="The add a component modal showing the list of components to add with 'local modular resource' shown at the bottom">}}
1. On the following screen:

   1. Select the camera from the dropdown menu.
   1. Enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} for your modular resource's {{< glossary_tooltip term_id="model" text="model" >}}, `example:camera:colorfilter`.
   1. Provide a name for this instance of your modular resource.
      This name must be different from the module name.

      {{<imgproc src="/tutorials/pet-photographer/add-colorfilter-module-create.png" resize="400x" declaredimensions=true alt="The add a component model showing the create a module step for a local color filter module">}}

1. Click **Create** to create the modular resource component.
1. In the resulting module configuration pane, copy the following JSON configuration into the **Attributes** section:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "vision_service": "my_color_detector",
     "actual_cam": "cam"
   }
   ```

   ![A component panel for a color filter modular resource with the attributes filled out for vision service and actual_cam](/tutorials/pet-photographer/colorfiltercam-component-attributes.png)

### Configure data capture

To add data capture for the color filter camera, click **Add Method** in the **Data Capture configuration** section of your color filter camera component.
Toggle the **Type** dropdown menu, select **ReadImage**, and set the **Frequency** of the capture to `0.1`, which will configure the data management service to capture images from your camera about once every 10 seconds.
Then, click **Save config**.

![A component panel for a color filter modular resource with the attributes filled out for vision service and actual_cam as well as the data capture configuration capture set capture ReadImage at 0.1 frequency](/tutorials/pet-photographer/colorfiltercam-component.png)

## Test your color filter camera

To test that your color filter camera is capturing and filtering images properly, navigate to the **Control** tab on your robot's page.

On the **colorfiltercam** panel, toggle **view colorfiltercam** to view your camera's live feed.
Test the filter by positioning your smart machine so that it captures an image of your pet wearing its collar.
Then examine the **Data** tab to confirm that only pictures containing your pet wearing their collar are stored.

For example, the following is the result of several dozen pictures of the same dog, but only those pictures where he is wearing the blue collar were captured and synced to the cloud:

![Filtered data tab contents from colorfiltercam showing only photos of dog with blue collar](/tutorials/pet-photographer/data-capture.png)

## Next steps

Your pet photographer is now set up.
Place it in an area your pet frequently visits and don't forget to attach the colored object to your pet.

Now you can follow similar steps and customize the code you've written to configure a sensor for detecting specific thresholds or filter out blurry images from your camera's captures.

Try these other tutorials for more on working with the data management and vision services:

{{< cards >}}
{{% card link="/tutorials/services/try-viam-color-detection/" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" %}}
{{% card link="/tutorials/projects/guardian/" %}}
{{% card link="/tutorials/projects/send-security-photo/" %}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/"  %}}
{{< /cards >}}
