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
languages: []
viamresources: []
platformarea: ["fleet"]
level: "Beginner"
date: "2024-08-09"
# updated: ""  # When the tutorial was last entirely checked
next: /manage/fleet/provision/setup/
cost: "0"
---

If most of your machines use the same setup, you can use a {{< glossary_tooltip term_id="fragment" text="fragment" >}}, like a cookie cutter, to configure the machines in the same way.
Fragments are a way of sharing and managing [machine configurations](/configure/) across multiple machines.

For example, if you have a fleet of rovers that uses the same hardware, you could use a fragment to configure the motors, base component, camera, and all other resources for all rovers.
If some of the rovers have a slightly different configuration, you can overwrite the configuration for just those {{< glossary_tooltip term_id="resource" text="resources" >}} of those rovers.

If one rover has an arm attached, you can add the rover configuration fragment (including the motors, camera, and base components), and then configure the arm on just that one rover.

## Create a fragment

You must be an [organization owner](/cloud/rbac/#permissions) to create fragments for an organization.

{{< table >}}
{{% tablestep link="/configure/" %}}
**1. Configure one machine**

Start by configuring one of your machines.

In the [Viam app](https://app.viam.com), use the **CONFIGURE** tab to build a configuration for all resources you want to use on all your machines.

{{<imgproc src="/how-tos/one-to-many/config.png" resize="800x" class="fill aligncenter" style="width: 400px" declaredimensions=true alt="Configuration builder UI">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Copy the raw JSON**

In your machine's **CONFIGURE** tab, switch to **JSON** and copy the raw JSON.

{{<imgproc src="/how-tos/one-to-many/raw-json.png" resize="700x" class="fill aligncenter" style="width: 400px" declaredimensions=true alt="JSON subtab of the CONFIGURE tab">}}

{{% /tablestep %}}
{{% tablestep link="/fleet/fragments/" %}}
**3. Create a fragment**

On the **FLEET** page, go to the [**FRAGMENTS** tab](https://app.viam.com/fragments).

Click **Create fragment**, and paste the copied JSON configuration into it.

Set your privacy settings.
There are three options for this:

- **Public:** Any user inside or outside of your organization will be able to view and use this fragment.
- **Private:** No user outside of your organization will be able to view or use this fragment.
- **Unlisted:** Any user inside or outside of your organization, with a direct link, will be able to view and use this fragment.

Click **Save**.

If you want to edit the fragment later, do it from this screen.

{{<imgproc src="/how-tos/one-to-many/new-fragment.png" resize="700x" class="fill aligncenter" style="width: 350px" declaredimensions=true alt="app.viam.com/fragment interface">}}

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/delete.png" class="fill alignleft" resize="500x" style="width: 200px" declaredimensions=true alt="Delete">}}
**4. Delete the original configuration (optional)**

Now that the configuration is saved as a fragment, you can delete each resource in the original config from your machine and _replace the config with the fragment_ in the next step.
By using the new fragment, all your machines will use the exact same configuration.

{{% /tablestep %}}
{{< /table >}}

## Add the fragment to multiple machines

With your fragment created, you can add it to all machines that should have it.

In the following, you will see how to add a fragment manually. If you are working in a factory setting and need to set up devices before they reach the end user, you can also fragments while [provisioning](/manage/fleet/provision/setup/) your fleet.

{{< table >}}
{{% tablestep %}}
{{<imgproc src="appendix/try-viam/rover-resources/fragments/fragments_list.png" resize="800x" class="fill alignleft imgzoom" style="width: 250px" declaredimensions=true alt="Add fragment">}}
**1. Add the fragment to one machine**

On your machine's **CONFIGURE** tab, click the **+** button and select **Insert fragment**.
Search for your fragment and add it.

Click **Save** in the upper right corner of the screen.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/repeat.svg" class="fill alignleft" style="width: 120px"  declaredimensions=true alt="Repeat">}}
**2. Repeat for each machine**

Repeat step 1 for each of the machines that you want to configure in the same way.

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
{{% tablestep link="/fleet/fragments/#modify-the-config-of-a-machine-that-uses-a-fragment" %}}

<!-- markdownlint-disable MD036 -->

**1. Edit your machine's config**

{{< tabs >}}
{{% tab name="Config Builder" %}}

Go to the **CONFIGURE** tab of the machine whose config you want to modify, and make your edits just as you would edit a non-fragment {{< glossary_tooltip term_id="resource" text="resource" >}}.

You can click the **{}** button to switch to advanced view and see the changes.

Click **Save**.

{{<gif webm_src="/how-tos/fragment-overwrite.webm" mp4_src="/how-tos/fragment-overwrite.mp4" alt="A motor config panel from a fragment being edited with different direction and pwm pin values." max-width="500px" class="aligncenter" >}}

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
         "components.motor1.attributes.board": "local"
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
This example uses [`$set`](https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set) to change the sync interval for a [data management service](/services/data/) named `data-management` in the fragment:

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
{{< expand "Pin a module version" >}}
This example uses [`$set`](https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set) to set [version update settings for a module](/registry/modular-resources/#configuration) named `custom-sensor` in the fragment:

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

Here are the version options:

- To update with new minor releases of the same major release branch, use `"^<major version number>"`, for example `"^1"`
- To update with new patch releases of the same minor release branch, use `"~<minor version number>"`, for example `"~1.8"`
- To always update with the latest release, use `"latest"`
- To pin to a specific release, use `"<version number>"`, for example `"1.8.3"`

{{< /expand >}}

6. Click **Save** in the upper right corner of the page to save your new configuration.
7. To check that your mods are working, view your machine's debug configuration.
   In **Builder** mode on the **CONFIGURE** tab, select the **...** (Actions) menu to the right of your main part's name in the left-hand panel and click the **View debug configuration** option to view the full configuration file.

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Support Notice" color="note" %}}

Fragment overwrites are currently _not_ supported for modifying [triggers](/configure/triggers/).

{{% /alert %}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Check your machine's logs**

After configuring fragment overwrites, check your machine's [**LOGS** tab](/cloud/machines/#logs).

If there are problems with overwrites to the fragment, the overwrites will not be partially applied and the configuration changes will not take effect until the configuration is fixed.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/reset.png" class="fill alignleft" resize="500x" style="width: 250px"  declaredimensions=true alt="Reset to fragment">}}
**3. (Optional) Revert fragment modifications**

If you need to restore the original fragment, click the **...** in the upper right corner of the card you modified, and click **Revert changes**.
Now, the fragment will be identical to the upstream fragment.

{{% /tablestep %}}
{{< /table >}}

## Update a fragment

You and your collaborators can edit a fragment at any time.

If you've already deployed the fragment to one or more machines, the Viam app updates the configuration on each deployed machine that uses that fragment.
You can see the number of machines using your fragment from the [fragments page](https://app.viam.com/fragments) in the Viam app.

{{< alert title="Test updates first" color="caution" >}}
Be cautious when making changes to fragments that have been deployed to production machines.

We recommend that you create a duplicate fragment, make your desired change to that second fragment, and then deploy that fragment to one or more test machines that are configured identically to your production machines.

Once you are confident that your configuration change works as expected, you can safely make the same change to the fragment in use on your production fleet, and the Viam app will deploy that change to all machines using that fragment.
{{< /alert >}}

## Example fragments

For an example of a fragment that configures multiple components and services, see the [Viam Rover fragment](https://app.viam.com/fragment?id=3e8e0e1c-f515-4eac-8307-b6c9de7cfb84).

For an example of creating a fragment and using it to configure a fleet of machines, see the [air quality fleet tutorial](/tutorials/control/air-quality-fleet/).
