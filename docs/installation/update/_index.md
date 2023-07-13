---
title: "Update viam-server"
linkTitle: "Update viam-server"
weight: 40
simple_list: false
type: docs
draft: false
image: "/installation/thumbnails/update.png"
imageAlt: "Update viam-server"
images: ["/installation/thumbnails/update.png"]
description: "Update your version of viam-server."
---

## Channels

There are two main channels for updates.
If you download a file for one of them, its self-update function will only look for updates from that particular channel.
That is to say, "latest" will get a lot of updates, and "stable" will get them less frequently.

### Latest

This is updated on every merge to the main branch of the codebase from which `viam-server` is built.

### Stable

Updates will be far less frequent.

## Update Methods

{{< tabs name="Updating viam-server" >}}
{{% tab name=Linux %}}

### Manual / Service-based

These app images have a built in self-update feature.
To update manually, just run the file with "--aix-update" as the only argument.
For example:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo viam-server --aix-update
```

When installed as a system service, this will be run automatically each time the service is started.

#### Disable Service-based Updates

If you want to DISABLE automatic updates from the service file, just comment out the following line in `/etc/systemd/system/viam-server.service` with a pound sign (#) so that it looks like this:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
# ExecStartPre=-/usr/local/bin/viam-server --aix-update
```

<br>

### Fallback (Re-download)

Lastly, if all else fails, or you ever encounter any issues, you can simply just replace the file (usually `/usr/local/bin/viam-server`) with a newly downloaded copy.
There is typically no need to reinstall the system service (unless the new version includes an update to the service file), but there is no harm in doing so either.

{{% /tab %}}
{{% tab name=macOS %}}

You can upgrade to the latest *stable* version of `viam-server` using Homebrew.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew upgrade viam-server
```

To upgrade to the *absolute latest* version of `viam-server` run this command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew upgrade viam-server --HEAD
```

There is not a way to automatically update `viam-server` on Mac, so we recommend running `brew upgrade viam-server` on a regular basis.

{{% /tab %}}
{{% /tabs %}}
