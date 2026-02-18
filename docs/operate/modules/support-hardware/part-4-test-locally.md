---
title: "Part 4: Test your module locally"
linkTitle: "Part 4: Test locally"
weight: 34
layout: "docs"
type: "docs"
description: "Test your module on a real machine before deploying to the registry."
---

**Part 4 of 5** | ⏱️ 20 minutes

## What you'll do in this part

- Add your module to a test machine using hot reload
- Configure your camera component
- Test the camera in the Viam app
- Learn the iteration workflow
- Troubleshoot common issues

You can test your module locally before uploading it to the [registry](https://app.viam.com/registry).

## Test with hot reload (recommended)

Hot reload is the fastest way to test your module. It automatically builds your module and deploys it to your machine for testing.

{{< alert title="Why hot reload?" color="tip" >}}
Hot reload handles cross-compilation automatically, so you can develop on your laptop (macOS/Windows) and test on a Raspberry Pi (Linux ARM) without any extra tools.
{{< /alert >}}

### Add module to your machine

Run the following command from your module directory to build and deploy your module:

{{< tabs >}}
{{% tab name="Same device" %}}

If you're developing on the same device where `viam-server` is running:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload-local --cloud-config /path/to/viam.json
```

Replace `/path/to/viam.json` with the path to your machine's cloud config file (usually in `/etc/viam/` on Linux or downloaded from the Viam app).

{{% /tab %}}
{{% tab name="Other device" %}}

If you're developing on a different device from where `viam-server` is running:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload --part-id 123abc45-1234-432c-aabc-z1y111x23a00
```

Replace the part ID with your machine's part ID. Find it by:
1. Go to your machine's page in the Viam app
2. Click the **Live** indicator
3. Click **Part ID** to copy it

{{% /tab %}}
{{< /tabs >}}

For more information, see the [`viam module` CLI documentation](/dev/tools/cli/#module).

The command will:
1. Build your module using your local architecture or the target machine's architecture
2. Package it with all dependencies
3. Use the shell service to copy it to your machine
4. Restart the module automatically

{{< alert title="Success!" color="note" >}}
You may need to refresh your machine page in the Viam app for your module to appear.
{{< /alert >}}

{{< expand "Troubleshooting hot reload" >}}

**Error: Could not connect to machine part: context deadline exceeded**

Try specifying the `--part-id` explicitly (find it on your machine's page by clicking **Live** → **Part ID**).

**Error: Rpc error: code = Unknown desc = stat /root/.viam/packages-local: no such file or directory**

Try specifying the `--home` directory:
```sh
viam module reload --part-id YOUR_PART_ID --home /Users/yourname/
```

**Error: Error while refreshing token, logging out. Please log in again**

Run `viam login` to reauthenticate the CLI.

**Still having problems?**

You can use manual testing (see below) as an alternative.

{{< /expand >}}

{{< expand "Alternative: Manual testing" >}}

If hot reload isn't working, you can manually add your module:

{{< tabs >}}
{{% tab name="Python" %}}

1. Navigate to your machine's **CONFIGURE** page
2. Click the **+** button, select **Local module**, then select **Local module** again
3. Enter the path to the `run.sh` script, for example: `/home/yourname/hello-world/run.sh`
4. Click **Create**
5. Save the config

For local modules, `viam-server` uses this path to start the module.

{{% /tab %}}
{{% tab name="Go" %}}

1. From your module directory, compile your module:
   ```sh {class="command-line" data-prompt="$"}
   viam module build local
   ```

2. Navigate to your machine's **CONFIGURE** page
3. Click the **+** button, select **Local module**, then select **Local module** again
4. Enter the path to the executable, for example: `/home/yourname/hello-world/bin/hello-world`
5. Click **Create**
6. Save the config

For local modules, `viam-server` uses this path to start the module.

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}

## Configure your component

Now that your module is added to your machine, configure a component that uses it:

1. On your machine's **CONFIGURE** page, click **+**
2. Select **Local module**, then **Local component**
3. Enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}}, for example: `exampleorg:hello-world:hello-camera`
   - You can find this in the `model` field of your `meta.json` file
4. Select **Camera** as the Type
5. Enter a Name, such as `camera-1`
6. Click **Create**

### Add configuration attributes

In the configuration panel that appears, add your model's required attributes.

