---
linkTitle: "Part 4: Deploy a Module"
title: "Part 4: Deploy a Module"
weight: 40
layout: "docs"
type: "docs"
description: "Deploy your inspector module and configure queryable detection data capture."
date: "2025-01-30"
---

**Goal:** Deploy your inspector to run on the machine autonomously.

**Skills:** Module packaging, registry deployment, tabular data capture.

**Time:** ~10 min

## What You'll Do

In Part 3, you built inspection logic that runs from your laptop. That's great for development, but in production the code needs to run on the machine itself—so it works even when your laptop is closed.

The starter repo already created most of what you need:

- A module entry point that connects your service to viam-server
- `meta.json`—registry metadata
- Model registration so viam-server can create instances of your service

You just need to set your namespace, build, package, and deploy.

## 4.1 Review the Module Structure

The starter repo already includes everything needed to run as a module. Let's review what's there.

### Module entry point

{{< tabs >}}
{{% tab name="Python" %}}

**`src/main.py`**

```python
import asyncio
from viam.module.module import Module
try:
    from models.inspector import Inspector
except ModuleNotFoundError:
    from .models.inspector import Inspector

if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
```

`Module.run_from_registry()` connects your module to viam-server. The import of `Inspector` is what triggers model registration—when Python loads the class, `EasyResource` automatically registers it. You don't need to modify this file.

{{% /tab %}}
{{% tab name="Go" %}}

**`cmd/module/main.go`**

```go
func main() {
    module.ModularMain(
        resource.APIModel{API: generic.API, Model: inspectionmodule.Inspector},
    )
}
```

This connects your module to viam-server and registers the inspector model. When you add this service to your machine configuration, viam-server uses this entry point to create and manage instances. You don't need to modify this file.

{{% /tab %}}
{{< /tabs >}}

{{< alert title="What is a model?" color="info" >}}
In Viam, a _model_ is a specific implementation of an API—identified by a triplet like `your-namespace:inspection-module:inspector`. This can be confusing because we also refer to ML models as "models." When you see "model" in the context of modules and resources, it means the implementation type, not a machine learning model.
{{< /alert >}}

### Model registration

{{< tabs >}}
{{% tab name="Python" %}}

In Python, model registration is automatic. When `Inspector` subclasses `EasyResource`, the `EasyResource.__init_subclass__` hook registers the model with viam-server using the `MODEL` class variable:

```python
class Inspector(Generic, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("stations", "inspection-module"), "inspector"
    )
```

No explicit registration function needed—the class definition itself is the registration.

{{% /tab %}}
{{% tab name="Go" %}}

**`module.go`** provides model registration in `init()`:

```go
var Inspector = resource.NewModel("stations", "inspection-module", "inspector")

func init() {
    resource.RegisterService(generic.API, Inspector,
        resource.Registration[resource.Resource, *Config]{
            Constructor: newInspectionModuleInspector,
        },
    )
}
```

Note the two uses of "inspector" here:

- `Inspector` (capital I)—the Go variable name, exported so `main.go` can reference it
- `"inspector"` (lowercase, in quotes)—a string that becomes the third part of the model triplet `stations:inspection-module:inspector`

This `init()` function runs automatically when the module starts, telling viam-server how to create instances of your service.

{{% /tab %}}
{{< /tabs >}}

### Registry metadata

{{< tabs >}}
{{% tab name="Python" %}}

**`meta.json`**

```json
{
  "module_id": "stations:inspection-module",
  "visibility": "private",
  "models": [
    {
      "api": "rdk:service:generic",
      "model": "stations:inspection-module:inspector"
    }
  ],
  "entrypoint": "./run.sh"
}
```

The `entrypoint` points to `run.sh`, which creates a virtual environment, installs dependencies, and starts the module. The `models` array is pre-populated—it tells the registry what your module provides.

{{% /tab %}}
{{% tab name="Go" %}}

**`meta.json`**

```json
{
  "module_id": "stations:inspection-module",
  "visibility": "private",
  "entrypoint": "bin/inspection-module"
}
```

The `entrypoint` is the compiled binary. The `models` array will be populated by `update-models` during the build process.

{{% /tab %}}
{{< /tabs >}}

{{< alert title="The key pattern" color="tip" >}}
The starter repo created module infrastructure. You added business logic (`detect`) and exposed it through `DoCommand`. The same constructor works for both CLI testing and module deployment.
{{< /alert >}}

## 4.2 Build and Upload Your Module

### Set your namespace

The starter repos use `stations` as a placeholder namespace. You need to replace it with your organization's public namespace so the module is registered under your account.

1. Find your public namespace:

   ```bash
   viam organizations list
   ```

   Look for the `public_namespace` value for your organization. If you don't have one set, go to your organization's settings page in the Viam app to create one.

