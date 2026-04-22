---
linkTitle: "Overview"
title: "Viam CLI overview"
weight: 1
layout: "docs"
type: "docs"
description: "The Viam CLI gives you command-line access to every operation in the Viam platform, from machine configuration to data export to fleet management."
---

The Viam CLI is a single binary that gives you command-line access to the Viam platform.
Everything you can do in the Viam app, and several things you can only do from the command line, are available as CLI commands.

## When to use the CLI

If you prefer working in a terminal, the CLI covers the same operations as the Viam app.
You can use whichever interface you prefer, or both.

The CLI is particularly well-suited for tasks that are awkward or impossible in a browser:

- **Scripting and automation.** Create machines, export data, upload modules, or submit training jobs from shell scripts and CI/CD pipelines.
- **Headless environments.** Authenticate with an API key, view logs, and shell into a remote machine without a browser.
- **Bulk operations.** List all machines across an organization, or export binary data filtered by location, machine, or component type.
- **Operations only available through the CLI.** Scaffold new modules, transfer files to and from machines, tunnel ports, and hot-reload modules during development.

## What the CLI covers

| Area                     | What you can do                                                  | Guide                                                              |
| ------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------ |
| Machine configuration    | Create machines, add components and services, apply fragments    | [Configure machines](/cli/configure-machines/)                     |
| Data management          | Export, tag, and delete captured data; configure database access | [Manage data](/cli/manage-data/)                                   |
| Datasets and ML training | Create datasets, submit training jobs, run inference             | [Datasets and training](/cli/datasets-and-training/)               |
| Data pipelines           | Create and manage scheduled MQL aggregation pipelines            | [Data pipelines](/cli/data-pipelines/)                             |
| Module development       | Scaffold, build, upload, and version modules                     | [Build and deploy modules](/cli/build-and-deploy-modules/)         |
| Fleet operations         | Monitor status, stream logs, shell into machines, copy files     | [Manage your fleet](/cli/manage-your-fleet/)                       |
| Organization admin       | Manage API keys, configure OAuth, set up billing                 | [Administer your organization](/cli/administer-your-organization/) |
| Scripting and CI/CD      | Authenticate in scripts, automate common workflows               | [Automate with scripts](/cli/automate-with-scripts/)               |

### CLI-only operations

Some operations are only available through the CLI:

- **Module scaffolding** (`viam module generate`) creates a new module project with boilerplate code and a build script.
- **Shell access** (`viam machines part shell`) opens an interactive terminal on a remote machine.
- **File transfer** (`viam machines part cp`) copies files to and from machines.
- **Port tunneling** (`viam machines part tunnel`) forwards a local port to a remote machine.
- **Module hot-reload** (`viam module reload`) builds a module and syncs it to a running machine without restarting the machine.

## Install

{{< readfile "/static/include/how-to/install-cli.md" >}}

Verify the installation:

```sh {class="command-line" data-prompt="$"}
viam version
```

To update the CLI to the latest version:

```sh {class="command-line" data-prompt="$"}
viam update
```

## Authenticate

{{< readfile "/static/include/how-to/auth-cli.md" >}}

Authentication tokens refresh automatically. You do not need to re-authenticate between sessions unless your token is revoked.

To check who you are authenticated as:

```sh {class="command-line" data-prompt="$"}
viam whoami
```

This prints your email if you logged in interactively, or `key-<uuid>` if you authenticated with an API key.

To end your session:

```sh {class="command-line" data-prompt="$"}
viam logout
```

To print your current access token (for piping into other tools, only works with interactive login, not API keys):

```sh {class="command-line" data-prompt="$"}
viam login print-access-token
```

### Authenticate in scripts and CI/CD

Scripts and CI/CD pipelines cannot complete an interactive login. Use API key authentication instead:

```sh {class="command-line" data-prompt="$"}
viam login api-key --key-id=<key-id> --key=<key>
```

