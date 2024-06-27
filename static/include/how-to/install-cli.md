You must have the Viam CLI installed to configure querying with third-party tools.

{{< tabs >}}
{{% tab name="macOS" %}}

To download the Viam CLI on a macOS computer, run the following commands:

```{class="command-line" data-prompt="$"}
brew tap viamrobotics/brews
brew install viam
```

{{% /tab %}}
{{% tab name="Linux aarch64" %}}

To download the Viam CLI on a Linux computer with the `aarch64` architecture, run the following commands:

```{class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-arm64
sudo chmod a+rx /usr/local/bin/viam
```

{{% /tab %}}
{{% tab name="Linux x86_64" %}}

To download the Viam CLI on a Linux computer with the `amd64` (Intel `x86_64`) architecture, run the following commands:

```{class="command-line" data-prompt="$"}
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-amd64
sudo chmod a+rx /usr/local/bin/viam
```

You can also install the Viam CLI using [brew](https://brew.sh/) on Linux `amd64` (Intel `x86_64`):

```{class="command-line" data-prompt="$"}
brew tap viamrobotics/brews
brew install viam
```

{{% /tab %}}
{{% tab name="Source" %}}

If you have [Go installed](https://go.dev/doc/install), you can build the Viam CLI directly from source using the `go install` command:

```sh {class="command-line" data-prompt="$"}
go install go.viam.com/rdk/cli/viam@latest
```

To confirm `viam` is installed and ready to use, issue the _viam_ command from your terminal.
If you see help instructions, everything is correctly installed.
If you do not see help instructions, add your local <file>go/bin/\*</file> directory to your `PATH` variable.
If you use `bash` as your shell, you can use the following command:

```sh {class="command-line" data-prompt="$"}
echo 'export PATH="$HOME/go/bin:$PATH"' >> ~/.bashrc
```

{{% /tab %}}
{{< /tabs >}}

For more information see [install the Viam CLI](/cli/#install).