2. Update `meta.json`—replace `stations` with your namespace in both the `module_id` and (if present) the `model` field:

   ```json
   {
     "module_id": "YOUR-NAMESPACE:inspection-module",
     ...
     "model": "YOUR-NAMESPACE:inspection-module:inspector"
   }
   ```

3. Update the model triplet in your source code to match:

{{< tabs >}}
{{% tab name="Python" %}}

   In `src/models/inspector.py`, update the `MODEL` definition:

   ```python
   MODEL: ClassVar[Model] = Model(
       ModelFamily("YOUR-NAMESPACE", "inspection-module"), "inspector"
   )
   ```

{{% /tab %}}
{{% tab name="Go" %}}

   In `module.go`, update the model variable:

   ```go
   var Inspector = resource.NewModel("YOUR-NAMESPACE", "inspection-module", "inspector")
   ```

{{% /tab %}}
{{< /tabs >}}

### Register the module

Create the module entry in the Viam registry:

```bash
viam module create --module-path meta.json
```

### Build and package

{{< tabs >}}
{{% tab name="Python" %}}

Build the module archive:

```bash
./build.sh
```

This creates a virtual environment, installs PyInstaller, bundles your code into a standalone binary, and packages it as `dist/archive.tar.gz`.

{{% /tab %}}
{{% tab name="Go" %}}

**Update the module's model list:**

Build a local binary, then run `update-models` to detect which models your module provides and update `meta.json`:

```bash
make
viam module update-models --binary /full/path/to/bin/inspection-module
```

Replace `/full/path/to/` with the absolute path to your module directory.

**Cross-compile for the target platform:**

Your module will run inside a Linux container, not on your development machine. Even if your Mac and the container both use ARM processors, a macOS binary won't run on Linux—you need to cross-compile. Cross-compilation also requires disabling CGO (Go's C interop) and using the `no_cgo` build tag.

{{< tabs >}}
{{% tab name="Mac (Apple Silicon)" %}}

```bash
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -tags no_cgo -o bin/inspection-module ./cmd/module
```

{{% /tab %}}
{{% tab name="Mac (Intel)" %}}

```bash
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -tags no_cgo -o bin/inspection-module ./cmd/module
```

{{% /tab %}}
{{% tab name="Windows" %}}

```bash
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -tags no_cgo -o bin/inspection-module ./cmd/module
```

{{% /tab %}}
{{% tab name="Linux (Intel/AMD)" %}}

```bash
go build -o bin/inspection-module ./cmd/module
```

No cross-compilation needed—you're already on Linux.

{{% /tab %}}
{{% tab name="Linux (ARM)" %}}

```bash
go build -o bin/inspection-module ./cmd/module
```

No cross-compilation needed—you're already on Linux.

{{% /tab %}}
{{< /tabs >}}

**Package for upload:**

```bash
tar czf module.tar.gz meta.json bin/
```

{{% /tab %}}
{{< /tabs >}}

### Upload to the registry

The `--platform` flag must match your machine's architecture. Replace `<archive>` with your archive path from the previous step (`dist/archive.tar.gz` for Python, `module.tar.gz` for Go):

{{< tabs >}}
{{% tab name="Mac (Apple Silicon)" %}}

```bash
viam module upload --version 0.0.1 --platform linux/arm64 --upload <archive>
```

{{% /tab %}}
{{% tab name="Mac (Intel)" %}}

```bash
viam module upload --version 0.0.1 --platform linux/amd64 --upload <archive>
```

{{% /tab %}}
{{% tab name="Windows" %}}

```bash
viam module upload --version 0.0.1 --platform linux/amd64 --upload <archive>
```

{{% /tab %}}
{{% tab name="Linux (Intel/AMD)" %}}

```bash
viam module upload --version 0.0.1 --platform linux/amd64 --upload <archive>
```

{{% /tab %}}
{{% tab name="Linux (ARM)" %}}

```bash
viam module upload --version 0.0.1 --platform linux/arm64 --upload <archive>
```

{{% /tab %}}
{{< /tabs >}}

## 4.3 Add the Module to Your Machine

**Add the inspector service:**

1. In the Viam app, go to your machine's **Configure** tab
2. Click **+** next to your machine part
3. Select **Component or service**
4. Search for your model (for example, `your-namespace:inspection-module:inspector`)
5. Name it `inspector-service`
6. Click **Create**

When you add a service from the registry, the module that provides it is added automatically.

**Configure the service attributes:**

```json
{
  "camera": "inspection-cam",
  "vision": "vision-service"
}
```

Click **Save**.

**Verify it started:**

1. Go to the **Logs** tab
2. Look for startup messages from the inspector module
3. You should see it initialize and connect to the camera and vision service

**Test the inspector:**

1. In the **Configure** tab, click on `inspector-service` to open its configuration panel
2. Expand **Test** card at the bottom
3. In the **DoCommand** field, enter `{"detect": true}`
4. Click **Execute**
5. You should see a response with `label` and `confidence` values
6. Click **Execute** several more times to see different detections as cans pass beneath the inspection-cam

