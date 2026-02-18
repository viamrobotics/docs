---
title: "Part 3: Implement your module"
linkTitle: "Part 3: Implement"
weight: 33
layout: "docs"
type: "docs"
description: "Implement configuration validation, reconfiguration, and API methods for your module."
---

**Part 3 of 5** | ⏱️ 30-40 minutes

## What you'll do in this part

- Implement configuration validation for your model
- Set up reconfiguration to use config values
- Implement the camera's `GetImages` method
- Understand how to implement API methods in general

At the end of this part, you'll have a working single-model module that returns images.

## Implementation overview

You'll implement your module in three main steps:

1. **Validation**: Check that user configuration is correct
2. **Reconfiguration**: Use configuration values in your code
3. **API methods**: Implement the actual functionality

## Step 1: Configuration validation

### Why validation matters

When users add your module to their machine, they provide configuration in JSON format. Validation ensures:
- Required attributes are present
- Attributes are the correct type
- You can provide helpful error messages early

For the example camera model, users will configure it like this:

```json
{
  "image_path": "/path/to/file.png"
}
```

Your validation must verify that `image_path` exists and is a string.

### Implement validate_config

Model configuration happens in two steps:

#### Validation

The validation step serves two purposes:

- Confirm that the model configuration contains all **required attributes** and that these attributes are of the right type.
- Identify and return a list of names of **required resources** and a list of names of **optional resources**.
  `viam-server` will pass these resources to the next step as dependencies.
  For more information, see [Module dependencies](/operate/modules/advanced/dependencies/).

{{< tabs >}}
{{% tab name="Python" %}}

Open `src/models/hello_camera.py` and find the `validate_config` method (around line 38).

Replace it with:

```python {class="line-numbers linkable-line-numbers" data-start="38" data-line="5-10"}
    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        # Check that a path to get an image was configured
        fields = config.attributes.fields
        if "image_path" not in fields:
            raise Exception("Missing image_path attribute.")
        elif not fields["image_path"].HasField("string_value"):
            raise Exception("image_path must be a string.")

        return [], []
```

**Code explanation:**
- **Lines 43-44**: Get the configuration attributes as a dictionary
- **Lines 45-46**: Check if `image_path` exists in the config
- **Lines 47-48**: Verify it's a string type (not a number or other type)
- **Line 50**: Return `(required_dependencies, optional_dependencies)` - we have none for this simple camera

{{% /tab %}}
{{% tab name="Go" %}}

Open `hello-world/module.go` and find the `Validate` function (around line 51).

Replace it with:

```go {class="line-numbers linkable-line-numbers" data-start="51" data-line="2-10"}
func (cfg *Config) Validate(path string) ([]string, []string, error) {
    var deps []string
    if cfg.ImagePath == "" {
        return nil, nil, resource.NewConfigValidationFieldRequiredError(path, "image_path")
    }
    if reflect.TypeOf(cfg.ImagePath).Kind() != reflect.String {
        return nil, nil, errors.New("image_path must be a string.")
    }
    imagePath = cfg.ImagePath
    return deps, []string{}, nil
}
```

Add the import at the top of the file:

```go {class="line-numbers linkable-line-numbers" data-start="7"}
"reflect"
```

**Code explanation:**
- **Line 53**: Check if `image_path` is empty (required field)
- **Lines 54-55**: Return error with helpful message if missing
- **Lines 56-58**: Verify it's a string type
- **Line 59**: Store the path in a global variable for later use
- **Line 60**: Return `(required_deps, optional_deps, error)` - we have no dependencies

{{% /tab %}}
{{< /tabs >}}

✅ **Checkpoint 1:** Configuration validation implemented

{{< expand "What happens if validation fails?" >}}
If a user misconfigures your module (forgets `image_path` or uses the wrong type), `viam-server` will:
1. Refuse to start the module
2. Show your error message in the configuration panel
3. Display the error in logs

This prevents runtime errors and helps users debug configuration issues quickly.
{{< /expand >}}

## Step 2: Reconfiguration

### Why reconfiguration matters

After validation succeeds, `viam-server` calls the `reconfigure` method. This is where you:
- Store configuration values for use in API methods
- Set up any stateful resources
- Access dependencies from other components

#### Reconfiguration

`viam-server` calls the `reconfigure` method when the user adds the model or changes its configuration.

The reconfiguration step serves two purposes:

- Use the configuration attributes and dependencies to set attributes on the model for usage within the API methods.
- Obtain access to dependencies.
  For information on how to use dependencies, see [Module dependencies](/operate/modules/advanced/dependencies/).

### Implement reconfigure

{{< tabs >}}
{{% tab name="Python" %}}

Open `src/models/hello_camera.py` and find the `reconfigure` method (around line 51).

Replace it with:

```python {class="line-numbers linkable-line-numbers" data-start="51" data-line="4-5"}
    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        attrs = struct_to_dict(config.attributes)
        self.image_path = str(attrs.get("image_path"))

        return super().reconfigure(config, dependencies)
```

Add the import at the top of the file:

```python {class="line-numbers linkable-line-numbers" data-start="1"}
from viam.utils import struct_to_dict
```

**Code explanation:**
- **Line 54**: Convert config attributes to a Python dictionary
- **Line 55**: Store `image_path` as an instance variable for use in API methods
- **Line 57**: Call parent class reconfigure (important!)

{{% /tab %}}
{{% tab name="Go" %}}

For Go modules, configuration handling is done differently:

1. Open `hello-world/module.go`

2. Add `imagePath = ""` to the global variables (around line 18):

   ```go {class="line-numbers linkable-line-numbers" data-start="18" data-line="4"}
   var (
       HelloCamera      = resource.NewModel("exampleorg", "hello-world", "hello-camera")
       errUnimplemented = errors.New("unimplemented")
       imagePath        = ""
   )
   ```

