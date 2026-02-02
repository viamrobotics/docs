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

The module generator already created most of what you need:

- `cmd/module/main.go`—module entry point
- `meta.json`—registry metadata
- Model registration in `init()`

You just need to build, package, and deploy.

## 4.1 Review the Generated Module Structure

The generator already created everything needed to run as a module. Let's review what's there.

**`cmd/module/main.go`**

```go
func main() {
    module.ModularMain(
        resource.APIModel{API: generic.API, Model: inspectionmodule.Inspector},
    )
}
```

This connects your module to viam-server and registers the inspector model. When you add this service to your machine configuration, viam-server uses this entry point to create and manage instances. You don't need to modify it.

**`module.go`** provides model registration in `init()`:

The generator created an `init()` function that registers your model:

```go
var Inspector = resource.NewModel("your-namespace", "inspection-module", "inspector")

func init() {
    resource.RegisterService(generic.API, Inspector,
        resource.Registration[resource.Resource, *Config]{
            Constructor: newInspectionModuleInspector,
        },
    )
}
```

This runs automatically when the module starts, telling viam-server how to create instances of your service.

**`meta.json`** Registry metadata:

```json
{
  "module_id": "your-namespace:inspection-module",
  "visibility": "private",
  "models": [
    {
      "api": "rdk:service:generic",
      "model": "your-namespace:inspection-module:inspector"
    }
  ],
  "entrypoint": "bin/inspection-module"
}
```

This tells the registry what your module provides.

{{< alert title="The key pattern" color="tip" >}}
The generator created module infrastructure. You added business logic (`detect`) and exposed it through `DoCommand`. The same `NewInspector` constructor works for both CLI testing and module deployment.
{{< /alert >}}

## 4.2 Build and Deploy

**Build the module binary:**

```bash
make
# Or manually: go build -o bin/inspection-module ./cmd/module
```

**Package for upload:**

```bash
tar czf module.tar.gz meta.json bin/
```

**Upload to the registry:**

```bash
viam module upload --version 1.0.0 --platform linux/amd64 --upload module.tar.gz
```

{{< alert title="Note" color="info" >}}
Use `linux/arm64` for ARM machines (like Raspberry Pi).
{{< /alert >}}

**Add the module to your machine:**

1. In the Viam app, go to your machine's **Configure** tab
2. Click **+** next to your machine
3. Select **Local module**, then **Local module**
4. Search for your module name (for example, `your-namespace:inspection-module`)
5. Click **Add module**

**Add the inspector service:**

1. Click **+** next to your machine
2. Select **Service**, then **generic**
3. For **Model**, select your model (for example, `your-namespace:inspection-module:inspector`)
4. Name it `inspector`
5. Click **Create**

**Configure the service attributes:**

```json
{
  "camera": "inspection-cam",
  "vision": "vision-service"
}
```

Click **Save**.

**Verify it's running:**

1. Go to the **Logs** tab
2. Look for log messages from the inspector module
3. You should see it starting and connecting to dependencies

The inspector now runs on the machine autonomously.

## 4.3 Configure Detection Data Capture

In Part 2, you captured images from the vision service. Those images are great for visual review, but they're binary data—you can't query them with SQL. Now you'll configure **tabular data capture** on your inspector's DoCommand, which will let you query detection results.

**Enable data capture on the inspector:**

1. In the **Configure** tab, click on `inspector` to open its configuration panel
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
4. Run a query to find all failures:

```sql
SELECT time_received, data
FROM readings
WHERE component_name = 'inspector'
  AND method_name = 'DoCommand'
ORDER BY time_received DESC
LIMIT 10
```

You can also filter by detection results:

```sql
SELECT time_received, data
FROM readings
WHERE component_name = 'inspector'
  AND data.label = 'FAIL'
ORDER BY time_received DESC
LIMIT 10
```

{{< alert title="Two types of captured data" color="info" >}}
You now have two complementary data streams:

- **Vision service images** (Part 2): Visual records for review and model retraining
- **Inspector tabular data** (this section): Queryable detection results for analytics

The images show what the system saw; the tabular data tracks what it decided.
{{< /alert >}}

## 4.4 Summary

You deployed your inspection logic as a Viam module:

1. **Reviewed**—the generator already created module structure and registration
2. **Deployed**—built, packaged, uploaded, configured
3. **Configured data capture**—detection results are now queryable

**The development pattern:**

- During development: CLI runs locally, uses remote hardware (fast iteration)
- In production: Module runs on machine, same code (autonomous operation)

**Your inspection system now runs 24/7** detecting defects without your laptop connected.

**[Continue to Part 5: Scale →](../part-5/)**
