---
title: "Fragments"
linkTitle: "Fragments"
weight: 15
type: "docs"
tags: ["fleet management", "configuration", "fragments"]
description: "Use fragments to manage configuration across multiple machines."
platformarea: ["fleet"]
level: "Beginner"
date: "2026-02-18"
---

Imagine you're deploying 50 rovers, each with the same motors, camera, and base configuration.
Normally, you'd need to configure each machine individually, creating 50 identical copies of the same configuration.
When you need to change a setting, you'd have to update all 50 machines manually.

Fragments solve this problem by allowing you to define a configuration once and reuse it across multiple machines.

## What are fragments?

Fragments are reusable configuration blocks that you define once and deploy to as many {{< glossary_tooltip term_id="machine" text="machines" >}} as needed. They are stored centrally in your {{< glossary_tooltip term_id="organization" text="organization" >}}. They contain the same types of {{< glossary_tooltip term_id="resource" text="resources" >}} as machine configurations: {{< glossary_tooltip term_id="component" text="components" >}}, {{< glossary_tooltip term_id="service" text="services" >}}, {{< glossary_tooltip term_id="module" text="modules" >}}, and triggers.

Fragments are structured as JSON configurations, identical in format to machine configs.
This means anything you can configure on a single machine can be packaged into a fragment and shared across your fleet.

### Example fragment configuration

Here's an example fragment for the rover scenario:

```json
{
  "components": [
    {
      "name": "left-motor",
      "model": "gpio",
      "api": "rdk:component:motor",
      "attributes": {
        "pins": {
          "a": "12",
          "b": "11",
          "pwm": "33"
        },
        "board": "local"
      },
      "depends_on": ["local"]
    },
    {
      "name": "right-motor",
      "model": "gpio",
      "api": "rdk:component:motor",
      "attributes": {
        "pins": {
          "a": "16",
          "b": "15",
          "pwm": "32"
        },
        "board": "local"
      },
      "depends_on": ["local"]
    },
    {
      "name": "front-camera",
      "model": "webcam",
      "api": "rdk:component:camera",
      "attributes": {
        "video_path": "video0"
      }
    }
  ]
}
```

This fragment contains three components: a left motor, a right motor, and a camera. When you add this fragment to a machine, that machine receives all three components automatically.

Update the fragment—for example, changing the camera's `video_path`—and all machines using the fragment receive the update.

## When to use fragments

Fragments are ideal when you're managing multiple machines with shared configuration requirements.

**Use fragments when:**
- You're deploying a fleet of identical or similar machines
- You need to maintain consistent configuration across multiple sites
- You want to test new configurations on a subset of machines before rolling them out fleet-wide
- You're distributing {{< glossary_tooltip term_id="module" text="modules" >}} or custom software across your fleet
- You need centralized control over configuration updates

**Common scenarios:**
- **Fleet standardization:** 50 delivery robots with identical hardware and software configurations
- **Multi-site deployment:** Solar monitoring stations across different locations sharing a common sensor setup, with site-specific overrides for local conditions
- **Staged testing:** Testing a new camera configuration on 5 machines before deploying to 200 machines
- **Module distribution:** Deploying a custom driver module to all machines that use a specific sensor type

If you only have one or two machines, or if each machine requires completely unique configuration, fragments may add unnecessary complexity.
Use them when the scaling benefits of centralized configuration management outweigh the overhead of creating and maintaining fragments.

## Fragment composition and nesting

Fragments can import other fragments, creating a nested architecture. This allows you to build modular configurations that combine in flexible ways.

### Example: Building up from base configurations

Consider a fleet of 50 rovers:
- All 50 rovers need the basic hardware: motors, wheels, and base components (base rover fragment)
- 20 of these rovers need a robotic arm attachment (arm fragment)
- The other 30 need a different arm with a specialized gripper (alternative arm fragment)

Instead of creating 50 separate configurations or two complete configurations, you create three fragments:
1. A base rover fragment with the common hardware
2. An arm fragment for the standard attachment
3. An alternative arm fragment for the specialized gripper