3. Edit the `type Config struct` definition (around line 32), replacing the comments with:

   ```go {class="line-numbers linkable-line-numbers" data-start="32"}
   type Config struct {
       resource.AlwaysRebuild
       ImagePath string `json:"image_path"`
   }
   ```

   This adds the `image_path` attribute and causes the resource to rebuild each time the configuration changes.

{{< expand "Need to maintain state across reconfigurations?" >}}
The `resource.AlwaysRebuild` parameter causes `viam-server` to fully rebuild the resource each time configuration changes.

If you need to maintain state (like keeping PWM loops running for a board), implement a `Reconfigure` function instead:

```go
func (c *helloWorldHelloCamera) Reconfigure(ctx context.Context, deps resource.Dependencies, conf resource.Config) error {
    // Update configuration values
    imagePath = cfg.ImagePath
    // Keep existing state alive
    return nil
}
```

For an example, see [mybase.go on GitHub](https://github.com/viamrobotics/rdk/blob/main/examples/customresources/models/mybase/mybase.go).
{{< /expand >}}

{{% /tab %}}
{{< /tabs >}}

✅ **Checkpoint 2:** Reconfiguration implemented

## Step 3: Implement API methods

Now comes the core functionality: implementing the methods from your chosen API.

### Camera API: Implement GetImages

The camera API has several methods, but you only need to implement the ones your hardware supports. For this example, we'll implement `GetImages` (required) and leave others unimplemented.

{{< tabs >}}
{{% tab name="Python" %}}

Open `src/models/hello_camera.py` and find the `get_images` method (around line 74).

Replace `raise NotImplementedError()` with:

```python {class="line-numbers linkable-line-numbers" data-start="74" data-line="9-13"}
    async def get_images(
        self,
        *,
        filter_source_names: Optional[Sequence[str]] = None,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Tuple[Sequence[NamedImage], ResponseMetadata]:
        img = Image.open(self.image_path)
        vi_img = pil_to_viam_image(img, CameraMimeType.JPEG)
        named = NamedImage("default", vi_img.data, vi_img.mime_type)
        metadata = ResponseMetadata()
        return [named], metadata
```

Add these imports at the top of the file:

```python {class="line-numbers linkable-line-numbers" data-start="1"}
from viam.media.utils.pil import pil_to_viam_image
from viam.media.video import CameraMimeType
from PIL import Image
```

**Code explanation:**
- **Line 82**: Open the image file using the path from configuration
- **Line 83**: Convert PIL image to Viam's image format
- **Line 84**: Create a NamedImage with source name "default"
- **Line 85**: Create response metadata (can include timing info)
- **Line 86**: Return list of images and metadata

**Add the Pillow dependency:**

Open `requirements.txt` and add:

```text
Pillow
```

Save the file.

{{% /tab %}}
{{% tab name="Go" %}}

Open `hello-world/module.go` and find the `Images` method (around line 111).

Replace `panic("not implemented")` with:

```go {class="line-numbers linkable-line-numbers" data-start="111"}
func (s *helloWorldHelloCamera) Images(ctx context.Context, filterSourceNames []string, extra map[string]interface{}) ([]camera.NamedImage, resource.ResponseMetadata, error) {
    var responseMetadataRetVal resource.ResponseMetadata

    imgFile, err := os.Open(imagePath)
    if err != nil {
        return nil, responseMetadataRetVal, errors.New("Error opening image.")
    }
    defer imgFile.Close()

    imgByte, err := os.ReadFile(imagePath)
    if err != nil {
        return nil, responseMetadataRetVal, err
    }

    named, err := camera.NamedImageFromBytes(imgByte, "default", "image/png")
    if err != nil {
        return nil, responseMetadataRetVal, err
    }

    return []camera.NamedImage{named}, responseMetadataRetVal, nil
}
```

Add this import at the top of the file:

```go {class="line-numbers linkable-line-numbers" data-start="7"}
"os"
```

**Code explanation:**
- **Lines 114-117**: Open the image file
- **Lines 119-122**: Read file contents into byte array
- **Lines 124-127**: Create a NamedImage from bytes
- **Line 129**: Return slice with one image, metadata, and no error

{{% /tab %}}
{{< /tabs >}}

### What about other camera methods?

The camera API includes methods like `GetPointCloud`, `GetProperties`, and `DoCommand`. You don't need to implement all of them:

- **Unimplemented methods** return an "unimplemented" error automatically
- **DoCommand** can be used for custom functionality (see [Run control logic](/operate/modules/control-logic/))

For this camera, we only implement `GetImages` because that's all our hardware supports.

✅ **Checkpoint 3:** Camera implementation complete

## What you've accomplished

✅ **Module implemented:**
- Configuration validation ensures correct setup
- Reconfiguration stores config values for use
- GetImages method returns images from the file path

✅ **Understanding:**
- How modules validate and use configuration
- How to implement API methods
- What happens with unimplemented methods

✅ **Ready to test:**
- Have a complete, working module
- Ready to test on a real machine

## Next steps

Your module is now ready to test! Continue to [Part 4: Test your module locally](/operate/modules/support-hardware/part-4-test-locally/) to see your module in action.

---

**Tutorial navigation:**
- **Previous:** [← Part 2: Choose an API and generate code](/operate/modules/support-hardware/part-2-choose-api-generate/)
- **Current:** Part 3: Implement your module
- **Next:** [Part 4: Test your module locally →](/operate/modules/support-hardware/part-4-test-locally/)
- **All parts:** [Module creation tutorial](/operate/modules/support-hardware/)