{{<imgproc src="/tutorials/first-project/docommand-test.png" resize="x1100" declaredimensions=true alt="DoCommand test panel showing detection result with label PASS and confidence score." class="imgzoom shadow">}}

The module is now ready. You'll configure automatic detection in the next section.

## 4.4 Configure Detection Data Capture

In Part 2, you captured images from the vision service. Those images are great for visual review, but they're binary data—you can't query them with SQL. Now you'll configure **tabular data capture** on your inspector's DoCommand, which will let you query detection results.

**Add inspector-service as a data manager dependency:**

The data manager needs to know about your inspector service before it can capture data from it. You'll add this dependency in the JSON configuration.

1. In the **Configure** tab, click **JSON** in the upper left
2. Find the `data-service` entry in the `services` array
3. Add `"depends_on": ["inspector-service"]` to the data-service configuration:

   ```json
   {
     "name": "data-service",
     "api": "rdk:service:data_manager",
     "model": "rdk:builtin:builtin",
     "attributes": { ... },
     "depends_on": ["inspector-service"]
   }
   ```

4. Click **Save**

This tells viam-server to wait for `inspector-service` to initialize before the data manager tries to capture data from it.

**Enable data capture on the inspector:**

1. In the **Configure** tab, click on `inspector-service` to open its configuration panel
2. Find the **Data capture** section and click **Add method**
3. Select the method: `DoCommand`
4. Set **Frequency (hz)** to `0.5` (captures every 2 seconds)
5. In the **Additional parameters** section, add the DoCommand input:

   ```json
   {
     "detect": true
   }
   ```

6. **Save** your configuration

This configuration tells the data manager to periodically call `DoCommand({"detect": true})` on your inspector and capture the response—which includes `label` and `confidence`.

**Query detection results:**

After a few minutes of data collection, you can query the results:

1. Open the **Data** tab in the Viam app
2. Click **Query**
3. Select **SQL** as your query language

   {{<imgproc src="/tutorials/first-project/data-query-sql.png" resize="x1100" declaredimensions=true alt="Data Query interface with SQL selected." class="imgzoom shadow">}}

4. Run a query to see recent detections:

   ```sql
   SELECT time_received, component_name, data
   FROM readings
   ORDER BY time_received DESC
   LIMIT 10
   ```

   You can also filter to show only failures:

   ```sql
   SELECT time_received,
          data.docommand_output.label,
          data.docommand_output.confidence
   FROM readings
   WHERE data.docommand_output.label = 'FAIL'
   ORDER BY time_received DESC
   LIMIT 10
   ```

**Understanding the data structure:**

Each captured detection is stored as a JSON document. Here's what the data looks like:

```json
{
  "component_name": "inspector-service",
  "component_type": "rdk:service:generic",
  "method_name": "DoCommand",
  "time_received": "2026-02-02T02:23:27.326Z",
  "data": {
    "docommand_output": {
      "label": "PASS",
      "confidence": 0.9999136328697205
    }
  },
  "additional_parameters": {
    "docommand_input": {
      "detect": true
    }
  },
  "organization_id": "...",
  "location_id": "...",
  "robot_id": "...",
  "part_id": "..."
}
```

The key fields for analysis are nested under `data.docommand_output`:

- `label`: The detection result—`PASS`, `FAIL`, or `NO_DETECTION`
- `confidence`: How confident the model is (0.0 to 1.0)

**Querying with MQL:**

You can also query using MQL (MongoDB Query Language), which is useful for aggregations. Select **MQL** in the Query interface. For example, to count failures by hour:

```javascript
[
  {
    $match: {
      component_name: "inspector-service",
      "data.docommand_output.label": "FAIL",
    },
  },
  {
    $group: {
      _id: { $dateTrunc: { date: "$time_received", unit: "hour" } },
      count: { $sum: 1 },
    },
  },
  { $sort: { _id: -1 } },
];
```

You'll use MQL aggregation pipelines in Part 5 to build dashboard widgets.

{{< alert title="Two types of captured data" color="info" >}}
You now have two complementary data streams:

- **Vision service images** (Part 2): Visual records for review and model retraining
- **Inspector tabular data** (this section): Queryable detection results for analytics

The images show what the system saw; the tabular data tracks what it decided.
{{< /alert >}}

## 4.5 Summary

You deployed your inspection logic as a Viam module:

1. **Reviewed**—the starter repo already provided module structure and registration
2. **Deployed**—set your namespace, built, packaged, uploaded, configured
3. **Configured data capture**—detection results are now queryable

**The development pattern:**

- During development: CLI runs locally, uses remote hardware (fast iteration)
- In production: Module runs on machine, same code (autonomous operation)

**Your inspection system now runs 24/7** detecting defects without your laptop connected.

**[Continue to Part 5: Productize →](../part-5/)**
