---
title: Machine ID
id: machine-id
full_link:
short_description: A unique identifier assigned to each machine in the Viam platform.
aka:
type: "page"
---

A **Machine ID** is a unique identifier assigned to each {{< glossary_tooltip term_id="machine" text="machine" >}} in the Viam platform. This ID is used to identify and reference a specific machine within the Viam ecosystem.

Machine IDs are:

- Automatically generated when a new machine is created in the Viam app
- Used in the {{< glossary_tooltip term_id="machine-fqdn" text="machine FQDN" >}} (Fully Qualified Domain Name) to enable remote access
- Required for API calls that target a specific machine
- Used in authentication and authorization processes
- Visible in the Viam app UI and accessible via the API

The Machine ID is part of the machine's FQDN, which typically follows the format `<machine-id>.<location-id>.viam.cloud`. This FQDN is used when connecting to a machine remotely through the Viam cloud infrastructure.

When working with the Viam platform programmatically, you'll often need to reference the Machine ID to specify which machine you want to interact with.