---
title: "Reuse machine configuration on many machines"
linkTitle: "Reuse machine configuration"
weight: 20
type: "docs"
tags: ["data management", "data", "services"]
images: ["/how-tos/one-to-many/new-fragment.png"]
description: "Reuse the machine configuration from one machine for multiple machines."
aliases:
  - /use-cases/one-to-many/
  - /how-tos/one-to-many/
  - /fleet/fragments/
  - /fleet/configure-a-fleet/
languages: []
viamresources: []
platformarea: ["fleet"]
level: "Beginner"
date: "2025-02-07"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

If most of your machines use the same setup, you can use a {{< glossary_tooltip term_id="fragment" text="fragment" >}}, like a cookie cutter, to configure the machines in the same way.
Fragments are a way of sharing and managing [machine configurations](/operate/get-started/supported-hardware/) across multiple machines.

For example, if you have a fleet of rovers that uses the same hardware, you could use a fragment to configure the motors, base component, camera, and all other resources for all rovers.
If some of the rovers have a slightly different configuration, you can overwrite the configuration for just those {{< glossary_tooltip term_id="resource" text="resources" >}} of those rovers.
If one rover has an arm attached, you can add the rover configuration fragment (including the motors, camera, and base components), and then configure the arm on just that one rover.

## Create a fragment

You must be an [organization owner](/manage/manage/rbac/) to create fragments for an organization.

