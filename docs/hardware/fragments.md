---
linkTitle: "Fragments"
title: "Fragments"
weight: 12
layout: "docs"
type: "docs"
description: "Capture working hardware configurations and keep them consistent across your fleet."
date: "2025-03-07"
---

Getting hardware to work together takes effort. Calibrating a camera mounted
on an arm, tuning motor PID parameters, getting the frame transforms right
between components. This work can take hours, and it's easy to lose when you
set up the next machine.

A **fragment** captures a working hardware configuration so you don't repeat
that work. Define the configuration once, including components, attributes,
and spatial relationships, then apply it to every machine that uses the same
hardware. When you update the fragment, every machine gets the update
automatically on its next config sync.

## Use existing fragments

When you search for a configuration block in the Viam app, fragments appear
alongside individual models. If a fragment matches your hardware combination,
use it. Someone has already figured out the right configuration for those
components working together.

For example, if you're setting up an xArm 6 with a wrist-mounted RealSense
camera, a fragment for that combination configures both components and their
spatial relationship in one step, rather than adding and configuring each one
individually.

## Save your own configurations

Once you get a combination of components working together, capture it as a
fragment so you can reuse it:

1. Go to your organization's
   [FRAGMENTS page](https://app.viam.com/fragments) in the Viam app.
2. Create a new fragment.
3. Add the components and their attributes. You can copy JSON from a working
   machine's configuration to get started.

The next time you build a machine with the same hardware, you can add the
fragment instead of configuring each component from scratch.

### Fragment variables

If part of the configuration varies between machines, use a **fragment
variable** instead of a fixed value. For example, if the arm's IP address
differs per machine:

```json
{
  "host": {
    "$variable": {
      "name": "arm_ip"
    }
  }
}
```

Each machine sets the `arm_ip` variable to its own arm's address. Everything
else comes from the fragment.

### How fragments merge

When you add a fragment to a machine, its configuration merges with the
machine's own configuration. If you update the fragment later, every machine
using it gets the update automatically on its next config sync.

## Contribute to the community

If you've built and tested a configuration that others with the same hardware
would benefit from, consider sharing it. Contributing fragments to the
registry means the next person setting up that hardware combination can start
from a working config instead of building one from scratch.

For the full walkthrough on creating and managing fragments, see
[Reuse Machine Configuration](/fleet/reuse-configuration/).

## Related

- [Add a component](/hardware/common-components/): step-by-step guides for
  each component type.
- [What is a module?](/build-modules/overview/): write
  modules that tie your components together.
- [Reuse Machine Configuration](/fleet/reuse-configuration/): the
  complete guide to fragment creation, variables, and fleet-wide deployment.
