---
linkTitle: "Module reference"
title: "Module developer reference"
weight: 40
layout: "docs"
type: "docs"
description: "Reference for module developers: lifecycle, interfaces, meta.json schema, CLI commands, environment variables, and registry rules."
date: "2025-03-05"
aliases:
  - /development/module-reference/
---

This page is a reference for module developers. For step-by-step
instructions, see [Write a Module](/build-modules/write-a-driver-module/) and
[Deploy a Module](/build-modules/deploy-a-module/).

## Module lifecycle

Every module, local or registry, runs as a separate child process alongside
`viam-server`, communicating over [gRPC](#module-protocol).

1. `viam-server` starts and checks for configuration updates (if online).
2. If the module has a [`first_run`](#first-run-scripts) script that hasn't
   succeeded yet, `viam-server` runs it before starting the module.
3. `viam-server` starts each configured module as a child process, passing it a
   socket address.
4. The module registers its models and APIs with `viam-server` through the
   [`Ready` RPC](#module-protocol).
5. For each configured resource, `viam-server` calls `ValidateConfig` to check
   attributes and discover dependencies.
6. `viam-server` starts required dependencies first. If a required dependency
   fails, the resource that depends on it does not start.
7. `viam-server` calls `AddResource` to create each resource. The module's
   constructor runs, typically calling `Reconfigure` to read config.
8. The resource is available for use.
9. When the user changes configuration, `viam-server` calls
   `ReconfigureResource`. Your `Reconfigure` method should complete
   within the per-resource configuration timeout (default: 2 minutes,
   configurable with `VIAM_RESOURCE_CONFIGURATION_TIMEOUT`).
10. On shutdown, `viam-server` sends `RemoveResource` for each resource, then
    terminates the module process.

### First-run scripts

If your module needs one-time setup (installing system packages, downloading
models, etc.), set the `first_run` field in [`meta.json`](#metajson-schema) to
the path of a setup script inside your archive.

- The script runs **before** the module entrypoint, with the same
  [environment variables](#environment-variables) available to the module.
- If the script exits with a non-zero status, reconfiguration is aborted.
  Currently running modules continue with their previous configuration.
- On success, a `.first_run_succeeded` marker file is created next to the
  module binary. The script will not re-run unless this marker is deleted
  or a new module version is installed.
- The default timeout is 1 hour, configurable through `first_run_timeout` in the
  module config.

### Crash recovery

If a module process crashes, `viam-server` automatically restarts it:

1. `viam-server` detects the exit and marks the module as failed.
2. The machine's status changes to **initializing**.
3. `viam-server` retries every 5 seconds.
4. On success, `viam-server` re-adds all resources in dependency order.
5. The machine returns to **running**.

If the module keeps crashing, `viam-server` retries indefinitely. Check the
**LOGS** tab for crash tracebacks.

### Communication

By default, modules communicate with `viam-server` over a Unix domain socket
with a randomized name.

TCP mode is used automatically on Windows or when the Unix socket path would
exceed the OS limit (103 characters on macOS). Force TCP mode by setting
`"tcp_mode": true` in the module config or setting `VIAM_TCP_SOCKETS=true`.

### Data directory

Every module receives a persistent data directory at
`~/.viam/module-data/<robot-id>/<module-name>/`. The path is available inside
the module through the `VIAM_MODULE_DATA` environment variable. This directory
persists across module restarts and reconfigurations.

### Timeouts

| Event                                   | Timeout                                                        | Behavior on timeout                       |
| --------------------------------------- | -------------------------------------------------------------- | ----------------------------------------- |
| Module startup (ready check)            | 5 minutes (configurable through `VIAM_MODULE_STARTUP_TIMEOUT`) | Module marked as failed; retry begins     |
| Config validation                       | 5 seconds                                                      | Validation fails; resource does not start |
| Resource removal during shutdown        | 20 seconds (all resources combined)                            | Resources orphaned                        |
| Module closure (removal + process stop) | ~30 seconds total                                              | Process killed                            |
| First-run setup script                  | 1 hour (configurable through `first_run_timeout`)              | Module startup fails                      |
| Crash restart retry interval            | 5 seconds                                                      | Next attempt after delay                  |

## Resource interfaces (Go)

### Config validation

```go
type ConfigValidator interface {
    Validate(path string) (requiredDependencies, optionalDependencies []string, err error)
}
```

Return required dependency names in the first slice. `viam-server` ensures they
are ready before calling your constructor. Return optional dependency names in
the second slice. These are passed to the constructor if available, but their
absence does not block startup.

### Resource interface

Every resource must implement:

```go
type Resource interface {
    Name() Name
    Reconfigure(ctx context.Context, deps Dependencies, conf Config) error
    DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error)
    Close(ctx context.Context) error
}
```

Plus the methods defined by the specific API (for example, `Readings` for sensor,
`GetImages` for camera).

### Constructor signature

```go
func(ctx context.Context, deps resource.Dependencies,
    conf resource.Config, logger logging.Logger) (ResourceT, error)
```

### Helper traits

Embed these in your resource struct to get default implementations:

| Trait                              | Effect                                                                                           |
| ---------------------------------- | ------------------------------------------------------------------------------------------------ |
| `resource.Named`                   | Interface for `Name()` and `DoCommand()`. Embed and set through `conf.ResourceName().AsNamed()`. |
| `resource.TriviallyCloseable`      | `Close()` returns nil.                                                                           |
| `resource.TriviallyReconfigurable` | `Reconfigure()` returns nil (no-op).                                                             |
| `resource.AlwaysRebuild`           | `Reconfigure()` returns `MustRebuildError` (always re-create).                                   |
| `resource.TriviallyValidateConfig` | `Validate()` returns no deps and no error.                                                       |

### Useful functions

| Function                          | Description                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------ |
| `resource.NativeConfig[*T](conf)` | Convert config attributes to a typed struct.                                         |
| `<api>.FromProvider(deps, name)`  | Type-safe dependency lookup (for example, `sensor.FromProvider(deps, "my-sensor")`). |
| `conf.ResourceName().AsNamed()`   | Create a `Named` implementation from config.                                         |
| `module.ModularMain(models...)`   | Convenience entry point for simple modules.                                          |
| `module.NewModuleFromArgs(ctx)`   | Create a module from CLI args (for custom entry points).                             |
| `module.NewLoggerFromArgs(name)`  | Create a logger that routes to `viam-server`.                                        |

## Resource interfaces (Python)

### Config validation

```python
@classmethod
def validate_config(cls, config: ComponentConfig) -> Tuple[Sequence[str], Sequence[str]]:
    # Return (required_deps, optional_deps)
    return [], []
```

### Constructor

```python
@classmethod
def new(cls, config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
    instance = cls(config.name)
    instance.reconfigure(config, dependencies)
    return instance
```

### Reconfigure

```python
def reconfigure(self, config: ComponentConfig,
                dependencies: Mapping[ResourceName, ResourceBase]) -> None:
    # Update internal state from new config
    pass
```

### Close

```python
async def close(self):
    # Clean up connections, stop background tasks, release hardware.
    # Must be idempotent (safe to call multiple times).
    pass
```

The default `close()` on `ResourceBase` is a no-op.

### EasyResource base class

For simple modules, inherit from both the API base class and `EasyResource` to
get default `new()`, `validate_config()`, and automatic model registration:

```python
from viam.components.sensor import Sensor
from viam.resource.easy_resource import EasyResource
from viam.module.module import Module


class MySensor(Sensor, EasyResource):
    MODEL = "my-org:my-module:my-sensor"

    async def get_readings(self, **kwargs):
        return {"temperature": 23.5}


if __name__ == '__main__':
    import asyncio
    asyncio.run(Module.run_from_registry())
```

### Useful functions

| Function                          | Description                                                      |
| --------------------------------- | ---------------------------------------------------------------- |
| `Module.from_args()`              | Create a module from CLI args.                                   |
| `Module.run_from_registry()`      | Discover and register all imported resource classes, then start. |
| `Module.run_with_models(*models)` | Register explicit model classes, then start.                     |
| `getLogger(name)`                 | Create a logger (`from viam.logging import getLogger`).          |
| `config.attributes.fields`        | Access raw config attributes (no typed config equivalent to Go). |

### Python and Go defaults

In Python, the default behavior when you don't implement a method differs from Go:

| Behavior                 | Go                                       | Python                                                                                   |
| ------------------------ | ---------------------------------------- | ---------------------------------------------------------------------------------------- |
| Seamless reconfigure     | Implement `Reconfigure()`                | Implement `reconfigure()` (called if your class satisfies the `Reconfigurable` protocol) |
| Rebuild on config change | Embed `resource.AlwaysRebuild`           | Omit `reconfigure()` (default: module destroys and re-creates the resource)              |
| No-op reconfigure        | Embed `resource.TriviallyReconfigurable` | No equivalent: implement an empty `reconfigure()` instead                                |
| No-op close              | Embed `resource.TriviallyCloseable`      | Default on `ResourceBase`                                                                |
| Skip config validation   | Embed `resource.TriviallyValidateConfig` | Default on `EasyResource`                                                                |

## Logging

From modules you can log at the resource level or at the machine level.
Resource-level logging is recommended because it makes it easier to identify
which component or service produced a message. Resource-level error logs also
appear in the **Error logs** section of each resource's configuration card.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Resource-level logging (recommended):
self.logger.debug("debug info")
self.logger.info("info")
self.logger.warn("warning info")
self.logger.error("error info")
self.logger.exception("error info", exc_info=True)
self.logger.critical("critical info")
```

For machine-level logging instead of resource-level:

```python
from viam.logging import getLogger

LOGGER = getLogger(__name__)

LOGGER.debug("debug info")
LOGGER.info("info")
LOGGER.warn("warning info")
LOGGER.error("error info")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func (c *component) someFunction(ctx context.Context, a int) {
  // Log with severity info:
  c.logger.CInfof(ctx, "performing some function with a=%v", a)
  // Log with severity debug (using value wrapping):
  c.logger.CDebugw(ctx, "performing some function", "a" ,a)
  // Log with severity warn:
  c.logger.CWarnw(ctx, "encountered warning for component", "name", c.Name())
  // Log with severity error without a parameter:
  c.logger.CError(ctx, "encountered an error")
}
```

{{% /tab %}}
{{< /tabs >}}

To see debug-level logs, run `viam-server` with the `-debug` flag or
[configure debug logging](/operate/reference/viam-server/#logging) for your
machine or individual resource.

## Common gotchas

**Always call `Reconfigure` from your constructor.**
Your constructor and `Reconfigure` should share the same config-reading logic.
The typical pattern is for the constructor to create the struct, then call
`Reconfigure` to populate it from config. This avoids duplicating config
parsing and ensures a newly created resource is fully configured.

**Clean up in `Close()`.**
If your resource starts background goroutines, opens connections, or holds
hardware handles, `Close()` must stop them. Leaked goroutines accumulate across
reconfigurations and can cause instability.
In Python, `close()` must be idempotent (it may be called more than once).

**Return the right dependency names from `Validate`.**
Dependencies listed as required in `Validate` (Go) or `validate_config`
(Python) must match actual resource names in the machine config. If the name
is wrong, `viam-server` waits for a resource that will never exist, and your
resource will not start. Use optional dependencies for resources that improve
functionality but aren't strictly needed.

**Prefer `Reconfigure` over `AlwaysRebuild`.**
`AlwaysRebuild` (Go) or omitting `reconfigure()` (Python) causes the resource
to be destroyed and re-created on every config change. This is simpler but
causes a brief availability gap. Implementing `Reconfigure` to update state
in-place provides seamless reconfiguration.

## Module protocol

Modules communicate with `viam-server` over gRPC using the `ModuleService`
defined in `proto/viam/module/v1/module.proto`:

All RPCs are initiated by `viam-server` and handled by the module:

| RPC                   | Purpose                                                  |
| --------------------- | -------------------------------------------------------- |
| `Ready`               | Handshake: module returns its supported API/model pairs. |
| `AddResource`         | Create a new resource instance from config.              |
| `ReconfigureResource` | Update an existing resource with new config.             |
| `RemoveResource`      | Destroy a resource instance.                             |
| `ValidateConfig`      | Validate config and return implicit dependencies.        |

The module also connects back to the parent `viam-server` to access other
resources (dependencies) on the machine.

## meta.json schema

Every module has a `meta.json` file that describes the module to the registry.
The full schema is available at `https://dl.viam.dev/module.schema.json`.

```json
{
  "$schema": "https://dl.viam.dev/module.schema.json",
  "module_id": "my-org:my-module",
  "visibility": "private",
  "url": "https://github.com/my-org/my-module",
  "description": "Short description of the module.",
  "models": [
    {
      "api": "rdk:component:sensor",
      "model": "my-org:my-module:my-sensor",
      "short_description": "A short description of this model.",
      "markdown_link": "README.md#my-sensor"
    }
  ],
  "entrypoint": "run.sh",
  "first_run": "setup.sh",
  "markdown_link": "README.md",
  "build": {
    "setup": "./setup.sh",
    "build": "./build.sh",
    "path": "module.tar.gz",
    "arch": ["linux/amd64", "linux/arm64"]
  }
}
```

| Field                        | Type   | Required | Description                                                                                                                                          |
| ---------------------------- | ------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$schema`                    | string | No       | JSON Schema URL for editor validation.                                                                                                               |
| `module_id`                  | string | Yes      | `namespace:name` or `org-id:name`.                                                                                                                   |
| `visibility`                 | string | Yes      | `private`, `public`, or `public_unlisted`.                                                                                                           |
| `url`                        | string | No       | Source repo URL. Required for cloud builds.                                                                                                          |
| `description`                | string | Yes      | Short description shown in the registry.                                                                                                             |
| `models`                     | array  | No       | List of API/model pairs the module provides. Deprecated: models are now inferred from the module binary.                                             |
| `models[].api`               | string | Yes      | Resource API (for example, `rdk:component:sensor`).                                                                                                  |
| `models[].model`             | string | Yes      | Model triplet (for example, `my-org:my-module:my-sensor`).                                                                                           |
| `models[].short_description` | string | No       | Short model description (max 100 chars).                                                                                                             |
| `models[].markdown_link`     | string | No       | Path to model docs within the repo.                                                                                                                  |
| `entrypoint`                 | string | Yes      | Path to the executable inside the archive.                                                                                                           |
| `first_run`                  | string | No       | Path to a one-time setup script. Runs before the entrypoint on first install and after version updates. See [First-run scripts](#first-run-scripts). |
| `markdown_link`              | string | No       | Path to README used as registry description.                                                                                                         |
| `build`                      | object | No       | Build configuration for local and cloud builds.                                                                                                      |
| `build.setup`                | string | No       | One-time setup command (for example, install dependencies).                                                                                          |
| `build.build`                | string | No       | Build command (for example, `make module.tar.gz`).                                                                                                   |
| `build.path`                 | string | No       | Path to built artifact. Default: `module.tar.gz`.                                                                                                    |
| `build.arch`                 | array  | No       | Target platforms. Default: `["linux/amd64", "linux/arm64"]`.                                                                                         |
| `build.darwin_deps`          | array  | No       | Homebrew dependencies for macOS builds (for example, `["go", "pkg-config"]`).                                                                        |
| `applications`               | array  | No       | Viam applications provided by the module. See [Applications](#applications).                                                                         |

### Applications

If your module provides a [Viam application](/operate/control/viam-applications/),
define it in the `applications` array in `meta.json`.

Each application object has the following properties:

| Property         | Type     | Description                                                                                                                                                                                                                                  |
| ---------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`           | string   | The application name, used in the application's URL (`name_publicnamespace.viamapps.com`). Must be all-lowercase, alphanumeric and hyphens only, cannot start or end with a hyphen, and must be unique within your organization's namespace. |
| `type`           | string   | `"single_machine"` or `"multi_machine"`. Whether the application can access one machine or multiple machines.                                                                                                                                |
| `entrypoint`     | string   | Path to the HTML entry point (for example, `"dist/index.html"`).                                                                                                                                                                             |
| `fragmentIds`    | []string | Fragment IDs a machine must contain to be selectable from the machine picker. Single-machine applications only.                                                                                                                              |
| `logoPath`       | string   | URL or relative path to the logo for the machine picker screen. Single-machine applications only.                                                                                                                                            |
| `customizations` | object   | Override branding on the authentication screen. Contains a `machinePicker` object with properties: `heading` (max 60 chars), `subheading` (max 256 chars).                                                                                   |

For example, if your organization namespace is `acme` and your application name
is `dashboard`, your application is accessible at:

```txt
https://dashboard_acme.viamapps.com
```

### Organization namespace

When uploading modules to the Viam Registry, you must set a unique namespace
for your organization.

**Create a namespace:** In the Viam app, click your organization name in the
top navigation bar, then click **Settings**, then click **Set a public namespace**. Enter a
name and click **Set namespace**. Namespaces may only contain letters, numbers,
and hyphens (`-`).

**Rename a namespace:**

1. Navigate to your organization settings page.
2. Click **Rename** next to your current namespace.
3. Enter the new namespace name and click **Rename**.
4. Update the module code and `meta.json` for each module your organization owns
   to reflect the new namespace.
5. (Recommended) Update the `model` field in machine configurations that
   reference the old namespace. Old references continue to work, but updating
   avoids confusion.

When you rename a namespace, Viam reserves the old namespace for backwards
compatibility: it cannot be reused.

## CLI commands

All module CLI commands are under `viam module`. You must be logged in
(`viam login`) to use commands that interact with the registry.

### Create and generate

| Command                            | Description                                                              |
| ---------------------------------- | ------------------------------------------------------------------------ |
| `viam module create --name <name>` | Register a module in the registry and generate `meta.json`.              |
| `viam module generate`             | Scaffold a complete module project with templates (interactive prompts). |

`generate` flags: `--name`, `--language` (`python` or `go`), `--visibility`,
`--public-namespace`, `--resource-subtype`, `--model-name`, `--register`,
`--dry-run`.

### Build

| Command                                      | Description                                       |
| -------------------------------------------- | ------------------------------------------------- |
| `viam module build local`                    | Run the build command from `meta.json` locally.   |
| `viam module build start --version <semver>` | Start a cloud build for all configured platforms. |
| `viam module build list`                     | List cloud build jobs and their status.           |
| `viam module build logs --id <build-id>`     | Stream logs from a cloud build job.               |

`build start` flags: `--ref` (git ref, default: `main`), `--platforms`,
`--token` (for private repos), `--workdir`.

During builds, the environment variables `VIAM_BUILD_OS` and `VIAM_BUILD_ARCH`
are set to the target platform. See [Environment variables](#environment-variables).

### Upload and update

| Command                                                       | Description                                              |
| ------------------------------------------------------------- | -------------------------------------------------------- |
| `viam module upload --version <semver> --platform <platform>` | Upload a built archive to the registry.                  |
| `viam module update`                                          | Push updated `meta.json` to the registry.                |
| `viam module update-models --binary <path>`                   | Auto-detect models from a binary and update `meta.json`. |
| `viam module download --id <module-id>`                       | Download a module from the registry.                     |

`upload` flags: `--tags` (platform constraints), `--force` (skip validation),
`--upload` (path to archive).

### Development loop

| Command                                   | Description                                                 |
| ----------------------------------------- | ----------------------------------------------------------- |
| `viam module reload-local --part-id <id>` | Build locally, transfer to machine, configure, and restart. |
| `viam module reload --part-id <id>`       | Build in cloud; machine downloads the package directly.     |
| `viam module restart --part-id <id>`      | Restart a running module without rebuilding.                |

`reload-local` flags: `--part-id` (target machine part), `--no-build` (skip
build), `--local` (run entrypoint directly on localhost instead of bundling),
`--model-name` (add a resource to config with this model triple),
`--name` (name the added resource), `--resource-name` (name the resource
instance), `--id` (module ID, alternative to `--name`),
`--cloud-config` (path to `viam.json`, alternative to `--part-id`),
`--workdir` (subdirectory containing `meta.json`), `--home-dir` (remote
user's home directory), `--no-progress` (hide transfer progress).

## Environment variables

### Runtime

These environment variables are available inside a running module process
(including [first-run scripts](#first-run-scripts)):

| Variable           | Description                                     |
| ------------------ | ----------------------------------------------- |
| `VIAM_MODULE_NAME` | The module's name from config.                  |
| `VIAM_MODULE_DATA` | Path to the module's persistent data directory. |
| `VIAM_MODULE_ROOT` | Parent directory of the module executable.      |
| `VIAM_MODULE_ID`   | Registry module ID (registry modules only).     |
| `VIAM_HOME`        | Path to the Viam home directory (`~/.viam`).    |

### Cloud-connected

When the machine is connected to Viam Cloud, these additional variables are
available inside the module process:

| Variable               | Description                                            |
| ---------------------- | ------------------------------------------------------ |
| `VIAM_API_KEY`         | API key (if an API key auth handler is configured).    |
| `VIAM_API_KEY_ID`      | API key ID (if an API key auth handler is configured). |
| `VIAM_MACHINE_ID`      | Cloud machine ID.                                      |
| `VIAM_MACHINE_PART_ID` | Cloud machine part ID.                                 |
| `VIAM_MACHINE_FQDN`    | Machine's fully qualified domain name.                 |
| `VIAM_LOCATION_ID`     | Cloud location ID.                                     |
| `VIAM_PRIMARY_ORG_ID`  | Primary organization ID.                               |

Custom environment variables can be added in the module's machine config under
the `env` field.

### Build-time

The following variables are set during [cloud builds](#build), not at runtime:

| Variable          | Description                                               |
| ----------------- | --------------------------------------------------------- |
| `VIAM_BUILD_OS`   | Target operating system (for example, `linux`, `darwin`). |
| `VIAM_BUILD_ARCH` | Target architecture (for example, `amd64`, `arm64`).      |

### Server-side

The following variables control `viam-server` startup behavior (not passed to modules):

| Variable                              | Description                                                                |
| ------------------------------------- | -------------------------------------------------------------------------- |
| `VIAM_MODULE_STARTUP_TIMEOUT`         | Override the default 5-minute startup timeout (for example, `10m`, `30s`). |
| `VIAM_RESOURCE_CONFIGURATION_TIMEOUT` | Override the default 2-minute per-resource configuration timeout.          |

## Supported platforms

| Platform        | Cloud build support                       |
| --------------- | ----------------------------------------- |
| `linux/amd64`   | Yes                                       |
| `linux/arm64`   | Yes                                       |
| `linux/arm32v6` | No                                        |
| `linux/arm32v7` | No                                        |
| `darwin/amd64`  | No                                        |
| `darwin/arm64`  | Yes                                       |
| `windows/amd64` | Yes                                       |
| `any`           | No (use for platform-independent modules) |

## Registry validation rules

| Rule                    | Constraint                                                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Module name             | 1-200 characters, `^[a-zA-Z0-9][-\w]*$` (must start with alphanumeric; may contain hyphens, underscores, letters, digits) |
| Module version          | Semantic versioning 2.0.0 (for example, `1.2.3`)                                                                          |
| Package name            | `^[\w-]+$`                                                                                                                |
| Metadata fields         | Max 16 key-value pairs                                                                                                    |
| Metadata key/value size | Max 500 KB each                                                                                                           |
| Compressed package      | Max 50 GB                                                                                                                 |
| Decompressed contents   | Max 250 GB                                                                                                                |
| Single file in package  | Max 25 GB                                                                                                                 |
| Model namespace         | Must match org namespace if org has one. Cannot use reserved namespace `rdk`.                                             |
| Public modules          | Require org to have a public namespace. Cannot use `public_unlisted` → `private` if external orgs are using the module.   |