{{< table >}}
{{% tablestep start=1 %}}
**Go to the [FRAGMENTS page](https://app.viam.com/fragments) and create a fragment** in your {{< glossary_tooltip term_id="organization" text="organization" >}}.

{{% /tablestep %}}
{{% tablestep %}}
**Add and configure all the resources** you want to use on your machines.

Fragments support all available resources except [triggers](/data-ai/reference/triggers-configuration/).
You can also add other fragments inside a fragment.

{{< alert title="Tip: Switch to JSON" color="tip" >}}
If you already created a machine to test your configuration, you can **Switch to JSON**, copy its JSON configuration and paste it into the fragment.

{{<imgproc src="/how-tos/one-to-many/raw-json.png" resize="700x" class="shadow fill" style="width: 400px" declaredimensions=true alt="JSON subtab of the CONFIGURE tab">}}
{{< /alert >}}

{{% /tablestep %}}
{{% tablestep %}}
**Set your privacy settings in the menu bar.**
There are three options for this:

- **Public:** Any user inside or outside of your organization will be able to view and use this fragment.
- **Private:** No user outside of your organization will be able to view or use this fragment.
- **Unlisted:** Any user inside or outside of your organization, with a direct link, will be able to view and use this fragment.

Click **Save**.

{{% /tablestep %}}
{{% tablestep %}}
**Add a description**

While not required, we recommend you add a description to your fragment from the fragment's page.

{{% /tablestep %}}
{{< /table >}}

{{< alert title="Tip: Organize resources into folders" color="tip" >}}

If you have many components and services in one fragment, you can add folders to your fragment and use them to organize the resources.

{{< /alert >}}

## Add the fragment to multiple machines

With your fragment created, you can add it to all machines that should have it.

In the following steps, you will see how to add a fragment manually. If you are working in a factory setting and need to set up devices before they reach the end user, you can also use fragments to [provision](/manage/fleet/provision/setup/) your machines.

{{< table >}}
{{% tablestep start=1 %}}
**On your machine's CONFIGURE tab, click the + button and select Insert fragment.**

Search for your fragment and add it.

Click **Save** in the upper right corner of the screen.

{{% /tablestep %}}
{{% tablestep %}}
**Repeat step 1 for each of the machines** that you want to configure in the same way.

If some of your machines have slight differences, you can still add the fragment and then add fragment overwrites in the next section.

{{% /tablestep %}}
{{< /table >}}

## Modify fragment settings on a machine

If some of your machines are similar but not identical, you can use a fragment with all of them and then overwrite parts of the configuration to customize it **without modifying the upstream fragment**.

For example, consider a fleet of rovers that all have the same motors, wheels, and base but a few rovers have a different camera than most.
You can configure a fragment that has the motors, wheels, base on the rovers as well as the camera that is used on most rovers.
For the rovers that have a different camera, you would then add the fragment and overwrite the camera configuration.

If you or a collaborator later modify fields within the upstream fragment, your modifications will still apply.
For example if you changed the default camera configuration in the fragment to be a different camera model, your modified rovers would still overwrite the camera model set by the fragment.

{{< table >}}
{{% tablestep start=1 %}}

<!-- markdownlint-disable MD036 -->

**On the CONFIGURE tab of the machine whose config you want to modify, make your edits** just as you would edit a non-fragment {{< glossary_tooltip term_id="resource" text="resource" >}}.

{{< tabs >}}
{{% tab name="Config Builder" %}}

You can click the **{}** button to switch to advanced view and see the changes.

Click **Save**.

{{<gif webm_src="/how-tos/fragment-overwrite.webm" mp4_src="/how-tos/fragment-overwrite.mp4" alt="A motor config panel from a fragment being edited with different direction and pwm pin values." max-width="500px" class="" >}}

{{% /tab %}}
{{% tab name="JSON" %}}

You can modify fragment fields in your machine's raw JSON config by using [update operators](https://www.mongodb.com/docs/manual/reference/operator/update/positional/#---update-).
Viam supports all update operators except for `$setOnInsert`, `$`, `$[]`, and `$[<identifier>]`.

To configure fragment overwrites manually instead of using the builder UI:

1. Navigate to your machine's **CONFIGURE** tab.
2. Switch to **JSON** mode.
3. Add a top-level section called `"fragment_mods"` (alongside the other top-level sections like `"components"` and `"fragments"`):

{{< tabs >}}
{{% tab name="Template" %}}

```json {class="line-numbers linkable-line-numbers"}
  "fragment_mods": [
    {
      "fragment_id": "<YOUR FRAGMENT ID>",
      "mods": [
        {
          <INSERT YOUR MODS HERE>
        }
      ]
    }
  ],
```

{{% /tab %}}
{{% tab name="Full example" %}}
This example assumes the fragment with ID `abcd7ef8-fa88-1234-b9a1-123z987e55aa` contains a motor configured with `"name": "motor1"`.

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [],
  "fragment_mods": [
    {
      "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
      "mods": [
        {
          "$set": {
            "components.motor1.attributes.max_rpm": 1818,
            "components.motor1.attributes.pins.a": 30,
            "components.motor1.attributes.board": "local"
          }
        },
        {
          "$unset": {
            "components.motor1.attributes.pins.pwm": 0
          }
        }
      ]
    }
  ],
  "fragments": ["abcd7ef8-fa88-1234-b9a1-123z987e55aa"]
}
```

{{% /tab %}}
{{< /tabs >}}

4. Edit the `fragment_id` value to match the ID of the fragment you want to modify, for example `"12345678-1a2b-9b8a-abcd987654321"`.
5. Add any update operators you'd like to apply to the fragment to the `mods` section.
   Click to view each example:

{{< expand "Change the name and attributes of a component" >}}
This example uses [`$set`](https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set) to make the following changes to the attributes of a motor named `motor1`:

- Sets the `max_rpm` to `1818`.
- Changes the name of `motor1` to `my_motor`.
  Note that this does not affect the other mods; you still use `motor1` for them.
- Sets the pin number for pin `a` to `30`.
- Sets the name of the board associated with this motor to `local`.
- Sets the `capture_frequency_hz` in the `service_config` for the first capture method in the `capture_methods` array.

```json {class="line-numbers linkable-line-numbers"}
"fragment_mods": [
 {
   "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
   "mods": [
     {
       "$set": {
         "components.motor1.attributes.max_rpm": 1818,
         "components.motor1.name": "my_motor",
         "components.motor1.attributes.pins.a": 30,
         "components.motor1.attributes.board": "local",
         "components.motor1.service_configs.0.attributes.capture_methods.0.capture_frequency_hz": 0.25
        }
     }
   ]
 }
],
```

{{< /expand >}}
{{< expand "Remove an attribute" >}}
This example uses [`$unset`](https://www.mongodb.com/docs/manual/reference/operator/update/unset/#mongodb-update-up.-unset) to remove the pin number set for the `pwm` pin, so the motor no longer has a PWM pin set.
In other words, it deletes the `pwm` pin field.

```json {class="line-numbers linkable-line-numbers"}
"fragment_mods": [
  {
    "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
    "mods": [
      {
       "$unset": {
         "components.motor1.attributes.pins.pwm": 0
       }
      }
    ]
  }
],
```

{{< /expand >}}
{{< expand "Modify dependencies" >}}
This example uses [`$set`](https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set) to assign a new list of dependencies to a component named `rover_base2`.

```json {class="line-numbers linkable-line-numbers"}
"fragment_mods": [
  {
    "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
    "mods": [
      {
       "$set": {
         "components.rover_base2.attributes.depends_on": ["local", "motor1"]
       }
      }
    ]
  }
],
```

{{< /expand >}}
{{< expand "Change motor pins from A and B to PWM and DIR" >}}
This example uses [`$rename`](https://www.mongodb.com/docs/manual/reference/operator/update/rename/) to make the following changes to the attributes of a motor named `motor1` in the fragment:

- Retrieves the pin number for pin `a` and assigns that value to the PWM pin.
  Deletes the `pins.a` field.
- Retrieves the pin number for pin `b` and assigns that value to the DIR pin.
  Deletes the `pins.b` field.

_`$rename` is for changing an attribute's key, not its value.
If you want to change the `name` of a component (for example, `motor1`), use `$set`, as shown in the change the name of a component example._

```json {class="line-numbers linkable-line-numbers"}
"fragment_mods": [
 {
   "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
   "mods": [
     {
       "$rename": {
         "components.motor1.attributes.pins.a": "components.motor1.attributes.pins.pwm",
         "components.motor1.attributes.pins.b": "components.motor1.attributes.pins.dir"
       }
     }
   ]
 }
],
```

{{< /expand >}}
{{< expand "Change a camera path" >}}
This example uses [`$set`](https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set) to change the video path for a camera named `camera-one` in the fragment:

```json {class="line-numbers linkable-line-numbers"}
"fragment_mods": [
  {
    "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
    "mods": [
      {
        "$set": {
          "components.camera-one.attributes.video_path": "0x11100004a12345"
        }
      }
    ]
  }
],
```

{{< /expand >}}
{{< expand "Modify data sync settings" >}}
This example uses [`$set`](https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set) to change the sync interval for a [data management service](/data-ai/capture-data/capture-sync/) named `data-management` in the fragment:

```json {class="line-numbers linkable-line-numbers"}
"fragment_mods": [
  {
    "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
    "mods": [
      {
        "$set": {
          "services.data-management.attributes.sync_interval_mins": "0.5"
        }
      }
    ]
  }
],
```

{{< /expand >}}
{{< expand "Set a module version" >}}
This example uses [`$set`](https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set) to configure [version update settings for a module](/operate/get-started/other-hardware/module-configuration/#module-configuration-details) named `custom-sensor` from the fragment:

```json {class="line-numbers linkable-line-numbers"}
"fragment_mods": [
  {
    "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
    "mods": [
      {
        "$set": {
          "modules.custom-sensor.version": "1.8.0"
        }
      }
    ]
  }
],
```

The `version` field supports the following values:

- To update with new minor releases of the same major release branch, use `"^<major version number>"`, for example `"^1"`
- To update with new patch releases of the same minor release branch, use `"~<minor version number>"`, for example `"~1.8"`
- To always update with the latest release, use `"latest"`
- To pin to a specific release, use `"<version number>"`, for example `"1.8.3"`

{{< /expand >}}
{{< expand "Set a package version" >}}
This example uses [`$set`](https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set) to configure [version update settings for a package](/data-ai/ai/deploy/#deploy-a-specific-version-of-an-ml-model) named `package_name` from the fragment:

```json {class="line-numbers linkable-line-numbers"}
"fragment_mods": [
  {
    "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
    "mods": [
      {
        "$set": {
          "packages.package_name.version": "latest"
        }
      }
    ]
  }
],
```

The `version` field supports the following values:

- To update with new minor releases of the same major release branch, use `"^<major version number>"`, for example `"^1"`
- To update with new patch releases of the same minor release branch, use `"~<minor version number>"`, for example `"~1.8"`
- To always update with the latest release, use `"latest"`
- To pin to a specific release, use `"<version number>"`, for example `"1.8.3"`

{{< /expand >}}
{{< expand "Change the log level of a resource" >}}
This example uses [`$set`](https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set) to modify [the log level](/operate/reference/viam-server/#logging) from the fragment for a resource:

```json {class="line-numbers linkable-line-numbers"}
"fragment_mods": [
  {
    "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
    "mods": [
      {
        "$set": {
          "components.control.log_configuration.level": "debug"
        }
      }
    ]
  }
],
```

If the resource comes from a module, you must instead set the `log_level` attribute on the module itself:

```json {class="line-numbers linkable-line-numbers"}
"fragment_mods": [
  {
    "fragment_id": "abcd7ef8-fa88-1234-b9a1-123z987e55aa",
    "mods": [
      {
        "$set": {
          "modules.my-control-logic.log_level":  "debug"
        }
      }
    ]
  }
],
```

{{< /expand >}}

6. Click **Save** in the upper right corner of the page to save your new configuration.
7. To check that your mods are working, view your machine's debug configuration.
   In **Builder** mode on the **CONFIGURE** tab, select the **...** (Actions) menu to the right of your main part's name in the left-hand panel and click the **View debug configuration** option to view the full configuration file.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}
**After configuring fragment overwrites, check your machine's [**LOGS** tab](/manage/troubleshoot/troubleshoot/#check-logs).**

If there are problems with overwrites to the fragment, the overwrites will not be partially applied and the configuration changes will not take effect until the configuration is fixed.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/reset.png" class="shadow fill alignleft" resize="500x" style="width: 250px"  declaredimensions=true alt="Reset to fragment">}}
**(Optional) Revert fragment modifications.**

If you need to restore the original fragment, click the **...** in the upper right corner of the card you modified, and click **Revert changes**.
Now, the fragment will be identical to the upstream fragment.

{{% /tablestep %}}
{{< /table >}}

## Update a fragment

You and your collaborators can edit a fragment at any time.
Viam automatically creates new versions of your fragment as you make changes.
Fragments can only be deleted if no machines are using them.

If you've already deployed the fragment to one or more machines, Viam updates the configuration on each deployed machine that uses that fragment.
You can see the number of machines using your fragment from the [fragments page](https://app.viam.com/fragments).

{{< alert title="Test updates first" color="caution" >}}
We recommend testing updates to fragments on a small number of machines before deploying them to a larger fleet.
For recommendations on updating software on deployed machines, see [Update software](/manage/software/update-software/).
{{< /alert >}}

### Create fragment tags

You can create tags to differentiate between versions of your fragment.
For example, you may want to create a tag for `stable` and `beta`.

1. Go to the [FRAGMENTS tab](https://app.viam.com/fragments) and click on a fragment.
1. Click on **Versions** in the menu bar.
1. Click **Add Tag**.
1. Select a version to pin the tag to.
   You can change this later.
1. Type in a name for your tag.

### Pin to a fragment version or tag

When you add a fragment to a machine you can choose to pin the fragment version to use:

- the **latest version**: Always update to the latest version of this fragment as soon as a new version becomes available.
  This is the default.
- a **specific version**: Do not update to any other version.
- a **tag**: Always use the version of this fragment with the selected tag.
  For example `stable` or `beta`.

## Example fragments

For an example of a fragment that configures multiple components and services, see the [Viam Rover fragment](https://app.viam.com/fragment?id=3e8e0e1c-f515-4eac-8307-b6c9de7cfb84).

For an example of creating a fragment and using it to configure a fleet of machines, see the [air quality fleet tutorial](/tutorials/control/air-quality-fleet/).