Each machine imports the base rover fragment.
Then 20 machines also import the arm fragment, and 30 import the alternative arm fragment.
If you need to update the motor configuration, you change it once in the base rover fragment, and all 50 machines receive the update.

This composability extends as deep as you need.
A fragment can import another fragment, which itself imports additional fragments.
This creates a hierarchy of configuration that mirrors your deployment architecture.

## Visibility and sharing

When you create a fragment, you control who can see and use it through visibility settings.

**Private fragments** are visible only within your {{< glossary_tooltip term_id="organization" text="organization" >}}.
Use private visibility for proprietary configurations or internal deployment patterns you don't want to share externally.

**Public fragments** are discoverable by anyone.
This is useful when you're a hardware vendor providing reference configurations for your products, or when you want to share useful patterns with the broader Viam community.
Anyone can search for and use public fragments.

**Unlisted fragments** take a middle path.
They're not publicly searchable, but anyone with the direct link can access them.
This is useful for sharing configurations with partners, customers, or across different {{< glossary_tooltip term_id="organization" text="organizations" >}} without making them fully public.

You manage fragments through the dedicated fragments tab on your fleet page.
From there, you can create new fragments, modify existing ones, and change their visibility settings.

## Version management

Every time you edit a fragment, Viam automatically creates a new version with an incremented version number: 1, 2, 3, and so on.
You don't manage version numbers manually—the system handles this for you.
All previous versions are preserved, giving you a complete history of configuration changes.

When a machine uses a fragment, you control how it receives updates through version pinning strategies:

### Latest (default)

By default, machines will always use the newest version of the fragment.
When you update the fragment, machines receive the change immediately (for online machines) or on their next connection (for offline machines).
This is useful for active development and when you want changes to propagate automatically.

### Specific version

Alternatively, you can pin the machine to a particular version number. The machine will continue using that version number even when newer versions are available.
This provides stability and prevents unexpected changes, which is useful for production deployments that need predictable behavior.

### Tags

Tags are movable labels you can attach to specific version numbers.
Common tag names include "stable," "beta," and "development."
A machine pinned to a tag follows that tag as you move it between versions.

For example, you might tag version 5 as "stable."
Machines pinned to "stable" use version 5.
After testing version 6 on a small subset of machines, you move the "stable" tag to version 6.
All machines following the "stable" tag now receive version 6, but you controlled exactly when this happened by moving the tag.

Tags enable staged rollouts.
You can test changes on machines following a "beta" tag, then promote those changes to the "stable" tag when you're confident they work correctly.

### Update propagation

