---
title: "Use Fragments to Configure a Fleet of Machines"
linkTitle: "Configure a Fleet"
weight: 40
type: "docs"
description: Use fragments to configure many machines at the same time.
tags: ["fleet management", "cloud", "app"]
aliases:
  - /fleet/configure-a-fleet/
---

{{< cards >}}
{{% card link="/use-cases/one-to-many/" %}}
{{< /cards >}}

If you have multiple machines with similar configurations, you can use a _fragment_ to configure all of the machines at the same time.
Fragments are a way of sharing and managing [machine configurations](/configure/) across multiple machines.

If there are differences between your machines, you can use a fragment to quickly configure the {{< glossary_tooltip term_id="resource" text="resources" >}} that are the same between machines.
You can then configure the differing resources separately, outside of the fragment.
For example, if you have multiple similar rovers but one has an arm attached, you can add the rover configuration fragment (including the motors and base components), and then configure the arm on just that one rover.

When you or one of your collaborators edit a fragment that you've already deployed to one or more machines, the Viam app updates the configuration on each deployed machine that uses that fragment.

{{< alert title="Alert" color="alert" >}}
Be cautious when making changes to fragments that have been deployed to production machines.
We recommend that you create a duplicate fragment, make your desired change to that second fragment, and then deploy that fragment to a test machine that is configured identically to your production machines.

Once you are confident that your configuration change works as expected, you can safely make the same change to the fragment in use on your production fleet, and the Viam app will deploy that change to all machines using that fragment.
{{< /alert >}}

If you attempt to delete a fragment that is currently deployed to a machine, you will receive an error message advising that the fragment is in use, but you can still delete the fragment if desired.
You can see the number of machines using your fragment from the [fragments page](https://app.viam.com/fragments) in the Viam app.

You must be an [organization owner](/cloud/rbac/#permissions) to create fragments associated with a given organization.

A fragment can define one, several, or all resources on a machine.
You can add multiple fragments to a single machine, and you can add additional resources to a machine that has already been configured with a fragment.

## Modify the config of a machine that uses a fragment

The configuration of components and services included in a fragment are _read-only_.
Likewise, when you modify the fragment itself, any changes are pushed to all machines that use that fragment.

If you need to modify the config of just one machine that uses a fragment, you have two options:

- Use `fragment_mods` in your machine's config to overwrite certain fields of the fragment.
- Copy and paste the contents of the fragment, remove the link to the fragment itself, then modify the config as needed.
  - If you use this method, future updates to the fragment _will not_ be automatically pushed to your machine.

{{% alert title="Support Notice" color="note" %}}

`fragment_mods` are _not_ supported for the modification of [trigger](/configure/triggers/) configuration.
You can create a trigger with a fragment but you cannot modify it with `fragment_mods`.

{{% /alert %}}

### Use `fragment_mods`

{{< tabs >}}
{{% tab name="Config Builder" %}}

When you make edits to the configuration of component or service that was configured using a fragment, the Viam app builder automatically adds an overwrite to your config.
If you have made edits, you will see an **edited from FRAGMENT NAME** indicator in the upper right corner of the edited component or service card.

![A motor config card with "edited from SCUTTLE101" in the upper right corner.](/fleet/fragment-edited.png)

{{% /tab %}}
{{% tab name="Raw JSON" %}}

You can modify fragment fields in your machine's raw JSON config by using [update operators](https://www.mongodb.com/docs/manual/reference/operator/update/positional/#---update-).
Viam supports all update operators except for `$setOnInsert`, `$`, `$[]`, and `$[<identifier>]`.

To configure fragment mods manually instead of using the builder UI:

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
This example uses [`$set`](https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set) to set [version update settings for a module](/registry/configure/#edit-the-configuration-of-a-module-from-the-viam-registry) named `custom-sensor` in the fragment:

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

### Revert fragment mods

If you need to restore the original fragment, click the **...** in the upper right corner of the card you modified, and click **Revert changes**.

### Copy and paste method

1. Navigate to the card belonging to your fragment on the **CONFIGURE** tab.
2. Click the **View JSON** button in the upper right corner of the card.
   Copy all of the JSON.
3. Return to the fragment card.
   Click the **...** (Actions) button in the upper right corner of the card. Click **Delete** and confirm your choice.
4. In the left-hand menu of the **CONFIGURE** tab, click **JSON** to switch to JSON mode.
5. Paste the raw fragment contents into the editor and click **Save** in the upper-right corner of the screen to save your config.
6. Now, you can edit the config in either **JSON** or **Builder** mode.

## Next steps

Viam provides several [pre-made fragments](https://app.viam.com/fragments) which you can use as templates for writing your own fragments.

For an example of a fragment that configures multiple components and services, see the [Viam Rover fragment](https://app.viam.com/fragment?id=3e8e0e1c-f515-4eac-8307-b6c9de7cfb84).

For an example of creating a fragment and using it to configure a fleet of machines, see the air quality fleet tutorial:

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}
