---
title: "How the Viam RDK manages modular resources."
linkTitle: "Modular Resource Management"
weight: 10
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
---

## Modular Resource Management with the RDK

### Dependency Management

Modular resources may depend on other built-in resources or other modular resources, and vice versa.
The Viam RDK handles dependency management.

### Startup

RDK ensures that any configured modules are loaded automatically on startup, and that configured modular resource instances are started alongside configured built-in resources instances.

### Reconfiguration

When you reconfigure a Viam robot (meaning, when you change its configuration), the behavior of modular resource instances versus built-in resource instances is equivalent.
This means you can add, modify, and remove a modular resource instance from a running robot as normal.

### Shutdown

During robot shutdown, the RDK handles modular resource instances similarly to built-in resource instances - it signals them for shutdown in topological (dependency) order.