To create an API key, see [Manage API keys](/cli/administer-your-organization/#manage-api-keys).

### Authenticate on a machine without a local browser

Interactive login normally opens a browser on the current machine. To log in on a machine without a local browser (for example, over SSH), pass `--no-browser`:

```sh {class="command-line" data-prompt="$"}
viam login --no-browser
```

The CLI prints an authentication URL. Open it in a browser on any machine to complete login.

## Set defaults

If you work primarily within one organization or location, set defaults to avoid passing `--org-id` or `--location-id` on every command.
The CLI validates that the org or location exists and is accessible before saving.
Defaults are scoped to the active profile, so each profile can have its own default org and location.

```sh {class="command-line" data-prompt="$"}
viam defaults set-org --org-id=<org-id>
```

```sh {class="command-line" data-prompt="$"}
viam defaults set-location --location-id=<location-id>
```

To find your organization ID:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

To find location IDs within your organization:

```sh {class="command-line" data-prompt="$"}
viam locations list
```

Clear defaults when you need to work across organizations:

```sh {class="command-line" data-prompt="$"}
viam defaults clear-org
```

```sh {class="command-line" data-prompt="$"}
viam defaults clear-location
```

## Manage authentication profiles

If you work across multiple organizations or use both personal and service accounts, profiles let you switch between saved credentials without re-authenticating.
Each profile stores an API key and maintains its own default org and location independently.

```sh {class="command-line" data-prompt="$"}
viam profiles add --profile-name=production --key-id=<key-id> --key=<key>
```

`profiles add` errors if the name already exists. Use `profiles update` to overwrite an existing profile:

```sh {class="command-line" data-prompt="$"}
viam profiles update --profile-name=production --key-id=<new-key-id> --key=<new-key>
```

Use a profile for a single command with the `--profile` global flag:

```sh {class="command-line" data-prompt="$"}
viam machines list --all --profile=production
```

Or set the `VIAM_CLI_PROFILE_NAME` environment variable to activate a profile for an entire shell session:

```sh {class="command-line" data-prompt="$"}
export VIAM_CLI_PROFILE_NAME=production
viam machines list --all
```

List and remove profiles:

```sh {class="command-line" data-prompt="$"}
viam profiles list
```

```sh {class="command-line" data-prompt="$"}
viam profiles remove --profile-name=staging
```

## Global flags

Every command accepts these flags:

| Flag                 | Description                                |
| -------------------- | ------------------------------------------ |
| `--profile`          | Use a saved authentication profile         |
| `--config`, `-c`     | Path to a CLI config file                  |
| `--debug`, `--vvv`   | Enable debug logging                       |
| `--quiet`, `-q`      | Suppress non-essential output              |
| `--disable-profiles` | Ignore all saved profiles for this command |

## Get help

Every command supports the `--help` flag:

```sh {class="command-line" data-prompt="$"}
viam --help
viam machines --help
viam machines part shell --help
```

## Enable shell completion

The CLI supports tab completion for commands, subcommands, and flag names.
To enable it, source the completion script for your shell.

{{< tabs >}}
{{% tab name="bash" %}}

Add to your `~/.bashrc`:

```sh {class="command-line" data-prompt="$"}
source <(viam completion bash)
```

{{% /tab %}}
{{% tab name="zsh" %}}

Add to your `~/.zshrc`:

```sh {class="command-line" data-prompt="$"}
source <(viam completion zsh)
```

{{% /tab %}}
{{% tab name="fish" %}}

```sh {class="command-line" data-prompt="$"}
viam completion fish > ~/.config/fish/completions/viam.fish
```

{{% /tab %}}
{{% tab name="PowerShell" %}}

```powershell {class="command-line" data-prompt=">"}
viam completion pwsh | Out-String | Invoke-Expression
```

{{% /tab %}}
{{< /tabs >}}

After sourcing the script, press **Tab** to complete commands and flags:

```sh {class="command-line" data-prompt="$"}
viam <Tab>         # lists all commands
viam machines <Tab> # lists subcommands of machines
viam data export <Tab> # lists subcommands of export
```