Machines that are online receive updates immediately when you change a fragment (if they're pinned to "latest" or a tag that has moved).
The system uses a polling mechanism—machines periodically check for configuration changes.
Machines that are offline receive updates the next time they connect.
No updates are lost due to temporary disconnections.

## Machine-level overrides

Fragments provide base configurations, but individual machines can override specific settings.
This handles the common case where you need fleet-wide standardization with occasional exceptions.

Overrides are part of the machine configuration, not the fragment.
When you override a fragment setting on a specific machine, the upstream fragment remains unchanged.
Other machines using that fragment are unaffected.

### When to use overrides

- **Hardware variations:** One machine has a failed GPIO pin, so you configure it to use a different pin while keeping the rest of the configuration identical to the fleet.
- **Site-specific settings:** A fleet of environmental monitors shares the same fragment, but one location requires a different sampling interval due to local regulations.
- **Testing and debugging:** You temporarily increase the log level on a single machine to diagnose an issue, without affecting other machines or changing the fragment.

### Override behavior

If any part of an override fails to apply, none of the overrides apply.
This prevents partial configuration states that could leave a machine in an inconsistent condition.

When the upstream fragment changes, those changes still flow to machines with overrides, but the overridden fields remain in place.
For example, if a machine overrides a camera's port but uses the fragment for everything else, an update to the motor configuration in the fragment still applies, but the camera port keeps using the overridden value.

### Override example

Suppose your rover fragment configures a motor with specific pins, but one rover has a faulty GPIO pin and needs to use different pins.

**Original fragment (used by all rovers):**

```json
{
  "components": [
    {
      "name": "left-motor",
      "model": "gpio",
      "api": "rdk:component:motor",
      "attributes": {
        "pins": {
          "a": "12",
          "b": "11",
          "pwm": "33"
        },
        "board": "local",
        "max_rpm": 150
      }
    }
  ]
}
```

**Machine configuration with override:**

On the machine with the faulty pin, you add an override to use different pins:

```json
{
  "fragments": [
    {
      "id": "abc123..."
    }
  ],
  "fragment_mods": [
    {
      "fragment_id": "abc123...",
      "mods": [
        {
          "$set": {
            "components.left-motor.attributes.pins.a": "16",
            "components.left-motor.attributes.pins.b": "15"
          }
        }
      ]
    }
  ]
}
```

This machine now uses pins 16 and 15 instead of 12 and 11, but still gets all other settings from the fragment.
If you later update the fragment to change `max_rpm` to 200, this machine receives that update—but keeps its custom pin configuration.

This balance between standardization and flexibility lets you manage large fleets with consistent configurations while handling real-world exceptions.

## Fragment variables

Fragments support variable substitution, allowing you to parameterize configurations.
This creates templates where the structure stays the same but specific values differ per machine.

For example, you might have a fleet of rovers where each needs a camera, but the video device path differs per machine.
Instead of creating separate fragments or using overrides, you can use a variable.

**Fragment definition with variable:**

```json
{
  "components": [
    {
      "name": "camera",
      "model": "webcam",
      "api": "rdk:component:camera",
      "attributes": {
        "video_path": {
          "$variable": {
            "name": "cam_device"
          }
        }
      }
    }
  ]
}
```

**Machine configuration using the fragment:**

When you add this fragment to a machine, you provide the variable value:

```json
{
  "fragments": [
    {
      "id": "abc123...",
      "variables": {
        "cam_device": "video0"
      }
    }
  ]
}
```

Another machine using the same fragment might set `"cam_device": "video1"`.
The fragment structure stays the same, but each machine gets its specific device path.

This is an advanced feature most useful when you have nearly identical configurations with just a few differing parameters.
For many use cases, creating separate fragments or using machine-level overrides is simpler.

For detailed information on fragment variables, see [Reuse machine configuration](/manage/fleet/reuse-configuration/).


## Testing and production workflows

Fragments support different workflows depending on whether you're preparing for production deployment or managing live systems.

### Before production

When you're first developing a fleet configuration, you typically start by configuring a single test machine until it works correctly.
Once satisfied with the configuration, you copy the entire JSON configuration and create a fragment from it.
This gives you a tested, proven configuration as your starting point.

You can then deploy this fragment to additional machines.
Test on a small subset first—perhaps 2-3 machines—before rolling out to your entire fleet.
This staged approach catches issues before they affect production systems.

### After production

When you need to modify a live fragment, direct changes would immediately affect all machines using it (if pinned to "latest").
This is risky for production systems.

A safer approach: create a new fragment based on your existing production fragment.
Give it a different name, like "production-rover-test."
Make your changes to this test fragment and deploy it to a single machine or small subset.
Test thoroughly.

Once you've validated the changes, copy the configuration from the successful test fragment back to your main production fragment.
The changes now roll out to your fleet in a controlled way.

Alternatively, use version tags for staged rollouts.
Keep some machines pinned to a "beta" tag and others to a "stable" tag.
Deploy changes to beta first, validate, then move the "stable" tag to promote the changes.


## Next steps

Now that you understand what fragments are and how they work, you're ready to create and deploy them.

For step-by-step instructions on creating fragments, configuring visibility settings, managing versions, and applying fragments to machines, see [Reuse machine configuration](/manage/fleet/reuse-configuration/).

### Related resources

- [Provision machines at scale](/manage/fleet/provision/) - Factory setup and automated provisioning
- [Software updates](/manage/software/update-software/) - Managing software versions across your fleet
- [Air quality fleet tutorial](/tutorials/control/air-quality-fleet/) - Hands-on example of managing multiple machines
- [Organization management and RBAC](/manage/manage/rbac/) - Control who can create and modify fragments
