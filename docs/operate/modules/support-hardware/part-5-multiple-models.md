---
title: "Part 5: Multiple models (advanced)"
linkTitle: "Part 5: Multiple models"
weight: 35
layout: "docs"
type: "docs"
description: "Learn how to create a module with multiple models implementing different APIs."
---

**Part 5 of 5** | ⏱️ 20-25 minutes | **Advanced**

{{< alert title="Prerequisites" color="note" >}}
Complete Parts 1-4 first. You should have a working single-model module before adding more models.
{{< /alert >}}

## What you'll do in this part

- Understand when to use multiple models in one module
- Generate code for a second model (sensor)
- Integrate both models into one module
- Implement the sensor's `GetReadings` method
- Test both models together

## When to use multiple models

Some of the code you generated for your first modular resource is shared across the module no matter how many modular resource models it supports. Some of the code is resource-specific.

If you have multiple modular resources that are related, you can put them all into the same module.

**Use multiple models when:**
- The hardware provides multiple capabilities (like our camera + sensor example)
- Models share dependencies or configuration
- They're logically related and users would configure them together

**Use separate modules when:**
- The functionality is unrelated
- Each model would be useful independently
- You want to version them separately

### Example: Why two models?

Our example hardware:
- Returns an image (camera functionality)
- Returns a random number (sensor functionality)

Since the [Camera API](/dev/reference/apis/components/camera/) can't return numbers and the [Sensor API](/dev/reference/apis/components/sensor/) can't return images, we need two models.

## Generate the second model

For convenience, run the module generator again from within your existing module's directory to generate code for the sensor:

1. Change directory into your module:
   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   cd hello-world
   ```

2. Run the generator for the sensor model:

{{< tabs >}}
{{% tab name="Python" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate --language python --model-name hello-sensor \
  --name hello-world --resource-subtype=sensor --public false \
  --enable-cloud true
```

{{< alert title="Important" color="caution" >}}
When prompted whether to register the module, select **No**. Your module is already registered.
{{< /alert >}}

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate --language go --model-name hello-sensor \
  --name hello-world --resource-subtype=sensor --public false \
  --enable-cloud true
```

{{< alert title="Important" color="caution" >}}
When prompted whether to register the module, select **No**. Your module is already registered.
{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

This creates a temporary nested `hello-world/hello-world/` directory. You'll copy the sensor-specific code from it.

## Integrate sensor code

Now integrate the sensor model into your existing module:

{{< tabs >}}
{{% tab name="Python" %}}

### 1. Move the sensor model file

Move the generated sensor model file:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
mv hello-world/src/models/hello_sensor.py src/models/
```

### 2. Update main.py

Open `src/main.py` and add `HelloSensor` to the imports:

```python {class="line-numbers linkable-line-numbers" data-line="6, 9"}
import asyncio

from viam.module.module import Module
try:
    from models.hello_camera import HelloCamera
    from models.hello_sensor import HelloSensor
except ModuleNotFoundError:  # when running as local module with run.sh
    from .models.hello_camera import HelloCamera
    from .models.hello_sensor import HelloSensor

if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
```

Save the file.

### 3. Move model documentation

Move the sensor documentation file:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
mv hello-world/<org-id>_hello-world_hello-sensor.md ./
```

### 4. Update meta.json

Open `meta.json` and update the description to mention both models:

```json {class="line-numbers linkable-line-numbers" data-line="6"}
{
  "$schema": "https://dl.viam.dev/module.schema.json",
  "module_id": "exampleorg:hello-world",
  "visibility": "private",
  "url": "",
  "description": "Example camera and sensor components: hello-camera and hello-sensor",
  "applications": null,
  "markdown_link": "README.md",
  "entrypoint": "./run.sh",
  "first_run": "",
  "build": {
    "build": "./build.sh",
    "setup": "./setup.sh",
    "path": "dist/archive.tar.gz",
    "arch": ["linux/amd64", "linux/arm64", "darwin/arm64", "windows/amd64"]
  }
}
```

Save the file.

### 5. Clean up

Delete the temporary directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
rm -rf hello-world/
```

{{% /tab %}}
{{% tab name="Go" %}}

### 1. Rename the camera model file

Rename `module.go` to `hello-camera.go`:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
mv module.go hello-camera.go
```

### 2. Move the sensor model file

Move and rename the sensor model file:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
mv hello-world/module.go hello-sensor.go
```

### 3. Update cmd/module/main.go

Open `cmd/module/main.go` and register both models:

```go {class="line-numbers linkable-line-numbers" data-start="1" data-line="8, 13-16"}
package main

import (
    "helloworld"
    "go.viam.com/rdk/module"
    "go.viam.com/rdk/resource"
    camera "go.viam.com/rdk/components/camera"
    sensor "go.viam.com/rdk/components/sensor"
)

func main() {
    // ModularMain can take multiple APIModel arguments, if your module implements multiple models.
    module.ModularMain(
      resource.APIModel{ camera.API, helloworld.HelloCamera},
      resource.APIModel{ sensor.API, helloworld.HelloSensor},
    )
}
```

Save the file.

### 4. Move model documentation