For the camera model, replace `{}` with:

```json {class="line-numbers linkable-line-numbers"}
{
  "image_path": "/path/to/your/image.png"
}
```

Replace `/path/to/your/image.png` with an actual path to an image file on your machine.

{{< alert title="Tip" color="tip" >}}
Make sure the image file exists and `viam-server` has permission to read it!
{{< /alert >}}

Save the config and wait a few seconds for it to apply.

## Test your component

Click the **TEST** section at the bottom of your camera's configuration card.

If everything is working correctly, you should see your image displayed in the test panel!

{{<imgproc src="/how-tos/hello-camera.png" resize="x1100" declaredimensions=true alt="The configuration interface with the Test section of the camera card open, showing a hello world image." style="width:800px" class="shadow aligncenter" >}}

### If you see errors

Errors will appear in:
- The configuration panel (red banner)
- The **LOGS** tab (click **LOGS** in the top navigation)

Common issues:
- **"Missing image_path attribute"**: Add `image_path` to your config JSON
- **"Error opening image"**: Check that the file path is correct and readable
- **Module not found**: Refresh the page or restart the module

## Iterate on your module

Each time you make changes to your module code, update it on your machine:

{{< tabs >}}
{{% tab name="Hot reload (recommended)" %}}

Run the reload command again:

{{< tabs >}}
{{% tab name="Same device" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload-local --cloud-config /path/to/viam.json
```

{{% /tab %}}
{{% tab name="Other device" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload --part-id 123abc45-1234-432c-aabc-z1y111x23a00
```

{{% /tab %}}
{{< /tabs >}}

Your machine may already have a previously published version of the module you're iterating on. If so, you can toggle **Hot Reloading** on and off in the module's configuration card in the Viam app:
- **On**: Uses your local development version
- **Off**: Uses the published registry version

{{% /tab %}}
{{% tab name="Manual testing" %}}

{{< tabs >}}
{{% tab name="Python" %}}

Save your code changes, then restart the module in your machine's **CONFIGURE** tab:

1. Find the module's card
2. Click the **...** menu in the upper-right corner
3. Click **Restart**

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="width:300px" class="shadow" >}}

{{% /tab %}}
{{% tab name="Go" %}}

1. Rebuild your module:
   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module build local
   ```

2. Restart it in your machine's **CONFIGURE** tab:
   - Find the module's card
   - Click the **...** menu
   - Click **Restart**

{{<imgproc src="/registry/restart-module.png" resize="x600" declaredimensions=true alt="Module menu." style="max-width:300px" class="shadow" >}}

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

### Development workflow

The typical development cycle:

1. **Edit code** in your module files
2. **Reload/restart** the module on your machine
3. **Test** using the TEST panel or Viam app
4. **Check logs** if something doesn't work
5. **Repeat** until it works as expected

{{< alert title="Debugging tip" color="tip" >}}
Use logging in your module code to help debug. Logs appear in the **LOGS** tab in the Viam app.

Python: `logger.info("Message")`
Go: `logger.Info("Message")`
{{< /alert >}}

## What you've accomplished

✅ **Module deployed:**
- Used hot reload to build and deploy your module
- Module running on a real machine

✅ **Component configured:**
- Added camera component with proper configuration
- Verified configuration validation works

✅ **Testing complete:**
- Tested camera in Viam app
- Confirmed images are returned correctly

✅ **Ready for more:**
- Understand the iteration workflow
- Know how to debug issues

## Next steps

Your module works! Now you have two options:

1. **Ready to deploy?** Once you've thoroughly tested your module, continue to [Package and deploy your module](/operate/modules/deploy-module/) to upload it to the registry
2. **Want to add more models?** Continue to [Part 5: Multiple models](/operate/modules/support-hardware/part-5-multiple-models/) to learn how to add the sensor model to your module

---

**Tutorial navigation:**
- **Previous:** [← Part 3: Implement your module](/operate/modules/support-hardware/part-3-implement-single-model/)
- **Current:** Part 4: Test your module locally
- **Next:** [Part 5: Multiple models (advanced) →](/operate/modules/support-hardware/part-5-multiple-models/) or [Deploy to registry →](/operate/modules/deploy-module/)
- **All parts:** [Module creation tutorial](/operate/modules/support-hardware/)