Move the sensor documentation file:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
mv hello-world/<org-id>_hello-world_hello-sensor.md ./
```

### 5. Update meta.json

Open `meta.json` and update the description to mention both models:

```json {class="line-numbers linkable-line-numbers" data-line="6"}
{
  "$schema": "https://dl.viam.dev/module.schema.json",
  "module_id": "exampleorg:hello-world",
  "visibility": "private",
  "url": "",
  "description": "Example camera and sensor components: hello-camera and hello-sensor",
  "applications": null,
  "markdown_link": "README.md",
  "entrypoint": "bin/hello-world",
  "first_run": "",
  "build": {
    "build": "make module.tar.gz",
    "setup": "make setup",
    "path": "module.tar.gz",
    "arch": ["linux/amd64", "linux/arm64", "darwin/arm64", "windows/amd64"]
  }
}
```

Save the file.

### 6. Fix duplicate definitions in hello-sensor.go

Since `errUnimplemented` and `Config` are already defined in `hello-camera.go`, update `hello-sensor.go`:

1. **Delete the `"errors"` import** (if it exists only for `errUnimplemented`)
2. **Delete the line:** `errUnimplemented = errors.New("unimplemented")`
3. **Rename** `type Config struct {` to `type sensorConfig struct {`
4. **Replace all instances** of `*Config` in `hello-sensor.go` with `*sensorConfig`

### 7. Clean up

Delete the temporary directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
rm -rf hello-world/
```

{{% /tab %}}
{{< /tabs >}}

✅ **Checkpoint 1:** Sensor code integrated

## Implement the sensor API

Now implement the `GetReadings` method for the sensor:

{{< tabs >}}
{{% tab name="Python" %}}

Open `src/models/hello_sensor.py` and find the `get_readings` method (around line 63).

Replace `raise NotImplementedError()` with:

```python {class="line-numbers linkable-line-numbers" data-start="63" data-line="8-11"}
    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:
        number = random.random()
        return {
            "random_number": number
        }
```

Add the import at the top of the file:

```python {class="line-numbers linkable-line-numbers" data-start="1"}
import random
```

Save the file.

**Code explanation:**
- **Line 70**: Generate a random number between 0 and 1
- **Lines 71-73**: Return a dictionary with the reading name and value
- Sensor readings are returned as key-value pairs (you can return multiple readings)

{{% /tab %}}
{{% tab name="Go" %}}

Open `hello-sensor.go` and find the `Readings` method (around line 92).

Replace `panic("not implemented")` with:

```go {class="line-numbers linkable-line-numbers" data-start="92"}
func (s *helloWorldHelloSensor) Readings(ctx context.Context, extra map[string]interface{}) (map[string]interface{}, error) {
    number := rand.Float64()
    return map[string]interface{}{
        "random_number": number,
    }, nil
}
```

Add the import at the top of the file:

```go {class="line-numbers linkable-line-numbers" data-start="7"}
"math/rand"
```

Save the file.

**Code explanation:**
- **Line 93**: Generate a random number between 0 and 1
- **Lines 94-96**: Return a map with the reading name and value
- **Line 97**: Return no error (nil)

{{% /tab %}}
{{< /tabs >}}

Note that the sensor has no configurable attributes, so you don't need to modify the validation or reconfiguration methods.

✅ **Checkpoint 2:** Sensor implementation complete

## Test both models

Now test your multi-model module:

1. **Reload the module** using hot reload:
   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module reload --part-id YOUR_PART_ID
   ```

2. **Add the sensor component:**
   - On your machine's **CONFIGURE** page, click **+**
   - Select **Local module** → **Local component**
   - Enter the model: `exampleorg:hello-world:hello-sensor`
   - Select **Sensor** as the Type
   - Enter a Name: `sensor-1`
   - Click **Create**

3. **Test the sensor:**
   - Click the **TEST** section of the sensor card
   - You should see `{"random_number": 0.xxxxx}` with a random number

4. **Verify camera still works:**
   - Test your camera component again
   - Both should work independently

{{<imgproc src="/how-tos/hello-camera.png" resize="x1100" declaredimensions=true alt="Camera and sensor both working in the test panel." style="width:800px" class="shadow aligncenter" >}}

✅ **Checkpoint 3:** Both models working!

## Best practices

### When adding multiple models:

1. **Keep models independent**: Each model should work without the others
2. **Share common code**: Put shared utilities in separate files
3. **Document each model**: Each model should have its own documentation file
4. **Test individually**: Verify each model works before combining
5. **Version together**: All models in a module share the same version number

### Module organization

For modules with many models, consider this structure:

```
my-module/
├── src/
│   ├── models/
│   │   ├── model1.py
│   │   ├── model2.py
│   │   └── model3.py
│   ├── utils/
│   │   └── shared.py
│   └── main.py
```

## What you've accomplished

✅ **Multi-model module created:**
- Generated second model (sensor)
- Integrated both models into one module
- Both models register and work independently

✅ **Complete implementation:**
- Camera returns images from configured path
- Sensor returns random number readings
- Both tested and working

✅ **Understanding:**
- When to use multiple models vs. separate modules
- How to integrate multiple models
- Best practices for module organization

## Next steps

Congratulations! You've created a complete, working module with multiple models. Now you're ready to:

1. **Deploy to the registry**: [Package and deploy your module](/operate/modules/deploy-module/)
2. **Share with others**: Make your module public so others can use it
3. **Add more features**: Implement additional models or enhance existing ones
4. **Learn more advanced topics**:
   - [Module dependencies](/operate/modules/advanced/dependencies/)
   - [Custom configuration options](/operate/modules/advanced/module-configuration/)
   - [Logging in modules](/operate/modules/advanced/logging/)

---

**Tutorial navigation:**
- **Previous:** [← Part 4: Test your module locally](/operate/modules/support-hardware/part-4-test-locally/)
- **Current:** Part 5: Multiple models (advanced)
- **Next:** [Deploy to registry →](/operate/modules/deploy-module/)
- **All parts:** [Module creation tutorial](/operate/modules/support-hardware/)
